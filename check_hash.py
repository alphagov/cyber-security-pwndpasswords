import pwndapi
testapp = pwndapi.pwndapi("test-agent", unverified=True, truncate=True )

testapp.get_passwords("21BD1")
