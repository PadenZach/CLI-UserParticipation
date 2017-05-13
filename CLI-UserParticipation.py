"""CLI-UserParticipation.

Usage:  CLI-UserParticipation.py --help
        CLI-UserParticipation.py <username> [-s | --simple] [-d | --differ]
        CLI-UserParticipation.py --config | -c

Options:
    --help         Show this screen.
    -c --config    Configure client id and account information.
    -s --simple    Display ASCII style graphs instead of matplotlib.
    -d --differ    Break up participation graphs by type of participation.
"""

# TODO (zpaden) Implement option to try to count upvotes for participation
# TODO (zpaden) Implement option to display types of participation seperately
# TODO (zpaden) Implement ASCII graphs as an option in place of matplotlib
# TODO (zpaden) Consider changing LoginSession, does it need to be an Object?
# TODO (zpaden) Work with 'bad' path and improve error handling.

import os
import praw
import prawcore
import docopt
import json
import getpass
import matplotlib.pyplot as plt


class LoginSession(object):
    """Class to hand praw authentication and store reddit object.

    Attributes:
            reddit - a praw.reddit instance
    """

    def __init__(self):
        """__init__ method for LoginSession.

        Will try to load pre-existing json config, if not will run prompt for
        configuring the client information.

        Params:
            -self
        """
        try:
            loginInfo = self.getLoginInfo()
        except FileNotFoundError:
            print('No login info found, generating new info: ')
            loginInfo = self.genUserInfo()

        try:
            self.reddit = self.login(loginInfo)
        except praw.exceptions.ClientException:  # or invalid loginInfo
            print('Login Failed. Trying to reset login info...')
            loginInfo = self.genUserInfo()
        except praw.exceptions.APIException as err:
            print('Looks like somethings wrong with reddit. Try again later.')
            print(err.error_type)
            print(err.message)

    def jsonLoginInfo(self, loginInfo):
        """Dump logininfo to json.

        Params:
            -loginInfo: list of client and account information.
            -self: as this is a class method.
        """
        f = open('loginInfo.json', 'w')
        json.dump(loginInfo, f)
        f.close()

    def getLoginInfo(self):
        """Get loginInfo from local json file.

        Params:
            -self: as this is a class method

        Returns:
            list containing loginInfo
        """
        f = open('loginInfo.json', 'r')
        loginInfo = json.load(f)
        return loginInfo

    def genUserInfo(self):
        """Generate user info, and save to json.

        Params:
            -self: as this is a class method.
        """
        loginInfo = []
        loginInfo.append(input("Enter client_id: "))
        loginInfo.append(input("Enter client secret: "))
        loginInfo.append(input("Enter username: "))
        loginInfo.append(getpass.getpass())
        loginInfo.append(
            "python3:CLI-UserParticipation:0.2:{}".format(loginInfo[2]))
        self.jsonLoginInfo(loginInfo)

        print("User info generated! :)")
        return loginInfo

    def login(self, loginInfo):
        """Login with given loginInfo.

        Params:
        -self: as this is a class method.
        -loginInfo: List of client and account information.

        Returns:
        praw.Reddit object.
        """
        return praw.Reddit(
            client_id=loginInfo[0],
            client_secret=loginInfo[1],
            password=loginInfo[3],
            user_agent=loginInfo[4],
            username=loginInfo[2]
        )


def findUserActivity(reddit, user):
    """Use praw API to fetch and record all types of user participation.

    Params:
        reddit - a praw reddit instance
        user - a username string.
    Returns:
        A dictionary with subreddit-frequency items.

    Uses praw to get a given user's recent comments and submissions. 'Recently'
    as in there previous 60 comments and submissions.
    """
    subFrequency = {}
    for comment in praw.models.Redditor(reddit, user).comments.new(limit=60):
        if comment.subreddit in subFrequency:
            subFrequency[comment.subreddit.display_name] += 1
        else:
            subFrequency[comment.subreddit.display_name] = 1

    for comment in praw.models.Redditor(reddit, user).submissions.new(
            limit=60):
        if comment.subreddit in subFrequency:
            subFrequency[comment.subreddit.display_name] += 1
        else:
            subFrequency[comment.subreddit.display_name] = 1

    return subFrequency


def generateActivityDisplay(userActivity):
    """Given user activity, Generate graph to display it via matplotlib.

    Params:
        userActivity - a dictionary with subreddit-frequency items.
    Uses matplotlib to plot user activity as a pie chart.
    """
    lists = sorted(userActivity.items())
    keys, values = zip(*lists)
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=keys, autopct='%1.1f%%')
    ax1.axis('equal')
    plt.show()


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    if args['--differ'] is True or args['--simple'] is True:
        print("This/These options are not implemented. Ignoring.")
    if args['--config'] is True:
        try:
            os.remove('loginInfo.json')
        except FileNotFoundError:
            pass
        LoginSession()
    if args['<username>'] is not None:
        reddit = LoginSession().reddit
        try:
            generateActivityDisplay(
                findUserActivity(reddit, args['<username>']))
        except TypeError:
            print("Thanks for using CLI-UserParticipation")
            quit()
        except prawcore.exceptions.NotFound:
            print("{} doesn't appear to exist. Please Try again".format(
                args['<username>']))
