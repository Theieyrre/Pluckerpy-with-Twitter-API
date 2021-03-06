# Pluckerpy with Twitter API

Pluckerpy implementation with Twitter API credentials  
Without API credentials: https://github.com/Theieyrre/Pluckerpy

## Requirements
> Python 3 ( 3.8.3)

## Install

If you have pipenv installed run to install dependencies and create virtualenv 
```
pipenv install
pipenv shell
```

To install dependencies with pip without virtualenv 
```
pip install -r requirements.txt
```

To run application
```python
python app.py |screen name|
```

Creates three files:
>followers_|screen name|.json: Followers of given user  
>friends_|screen name|.json: Friends ( people who given user follows) of given user  
>timeline_|screen name|.json: Tweets of given user

| Parameters   |      Description      |
|----------|:-------------:|
| screen_name |  [REQUIRED] Screen name of the Twitter Account |
| count |  [OPTIONAL] Total amout of tweets to get from user timeline, default: 20 |
| -k, --key |  [OPTIONAL] Twitter API Key |
| -s, --secret |  [OPTIONAL] Twitter API Secret |
| -at, --access_token |  [OPTIONAL] Twitter Accesss Token |
| -as, --access_secret |  [OPTIONAL] Twitter Accesss Secret |
| -d, --dir |  [OPTIONAL] Directory name to write outputs to, default: output|
| -v, --verbose |  Extra prints |
| --csv |  [OPTIONAL] Print in csv format |

To run application with list of names
```python
python app_big.py |JSON File with array of names|
```

Creates three files for each account:
>followers_|screen name|.json: Followers of given user  
>friends_|screen name|.json: Friends ( people who given user follows) of given user  
>timeline_|screen name|.json: Tweets of given user

| Parameters   |      Description      |
|----------|:-------------:|
| file_name |  [REQUIRED] JSON file with JSON array including screen names |
| count |  [OPTIONAL] Total amout of tweets to get from user timeline, default: 199 |
| -k, --key |  [OPTIONAL] Twitter API Key |
| -s, --secret |  [OPTIONAL] Twitter API Secret |
| -at, --access_token |  [OPTIONAL] Twitter Accesss Token |
| -as, --access_secret |  [OPTIONAL] Twitter Accesss Secret |
| -d, --dir |  [OPTIONAL] Directory name to write outputs to, default: output|
| --csv |  [OPTIONAL] Print in csv format |
| --all |  [OPTIONAL] Concatenates different users dataframes to yield three csv files instead |
| -v, --verbose |  Extra prints |

Access Token and Access Secret are necessary to run application with an authorized twitter account and callback action  
Optional parameters or .env file is necessary to run. Either one of them is enough 

To run application with list of names
```python
python location.py |Folder name of JSON Accounts|
```

Creates three files for each account:
>|Folder name|.csv accounts with locations

| Parameters   |      Description      |
|----------|:-------------:|
| folder |  [REQUIRED] Folder name of accounts |
| -k, --key |  [OPTIONAL] Twitter API Key |
| -s, --secret |  [OPTIONAL] Twitter API Secret |
| -at, --access_token |  [OPTIONAL] Twitter Accesss Token |
| -as, --access_secret |  [OPTIONAL] Twitter Accesss Secret |
| -v, --verbose |  Extra prints |

Access Token and Access Secret are necessary to run application with an authorized twitter account and callback action  
Optional parameters or .env file is necessary to run. Either one of them is enough 