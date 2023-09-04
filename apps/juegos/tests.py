from django.test import TestCase
import requests,os,json


CLIENT_ID=os.environ.get('IDCLIENTE')
SECRETO=os.environ.get('CLIENT_SECRET')

# https://id.twitch.tv/oauth2/token?client_id=abcdefg12345&client_secret=hijklmn67890&grant_type=client_credentials

r=requests.post("https://id.twitch.tv/oauth2/token",data={"client_id":CLIENT_ID,"client_secret":SECRETO,"grant_type":"client_credentials"})
res=json.loads(r.text)
print(res)