import requests
import logging
import json
import re
import hashlib

apilogger = logging.getLogger('pwndcheck')
apilogger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#handler = logging.FileHandler('logger.log')
#handler.setLevel(logging.DEBUG)

# create a logging format

# add the handlers to the logger
logging.getLogger().addHandler(logging.StreamHandler())

baseURL = "https://haveibeenpwned.com/api/v2"

HEADERS = {'user-agent': 'firebreak-testapp/haveibeenpwnd/ v0.1', 'api-version': 2}
range_url = 'https://api.pwnedpasswords.com/range/{}'
email_url = 'https://haveibeenpwned.com/api/v2/breachedaccount/{}'

class pwndapi():
    '''
    Mandatory parameters:
    email account to search for
    user-agent
    '''
    def __init__(self, account, agent):
        self.account = account
        self.user_agent = agent
        self.header = {'User-Agent': self.user_agent}
        logger.debug("Account: %s, User-agent: %s", self.account, self.user_agent)

    def get_resource(self, urlToFetch ):

        r = requests.get(urlToFetch, headers=self.header, verify=True)
        logger.debug("URL: %s, status:%i", urlToFetch, r.status_code)

        if r.status_code == 400:
            return fourHundredString
        elif r.status_code == 403:
            return fourOThreeString
        elif r.status_code == 404:
            return fourOFourString
        elif r.status_code == 429:
            return fourTwentyNineString
        elif r.status_code >= 500:
            return fiveHundredString
        else:
            return r.json()

    def all_breaches(self, domain=None, truncate=False, unverified=False):
        if truncate == True:
            truncate = '?truncateResponse=true'
        else:
            truncate = '?truncateResponse=false'
        if domain == None:
            domain = ''
        else:
            domain = '&domain=' + domain
        if unverified == True:
            unverified = '&includeUnverified=true'
        else:
            unverified = ''

        url = baseURL + "/breaches" + truncate + domain + unverified
        resp = self.get_resource(url)
        print(resp)


testapp = pwndapi("testapp","test-agent")

testapp.all_breaches(domain="adobe.com",unverified=False,truncate=True)
