# Pluckerpy with Twitter API

Pluckerpy implementation with Twitter API credentials  
Without API credentials: https://github.com/Theieyrre/Pluckerpy

## Requirements
> Python 3 ( 3.8.3)\

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

Access Token and Access Secret are necessary to run application with an authorized twitter account and callback action  
Optional parameters or .env file is necessary to run. Either one of them is enough 
