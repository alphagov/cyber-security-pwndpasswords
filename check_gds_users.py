import pwndapi
import csv
import logging
import operator
import time

mylogger = logging.getLogger("patrick")
# set the log level to debug and above
mylogger.setLevel(logging.DEBUG)

# not going to log to file at the minute
#handler = logging.FileHandler('logger.log')
#handler.setLevel(logging.DEBUG)

# add the handlers to the logger
mylogger.addHandler(logging.StreamHandler())

testapp = pwndapi.pwndapi("test-agent", unverified=True, truncate=True)

### examples to test the functionality
# testapp.one_account(email_address="george@hotmail.com")

all_user_all_breaches = []
count_users_impacted = 0
count_users = 0

with open("users.csv") as f:
    reader = csv.reader(f, delimiter=" ")

    for row in reader:
        for email in row:
            mylogger.debug(email)
            count_users += 1
            response = testapp.one_account(email)
            mylogger.debug(response)
            time.sleep(1.6)
            if response == "404 - Not found - the account could not be found and has therefore not been pwned" :
                break
            else:
                count_users_impacted += 1

            for item in response:
                breached_site = (item['Name'])
                all_user_all_breaches.append(breached_site)

# count
result = dict((i, all_user_all_breaches.count(i)) for i in all_user_all_breaches)

# sort
sorted_d = sorted(result.items(), key=operator.itemgetter(1))
# logger.debug(sorted_d)

a1_sorted_keys = sorted(result, key=result.get, reverse=True)

for r in a1_sorted_keys:
    print(r, result[r])

print("Total number of employees checked: " + str(count_users))
print("Total number of employees impacted: " + str(count_users_impacted))