import basic

settings = basic._TEST_SETTINGS
#settings = basic._LIVE_SETTINGS
print basic.listEventTypes(settings)
print basic.listInPlayEvents(settings, 1)
