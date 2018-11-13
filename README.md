# PITM
## Parent In the Middle - A simple parental control tool using mitmproxy

### Features
It has the following functionality

* Whitelist websites
* Blacklist websites
* Profanity Filter
* Track websites visited
* Compute current session Time
* Extend the Profanity Filter by adding custom blockwords.

### To Run:

* Run `$ pip install -r requirements.txt` to setup environment.
* Go to `constants.py` and update the file paths to your local environment.
* Set the following env variables
   * `$ set FLASK_APP=server.py`
* To run the server execute `$ flask run`
