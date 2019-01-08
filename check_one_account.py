import pwndapi

testapp = pwndapi.pwndapi("test-agent", unverified=True, truncate=True )

### examples to test the functionality
testapp.one_account(email_address="george@hotmail.com")
