# Barnaby

Barnaby is a personal assistant API. This makes it offer many possibilities for integration with your projects. It uses APIs such as NewsAPI and DuckDuckGo Instant Answer API.

## How to use
* Run script ```setup.sh``` to install all required dependencies.
* Set your own API keys on the file ```apis.json```. You will need to create some accounts. All APIs used are free. Used APIs are:
    * NewsAPI
    * DuckDuckGo Instant Answer API (No API key or account needed)
    * OpenWeatherMap API
    * IPGeoLocation API
* Run script ```app.py```.
* That's it! Now by default you can use Barnaby on the address ```http://localhost:5000```.

## Endpoints
Endpoint | Description
-------- | -----------
```/```  | Shows this README
```/api_config``` | Shows API configuration.
```/assistant``` | Barnaby endpoint. ```q``` paramether is mandatory (Example: "How is the weather?"). Set ```train``` paramether to true to train the neural network (not needed, unless you make changes to it). A JSON response will be returned.