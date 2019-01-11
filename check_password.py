import pwndapi as pwndapi

testapp = pwndapi.pwndapi("test-agent", unverified=True, truncate=True )

### examples to test the functionality
print(testapp.test_password("password123"))