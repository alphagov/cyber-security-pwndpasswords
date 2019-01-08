import requests
import logging
import json
import re
import hashlib

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create a logger
logger = logging.getLogger(__name__)
# set the log level to debug and above
logger.setLevel(logging.DEBUG)

# not going to log to file at the minute
#handler = logging.FileHandler('logger.log')
#handler.setLevel(logging.DEBUG)


# add the handlers to the logger
logging.getLogger().addHandler(logging.StreamHandler())

# starting point for all the API calls
baseURL = "https://haveibeenpwned.com/api/v2"

# human readable error strings
fourHundredString = "400 - Bad request - the account does not comply with an acceptable format (i.e. it's an empty string)"
fourOThreeString = "403 - Forbidden - no user agent has been specified in the request"
fourOFourString = "404 - Not found - the account could not be found and has therefore not been pwned"
fourTwentyNineString = "Rate limit exceeded, refer to acceptable use of the API: https://haveibeenpwned.com/API/v2#AcceptableUse"
fiveHundredString = "A server error occurred on haveibeenpwned.com. Please try again later."
emailFormatString = "The provided string is not an email address"

# instance of the pwndapi class that does all of the API work
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
        # right now we're just printing this to the screen....
        print(resp)

    def one_account(self, email_address):

        url = baseURL + "/breachedaccount/"+email_address+"?truncateResponse=true"
        resp = self.get_resource(url)
        print(resp)


testapp = pwndapi("testapp","test-agent")

#testapp.all_breaches(domain="adobe.com",unverified=False,truncate=False)
testapp.one_account("msivorn@gmail.com")
