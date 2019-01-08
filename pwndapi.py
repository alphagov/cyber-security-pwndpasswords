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

# instance of the pwndapi class that does all of the API work
class pwndapi():
    # human readable error strings
    fourHundredString = "400 - Bad request - the account does not comply with an acceptable format (i.e. it's an empty string)"
    fourOThreeString = "403 - Forbidden - no user agent has been specified in the request"
    fourOFourString = "404 - Not found - the account could not be found and has therefore not been pwned"
    fourTwentyNineString = "Rate limit exceeded, refer to acceptable use of the API: https://haveibeenpwned.com/API/v2#AcceptableUse"
    fiveHundredString = "A server error occurred on haveibeenpwned.com. Please try again later."
    emailFormatString = "The provided string is not an email address"
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
        self.__allbreaches_url = "https://haveibeenpwned.com/api/v2/breaches?"
        self.__one_account_url = "https://haveibeenpwned.com/api/v2/breachedaccount/"
        self.__pastes_account_url = "https://haveibeenpwned.com/api/v2/pasteaccount/"
        self.__password_hash_url = "https://api.pwnedpasswords.com/range/"

        logger.debug("User-agent: %s", self.__user_agent)

    def get_resource(self, urlToFetch ):

        r = requests.get(urlToFetch, headers=self.__header, verify=True)
        logger.debug("URL: %s, status:%i", urlToFetch, r.status_code)
        logger.debug(r.headers.get('content-type'))

        resp = ""
        if r.status_code == 200:
            logger.info("successful request... ")
            content_type = r.headers.get('content-type')
            if content_type == "text/plain":
                try:
                    resp = r.text
                except:
                    resp = "couldn't load remote page content"
            elif "application/json" in content_type:
                try:
                    resp = r.json()
                except json.JSONDecodeError:
                    resp = "couldn't load json"
        elif r.status_code == 400:
            resp = fourHundredString
        elif r.status_code == 403:
            resp = fourOThreeString
        elif r.status_code == 404:
            resp = fourOFourString
        elif r.status_code == 429:
            resp = fourTwentyNineString
        elif r.status_code >= 500:
            resp = fiveHundredString
        logger.debug("response: %s",  resp[:50])

        # return the response, whatever it is
        return resp

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

    def __build_url(self, endpoint, params, append_filters=True):
        url = endpoint

        for param in params:
            url = url + param

        if append_filters:
            url = url + self.__truncate_setting + self.__unverified_setting

        logger.debug("url is: %s", url)

        return url

    def __validate_emailaddress(self,email_address):
        # TODO: write the validation
        return email_address

    def __validate_password_hash(self, hash):
        return hash

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

    def get_pastes(self, email_address):
        email = self.__validate_emailaddress(email_address) + "?"
        url = self.__build_url(self.__pastes_account_url, [email])
        resp = self.get_resource(url)
        print(resp)

    def get_passwords(self, password_hash):
        hash  =self.__validate_password_hash(password_hash)
        url = self.__build_url(self.__password_hash_url, [hash], append_filters=False)
        resp = self.get_resource(url)
        print(resp)

    def test_password(self, password):
        '''
        See how many times a given password is owned... note that pwntpasswords only
        uses the first 5 characters, so it's not an exact match
        '''
        hash_object = hashlib.sha1(bytes(password, encoding='utf-8'))

        hex_digest = hash_object.hexdigest()
        hex_digest = hex_digest.upper()
        hash = hex_digest[:5]

        pnum = 0
        url = self.__build_url(self.__password_hash_url, [hash], append_filters=False)
        resp = self.get_resource(url)

        # response: hash, count
        data = resp.splitlines()
        print(data)
        for item in data:
            if item[0:35] == hex_digest[5:]:
                pnum = item[36:]
        logger.debug("password has been owned this many times: %i", int(pnum))

#testapp = pwndapi("test-agent", unverified=True, truncate=True )

### examples to test the functionality
#testapp.all_breaches(domain="ashleymadison.com")
#testapp.one_account(email_address="george@hotmail.com")
#testapp.get_pastes("george@hotmail.com")
#testapp.get_passwords("21BD1")
#testapp.test_password("999999")
