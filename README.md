# This is a helper to click on 'Enroll Now' button on your wishlist from WebReg account
# pre-request:
#   java 17
#   python 3.12
#   selenium driver 133.0
# download chromedriver from https://googlechromelabs.github.io/chrome-for-testing/
# Prepare pip dependencies

The easiest way is to use following commands:

```bash
#python 3
python3 -m venv env

source venv/bin/activate
pip install selenium
```

steps:

1. find your target program number:
    - login to webreg website
    - find your desire program and go into the detail page.
    - it's part of url on the program details page, eg url: https://anc.ca.apm.activecommunities.com/burnaby/activity/search/detail/58049
    - number is 58049
2. cd webreg
3. python webreg.py 
    --username <login email address> 
    --name <Person's Name to register>, eg: "Simon Cui" 
    --number <program number>, eg: 58049
    --refresh (optional) only if want to wait for the avaiable spot 
    --dryrun (optional) only for debugging