# FEC-Data-Wranglin
get_that_data.py pulls data from FEC API to use later on ML project. (ETA? IDK)

If you want to make more than a handful of requests you need an api_key, visit https://api.open.fec.gov/developers/#/ to get a key.

You will break the program if you put anything other than a key or hitting enter for DEMO_KEY when asked for input. I'll fix it later.
And yes I know the data processing is wildly inadequate, that's on my fix-it list too.

Requires numpy and urllib.request

If you want to test it without downloading all of the FEC's data, check the Special Note in the docstring for get_the_data()

Run python3 get_that_data.py in the terminal

It ain't pretty but it works!
