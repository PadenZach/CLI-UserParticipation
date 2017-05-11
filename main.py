import praw
import prawcore
import json
import matplotlib.pyplot as plt

class LoginSession(object):
    """ Class to hand praw authentication and store reddit object
        Attributes:
            reddit - a praw.reddit instance
    """


    def __init__(self):
        try:
            loginInfo = self.getLoginInfo()
        except FileNotFoundError:
            print('No login info found, generating new info: ')
            loginInfo = self.genUserInfo()

        try:
            self.reddit = self.login(loginInfo)
        except praw.exceptions.ClientException: #or invalid loginInfo
            print('Login Failed. Trying to reset login info...')
            loginInfo = self.genUserInfo()
        except praw.exceptions.APIException as err:
            print('Looks like somethings wrong with reddit. Try again later.')
            print(err.error_type)
            print(err.message)

    def jsonLoginInfo(self, loginInfo):
        f = open('loginInfo.json', 'w')
        json.dump(loginInfo, f)
        f.close()

    def getLoginInfo(self):
        f = open('loginInfo.json', 'r')
        loginInfo = json.load(f)
        return loginInfo

    def genUserInfo(self):
        loginInfo = []
        loginInfo.append(input("Enter client_id: "))
        loginInfo.append(input("Enter client secret: "))
        loginInfo.append(input("Enter username: "))
        loginInfo.append(input("Enter password: "))
        loginInfo.append("python3:cliUpvoteSearch:0.1:{}".format(loginInfo[2]))
        self.jsonLoginInfo(loginInfo)
        return loginInfo

    def login(self, loginInfo):
        return praw.Reddit(
            client_id=loginInfo[0],
            client_secret=loginInfo[1],
            password=loginInfo[3],
            user_agent=loginInfo[4],
            username=loginInfo[2]
        )


def findUserActivity(reddit, user):
    """
    Params:
        reddit - a praw reddit instance
        user - a username string.
    Returns:
        A dictionary with subreddit-frequency items.

    Uses praw to get a given user's recent comments and submissions. 'Recently'
    as in there previous 60 comments and submissions.
    """
    subFrequency = {}
    for comment in  praw.models.Redditor(reddit, user).comments.new(limit = 60):
        if comment.subreddit in subFrequency:
            subFrequency[comment.subreddit.display_name] += 1
        else:
            subFrequency[comment.subreddit.display_name] = 1

    for comment in  praw.models.Redditor(reddit, user).submissions.new(limit = 60):
        if comment.subreddit in subFrequency:
            subFrequency[comment.subreddit.display_name] += 1
        else:
            subFrequency[comment.subreddit.display_name] = 1

    return subFrequency

def generateActivityDisplay(userActivity):
    """
    Params:
        userActivity - a dictionary with subreddit-frequency items.
    Uses matplotlib to plot user activity as a pie chart.
    """

    lists = sorted(userActivity.items())
    keys, values = zip(*lists)
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels = keys, autopct='%1.1f%%')
    ax1.axis('equal')
    plt.show()

reddit = LoginSession().reddit
user = None
print('Enter a blank username to quit')

while user != '':
    user = input("Enter username to parse: ")
    try:
        generateActivityDisplay(findUserActivity(reddit, user))
    except TypeError:
        print("Thanks for using CLI-UserParticipation")
        quit()
    except prawcore.exceptions.NotFound:
        print("{} doesn't appear to exist. Please Try again".format(user))
