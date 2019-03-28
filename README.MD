**README**

Application developed by Kareem Sait

Powered by Dark Sky API

https://darksky.net/dev

**Requirements:**

Dark Sky API Key

Python 3.7

Python "requests" library

**Assumptions:**

According to the Dark Sky documentation, they do not store forecast data in the time machine. Thus, all comparisons are 
done on the day the application is run. In other words, There is no "Observed" data for "Forecasted days" that have 
yet to occur, and there is no "Forecast data" for "days with Observed historical data" that have already occured in 
the past. The only comparison that can be done is for the day the application is run.

The goal and flow of the application is as follows:

1. Download forecasted and observed DAILY weather for today (not hourly or by minute etc...)
2. Store in JSON and retrieve only the elements for today (as the rest of the week's forecast has no observed data)
3. Compare the values of each key between forecasted and observed data to identify differences and print them out
4. Write the data to json files "forecast.json" and "observed.json" to allow them to be loaded to a separate application
 for further analysis

The file that is created is overwritten with each run because it is assumed this script is run once daily, 
and if it is rerun multiple times in one day, the latest record would be the desired record. There would be some other 
process to move this data to the desired analysis software. Concerns around making sure data is not lost could also 
be addressed in the future. Perhaps delete the file after ingestion to analysis software and edit this application to 
throw an error if the file exists so as not to overwrite unprocessed data (but manual intervention would be necessary if running 
multiple times in one day, or appending instead of overwritting if preserving all runs is desired).

**Key Validation Concept**

The application has 2 main validations run in the code to ensure the data being compared is the desired data sets.
1. The "time" key for both forecast and observed data has the same value ensuring the data for the same day is being 
compared in both data sets
2. The forecast "DAILY" data block has 8 elements (or at least more than 1) while the time machine request returns only 
1 data block for "today's date" for the "DAILY" request. Verifying the number of returned elements is this application's 
way to verify that the data being compared is between the "FORECAST" data and "OBSERVED" time machine data.

**Running the application**

1. Register and retrieve an API key from Dark Sky (https://darksky.net/dev)
2. Clone the repo to your working directory
3. Import the project into your favourite IDE (developed in IntelliJ)
4. Validate you have python 3.7 installed and configured as your SDK
5. Ensure the requests library is installed.
`sudo pip install requests `   
6. Set the enviornemt variable "darksky_key" to be your api key from step 1.
7. Run comparator.py
8. log level is set to "DEBUG" to see actual key by key comparisons and more information. Change to "INFO" for summary

Alternatively, you can run the python script by
`python3 comparator.py` from the command line (on a mac), but you will still need to set the env variable in step 6

**Tests**

There is a single "observed_test.json" file provided for testing. Uncommenting the code on line 118 inside the 
"compareWeather" function will load the test json. This will demonstrate the evaluation logic is functional by showing
what key/value pairs are different between forecast and observed data. This test json will not be written to 
observed.json as the functionality it is testing is the evaluation logic only.

**Exit Codes**

`0: Sucessful`

`1: Failed to download forecast data`

`2: Failed to download observed data`

`3: Forecast Data only had 1 data block`

`4: Observed Data had more than 1 data block`

`5: "Time" key differnet for forecast and observed data blocks`

