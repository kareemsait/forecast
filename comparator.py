import logging
import requests
import time
import json
import datetime
import os

# Set log level to debug to demonstrate code. Change this setting to INFO for production.
logging.basicConfig(level=logging.DEBUG)

class Comparotor():

    def main(self):
        # API Request Key
        key = os.environ.get('darksky_key', '')

        # Latitude and Longitude of Tokyo, Japan
        lat = os.environ.get('lat', '35.6762')
        lon = os.environ.get('lon', '139.6503')

        # Options of the GET Request to remove unneded data blocks
        options = '?units=ca&exclude=currently,minutely,hourly,alerts,flags'

        # Getting current time in order to submit a time machine request to ask for observed weather data for today
        # cast to str for concat to http request
        t = str(int(time.time()))

        # Create request URL to dark sky api for Daily FORECAST
        requestURL = 'https://api.darksky.net/forecast/' + key + '/' + lat + ',' + lon + options
        logging.debug(requestURL)
        forecastRequest = requests.get(requestURL)

        # Notify of Error if failed to request API and exit
        if forecastRequest.status_code != 200:
            logging.error("Error downloading weather forecast")
            exit(1)

        # Convert request result to json
        forecastJson = forecastRequest.json()
        numElm = len(forecastJson['daily']['data'])
        logging.debug('Forecast data block size: ' + str(numElm))
        if numElm < 2:
            logging.error("Number of elements indicates this is a time machine request instead of a forecast request")
            exit(3)

        # Retrieve only today's forecast info, not the whole week
        forecastToday = forecastJson['daily']['data'][0]
        forecastTime = forecastToday['time']

        # Print to debug
        logging.debug(forecastToday)

        # Create request url for time machine data using t which is the current timestamp
        # (this should retrieve observational data for today)
        requestURL = 'https://api.darksky.net/forecast/' + key + '/' + lat + ',' + lon + ',' + t + options
        logging.debug(requestURL)

        observedRequest = requests.get(requestURL)

        if observedRequest.status_code != 200:
            logging.error("Error downloading weather observation")
            exit(2)

        observedJson = observedRequest.json()
        numElm = len(observedJson['daily']['data'])
        logging.debug('Forecast data block size: ' + str(numElm))
        if numElm > 1:
            logging.error("Number of elements indicates this is a forecast request instead of a time machine request")
            exit(4)

        # There is only one element but it is a list, so retrieve the element in order to do key/value comparisons
        observedToday = observedJson['daily']['data'][0]
        observedTime = observedToday['time']

        if forecastTime != observedTime:
            logging.error("The time of the comparison does not match")
            exit(5)

        logging.debug(observedToday)

        # Call method to evaluate accuracy of forecast versus time machine data by passing both
        compareWeather(self, forecastToday, observedToday)

        # Write the data to file for later analysis
        write_json(self, forecastToday, observedToday)

def write_json(self,forecast, observed):

    # Wrtie the outputs of the forecasted and observed weather data to json files
    logging.info("Writting forecast data to 'forecast.json")
    with open('forecast.json', 'w') as outfile:
        json.dump(forecast, outfile)
    logging.info('Complete...')
    logging.info("Writting observed weather data to 'observed.json'")
    with open('observed.json', 'w') as outfile:
        json.dump(observed, outfile)
    logging.info('Complete...')

def load_test(self):

    with open('observed_test.json') as f:
        observed = json.load(f)
    return observed

def compareWeather(self,forecast, observed):

    identical = 'TRUE'

    # Test evaluation logic, remove comment on below to use custom test json as observational data
    #observed = load_test(self)

    #Print the timestamp of the comparison
    t = forecast['time']
    print('Comparison for: ' + str(datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')))

    for key in observed.keys():
        value = observed[key]

        logging.debug('observed key: %s' % key )
        logging.debug('observed value: %s' % value )
        logging.debug('forecast value: %s' % forecast[key])

        if forecast[key] != value:
            print("For KEY \"%s\" the VALUES are different" % key)
            print("Forecast says \"%s\" will be: %s " % (key, value))
            print("Observed says \"%s\" will be: %s " % (key, forecast[key]))
            identical = 'FALSE'

    if identical == 'TRUE':
        print("Both the forecast and observed weather for today is currently the same")

def main():
    logging.info('Started Weather Comparator...')
    c = Comparotor()
    c.main()


if __name__ == "__main__":
    main()