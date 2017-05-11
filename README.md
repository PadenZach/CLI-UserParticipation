# CLI-UserParticipation

This project is a rather simple python script used to show a given reddit user's
participation in various subreddits.



## Installing:
To use the script, you have your own reddit API client id and client secret, as
well as a reddit account. While creation of a reddit account is obvious, and
won't be discussed here, getting a client id and secret will be.

  - While logged in goto to the [apps prefrence page](https://www.reddit.com/prefs/apps/) on reddit.
  - Scroll down to bottom and click 'create another app...'.
  - Click on the 'script' radio button.
  - Enter a name and description to your liking. I suggest something descriptive
  such as "CLI-UserParticipation" and perhaps linking to the github in the desc.
  - Set the redirect URI to http://localhost:8080
  - click the button 'Create app'
  - Under 'developed applications' find the app you just created and click edit,
  this will allow you to view your client secret. The client id is the shorter
  key under the 'personal use script' text.

##### Requirements:
  - python3.5 (Although other versions of 3 may work.)
  - praw
  - matplotlib
  If you already have python3.5+ and pip3 on your system try this command for
  installing the requirements via pip:
  ```
  pip3 install praw matplotlib
  ```
  Note that you *may* need to run that command as sudo for it to install
  correctly.
