import pwndapi as pwndapi

testapp = pwndapi.pwndapi("test-agent", unverified=True, truncate=True )

### examples to test the functionality
testapp.test_password("999999")