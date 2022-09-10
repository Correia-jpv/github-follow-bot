from base64 import b64encode
import datetime
import random
import requests
from requests.adapters import HTTPAdapter
import time
from tqdm import tqdm
from urllib.parse import parse_qs
from urllib.parse import urlparse
from urllib3.util import Retry


class GithubAPIBot:
    # Constructor
    def __init__(
        self,
        username: str,
        token: str,
        sleepSecondsActionMin: int,
        sleepSecondsActionMax: int,
        sleepSecondsLimitedMin: int,
        sleepSecondsLimitedMax: int,
        sleepHour=None,
        sleepMinute=None,
        sleepTime=None,
        maxAction=None,
    ):
        if not isinstance(username, str):
            raise TypeError("Missing/Incorrect username")
        if not isinstance(token, str):
            raise TypeError("Missing/Incorrect token")

        self.__username = username
        self.__token = token
        self.__sleepSecondsActionMin = sleepSecondsActionMin
        self.__sleepSecondsActionMax = sleepSecondsActionMax
        self.__sleepSecondsLimitedMin = sleepSecondsLimitedMin
        self.__sleepSecondsLimitedMax = sleepSecondsLimitedMax
        self.__sleepHour = sleepHour
        self.__sleepMinute = sleepMinute
        self.__sleepTime = sleepTime
        self.__maxAction = maxAction
        self.__usersToAction = []
        self.__followings = []

        # Requests' headers
        HEADERS = {
            "Authorization": "Basic " + b64encode(str(self.token + ":" + self.token).encode("utf-8")).decode("utf-8")
        }

        # Session
        self.session = requests.session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.headers.update(HEADERS)

        # Authenticate
        try:
            res = self.session.get("https://api.github.com/user")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        if res.status_code == 404:
            raise ValueError("\nFailure to Authenticate, please check Personal Access Token and Username!")
        else:
            print("\nSuccessful authentication.")

        self.getFollowings()

    # Getters & Setters
    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value

    @property
    def sleepSecondsActionMin(self):
        return self.__sleepSecondsActionMin

    @sleepSecondsActionMin.setter
    def sleepSecondsActionMin(self, value):
        self.__sleepSecondsActionMin = value

    @property
    def sleepSecondsActionMax(self):
        return self.__sleepSecondsActionMax

    @sleepSecondsActionMax.setter
    def sleepSecondsActionMax(self, value):
        self.__sleepSecondsActionMax = value

    @property
    def sleepSecondsLimitedMin(self):
        return self.__sleepSecondsLimitedMin

    @sleepSecondsLimitedMin.setter
    def sleepSecondsLimitedMin(self, value):
        self.__sleepSecondsLimitedMin = value

    @property
    def sleepSecondsLimitedMax(self):
        return self.__sleepSecondsLimitedMax

    @sleepSecondsLimitedMax.setter
    def sleepSecondsLimitedMax(self, value):
        self.__sleepSecondsLimitedMax = value

    @property
    def sleepHour(self):
        return self.__sleepHour

    @sleepHour.setter
    def sleepHour(self, value):
        self.__sleepHour = value

    @property
    def sleepMinute(self):
        return self.__sleepMinute

    @sleepMinute.setter
    def sleepMinute(self, value):
        self.__sleepMinute = value

    @property
    def sleepTime(self):
        return self.__sleepTime

    @sleepTime.setter
    def sleepTime(self, value):
        self.__sleepTime = value

    @property
    def maxAction(self):
        return self.__maxAction

    @maxAction.setter
    def maxAction(self, value):
        self.__maxAction = value

    @property
    def usersToAction(self):
        return self.__usersToAction

    @usersToAction.setter
    def usersToAction(self, value):
        self.__usersToAction = value

    @property
    def followings(self):
        return self.__followings

    @followings.setter
    def followings(self, value):
        self.__followings = value

    def getUsers(self, url="", maxAction=None, following=False):
        users = []

        try:
            res = self.session.get(url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        # Get usernames from each page
        page = 1
        while True:
            try:
                res = self.session.get(url + "?page=" + str(page)).json()
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)

            for user in res:
                # Check if we already have enough usernames
                if maxAction != None:
                    if len(users) >= int(maxAction):
                        break

                # Add username if it's not being followed already
                if (
                    not following
                    and not (user["login"] in self.followings)
                    or following
                    and (user["login"] in self.followings)
                ):
                    users.append(user["login"])

            # Check if we already have enough usernames
            if maxAction != None:
                if len(users) >= int(maxAction):
                    break

            if res == []:
                break
            else:
                page += 1
        
        return users

    def getFollowers(self, username=None, following=None):
        if username == None:
            username = self.username
        print(f"\nGrabbing {username}'s followers.\n")
        self.usersToAction.extend(
            self.getUsers(
                url=f"https://api.github.com/users/{username}/followers",
                maxAction=self.maxAction,
                following=following,
            )
        )

    def getFollowings(self, username=None):
        if username == None:
            username = self.username
        print(f"\nGrabbing {username}'s followings.\n")
        self.followings.extend(self.getUsers(url=f"https://api.github.com/users/{username}/following"))

    def run(self, action):
        if len(self.usersToAction) == 0:
            print(f"Nothing to {action}")
        else:

            # Users to follow/unfollow must not exceed the given max
            if self.maxAction != None:
                self.usersToAction = self.usersToAction[: min(len(self.usersToAction), int(self.maxAction))]

            # Time for the bot to go to sleep
            if self.sleepHour != None and self.sleepMinute != None and self.sleepTime != None:
                sleepTime = nextSleepTime(int(self.__sleepHour), int(self.sleepMinute))

            # Start follow/unfollow
            print(f"\nStarting to {action}.\n")
            users = tqdm(
                self.usersToAction,
                initial=1,
                dynamic_ncols=True,
                smoothing=True,
                bar_format="[PROGRESS] {n_fmt}/{total_fmt} |{l_bar}{bar}|",
                position=0,
                leave=False,
            )
            for user in users:
                
                # Set the bot to sleep at the set time
                if self.sleepHour != None and self.sleepMinute != None and self.sleepTime != None:
                    timeNow = datetime.datetime.now()
                    if timeNow.timestamp() > sleepTime.timestamp():
                        sleepTime = nextSleepTime(int(self.__sleepHour), int(self.__sleepMinute))
                        timeNow += datetime.timedelta(hours=int(self.__sleepTime))
                        sleepUntil(timeNow.hour, random.randint(0, 59))

                # Follow/unfollow user
                try:
                    if action == "follow":
                        res = self.session.put(f"https://api.github.com/user/following/{user}")
                    else:
                        res = self.session.delete(f"https://api.github.com/user/following/{user}")
                except requests.exceptions.RequestException as e:
                    raise SystemExit(e)

                # Unsuccessful
                if res.status_code != 204:
                    sleepSeconds = random.randint(self.sleepSecondsLimitedMin, self.sleepSecondsLimitedMax)
                # Successful
                else:
                    sleepSeconds = random.randint(self.sleepSecondsActionMin, self.sleepSecondsActionMax)

                # Sleep
                sleepSecondsObj = list(range(0, sleepSeconds))
                sleepSecondsBar = tqdm(
                    sleepSecondsObj,
                    dynamic_ncols=True,
                    smoothing=True,
                    bar_format="[SLEEPING] {n_fmt}s/{total_fmt}s |{l_bar}{bar}|",
                    position=1,
                    leave=False,
                )
                for second in sleepSecondsBar:
                    time.sleep(1)

            print(f"\n\nFinished {action}ing!")

    def follow(self):
        self.run("follow")

    def unfollow(self):
        self.run("unfollow")

def nextSleepTime(hour, minute):
    timeNow = datetime.datetime.now()
    future = datetime.datetime(timeNow.year, timeNow.month, timeNow.day, hour, minute)

    if timeNow.timestamp() > future.timestamp():
        future += datetime.timedelta(days=1)
    return future

def sleepUntil(hour, minute):
    t = datetime.datetime.today()
    future = datetime.datetime(t.year, t.month, t.day, hour, minute)

    if t.timestamp() >= future.timestamp():
        future += datetime.timedelta(days=1)
    
    print(f'\nSleeping... Waking up at {future.hour}:{future.minute}')
    
    sleepSeconds = int((future-t).total_seconds())
    sleepSecondsObj = list(range(0, sleepSeconds))
    sleepSecondsBar = tqdm(
        sleepSecondsObj,
        dynamic_ncols=True,
        smoothing=True,
        bar_format="[SLEEPING] {n_fmt}s/{total_fmt}s |{l_bar}{bar}|",
        position=2,
        leave=False,
    )
    for second in sleepSecondsBar:
        time.sleep(1)

    print(f'\nWaking up...')