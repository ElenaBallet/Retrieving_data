#!/usr/local/bin/python3
import sys
from google.ads.googleads.client import GoogleAdsClient
 
def google_ads_authentication(cred_dict):
    try:
        client = GoogleAdsClient.load_from_dict(cred_dict)
 
        print("\nАутификация в Google Ads успешно пройдена")
        return client
 
    except:
        print("\nАутификация в Google Ads не пройдена")