# flightscanner

Script that searches flights with given condition. You can build your own multistop flight with as many stops as you need and connections between them. You can also extend current model to add more filters etc. Uses sky scanner API to do the search.

## important
sky scanner API appears to only provide flight date without time, so the search is not as precise 

## setup
* setup virtualenv and install required packages
```cmd
pip install -r requirements.txt
```
* get skyscanner key, in order to do that you need to create an account on rapidapi: https://rapidapi.com/skyscanner/api/skyscanner-flight-search/details
* use sky scanner key to create `SkyScannerAPI`