import pwndapi
import csv
import logging

logger = logging.getLogger(__name__)
# set the log level to debug and above
logger.setLevel(logging.DEBUG)

# not going to log to file at the minute
#handler = logging.FileHandler('logger.log')
#handler.setLevel(logging.DEBUG)

# add the handlers to the logger
logging.getLogger().addHandler(logging.StreamHandler())

testapp = pwndapi.pwndapi("test-agent", unverified=True, truncate=True)

### examples to test the functionality
# testapp.one_account(email_address="george@hotmail.com")


with open("users.csv") as f:
    reader = csv.reader(f, delimiter=" ")
    for row in reader:
        for email in row:
            print(email)
            response = testapp.one_account(email)
            print(response)
