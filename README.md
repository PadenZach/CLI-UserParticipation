# CLI-UserParticipation

This project is a rather simple python script used to show a given reddit user's participation in specific subreddits.



## Installing:
To use the script, you have your own reddit API client id and client secret, as
well as a reddit account. Creation of a reddit accout is obvious and isn't covered here, but getting a client id and secret will be.

  - While logged in goto to the [apps prefrence page](https://www.reddit.com/prefs/apps/) on reddit.
  - Scroll down to bottom and click 'create another app...'.
  - Click on the 'script' radio button.
  - Enter a name and description to your liking. I suggest something descriptive
  such as "CLI-UserParticipation" and perhaps linking to the github in the desc.
  - Set the redirect URI to http://localhost:8080
  - click the button 'Create app'
  - Under 'developed applications' find the app you created and click edit, this will allow you to view your client secret. The client id is the shorter key under the 'personal use script' text.

##### Requirements:
  - python3.5 (Although other versions of 3 may work.)
  - praw
  - matplotlib
  - docopt
  If you already have python3.5+ and pip3 on your system try this command for installing the requirements via pip:

  ```
  pip3 install praw matplotlib docopt
  ```
  Note that you *may* need to run that command as sudo for it to install the module.

## Running:
  Download the main.py file and run. I suggest that you put it in it's own directory given that it will generate a json file containing your login info, client id, and client secret.
  The program stores your client information and reddit account information locally as a json file.
  This way you don't need to reenter your information each time you run the program.

  Example running command:
  ```
  python3 main.py
  ```
