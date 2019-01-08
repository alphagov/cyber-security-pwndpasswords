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
    user-agent
    '''
    def __init__(self, agent, unverified, truncate):
        self.__truncate_setting = self.__true_or_false_url_parameters("truncateResponse", truncate)
        self.__unverified_setting = self.__true_or_false_url_parameters("includeUnverified", unverified)
        self.__user_agent = agent
        self.__header = {'User-Agent': self.__user_agent}
        # starting point for all the API calls
        self.__base_url = "https://haveibeenpwned.com/api/v2"
        self.__allbreaches_url = "/breaches?"
        self.__one_account_url = "/breachedaccount/"


        logger.debug("User-agent: %s", self.__user_agent)

    def get_resource(self, urlToFetch ):

        r = requests.get(urlToFetch, headers=self.__header, verify=True)
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

    def __none_url_parameters(self, key, value):
        if value == None:
            resp = ''
        else:
            resp = "&" + key + "=" + value
        return resp

    def __true_or_false_url_parameters(self, key, value):
        if value == True:
            resp = "&"+ key+"=true"
        else:
            resp = "&" + key + "=false"
        return resp

    def __build_url(self,endpoint,params):
        url = self.__base_url + endpoint

        for param in params:
            url = url + param
            logger.debug("url is: %s", url)
        url = url + self.__truncate_setting + self.__unverified_setting
        logger.debug("url is: %s", url)

        return url

    def __validate_emailaddress(self,email_address):
        # TODO: write the validation
        return email_address

    def all_breaches(self, domain=None):
        domain = self.__none_url_parameters("domain", domain)

        url = self.__build_url(self.__allbreaches_url, [domain])
        resp = self.get_resource(url)
        # right now we're just printing this to the screen....
        print(resp)

    def one_account(self, email_address, domain=None):
        domain = self.__none_url_parameters("domain", domain)
        email = self.__validate_emailaddress(email_address)+"?"

        url = self.__build_url(self.__one_account_url, [email, domain])
        resp = self.get_resource(url)
        print(resp)


testapp = pwndapi("test-agent", unverified=True, truncate=True )

testapp.all_breaches(domain="adobe.com")
testapp.one_account(email_address="george@hotmail.com")
