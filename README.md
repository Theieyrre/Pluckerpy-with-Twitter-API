# Pluckerpy with Twitter API

Pluckerpy implementation with Twitter API credentials  
Without API credentials: https://github.com/Theieyrre/Pluckerpy

To run application
```python
python app.py <screen name>
```

Creates three files:
>followers_<screen name>.json: Followers of given user  
>friends_<screen name>.json: Friends ( people who given user follows) of given user  
>timeline_<screen name>.json: Tweets of given user

| Parameters   |      Description      |
|----------|:-------------:|
| screen_name |  [REQUIRED] Screen name of the Twitter Account |
| count |  [OPTIONAL] Total amout of tweets to get from user timeline, default: 20 |
| -k, --key |  [OPTIONAL] Twitter API Key |
| -s, --secret |  [OPTIONAL] Twitter API Secret |
| -at, --access_token |  [OPTIONAL] Twitter Accesss Token |
| -as, --access_secret |  [OPTIONAL] Twitter Accesss Secret |

Access Token and Access Secret are necessary to run application without an authorized twitter account and callback action  
Optional parameters or .env file is necessary to run. Either one of them is enough 
