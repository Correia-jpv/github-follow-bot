import argparse
from datetime import datetime
from dotenv import load_dotenv
import json
import os
from GithubAPIBot import GithubAPIBot

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--all", help="Unfollow all your followings", action="store_true")
parser.add_argument("-fo", "--followers", help="Only unfollow users who already follow you", action="store_true")
parser.add_argument("-nf", "--non-followers", help="Only unfollow users who don't follow you back", action="store_true")
parser.add_argument("-f", "--file", help="File with usernames to Unfollow")
parser.add_argument("-m", "--max-unfollow", help="Max Number of People to Unfollow")
parser.add_argument("-smin", "--sleep-min", help="Min Number of range to randomize sleep seconds between actions")
parser.add_argument("-smax", "--sleep-max", help="Max Number of range to randomize sleep seconds between actions")
parser.add_argument(
    "-slmin", "--sleep-min-limited", help="Min Number of range to randomize sleep seconds when account limited"
)
parser.add_argument(
    "-slmax", "--sleep-max-limited", help="Max Number of range to randomize sleep seconds when account limited"
)
parser.add_argument("-sh", "--sleep-hour", help="Hour for the bot to go to sleep")
parser.add_argument("-sm", "--sleep-minute", help="Minute for the bot to go to sleep")
parser.add_argument("-st", "--sleep-time", help="Total time (in hours) for the bot to sleep")
args = parser.parse_args()

sleepSecondsActionMin = int(args.sleep_min or 3)
sleepSecondsActionMax = int(args.sleep_max or 9)
sleepSecondsLimitedMin = int(args.sleep_min_limited or 90)
sleepSecondsLimitedMax = int(args.sleep_max_limited or 300)

load_dotenv()
USER = os.getenv("GITHUB_USER")
TOKEN = os.getenv("TOKEN")


bot = GithubAPIBot(
    USER,
    TOKEN,
    sleepSecondsActionMin,
    sleepSecondsActionMax,
    sleepSecondsLimitedMin,
    sleepSecondsLimitedMax,
    args.sleep_hour,
    args.sleep_minute,
    args.sleep_time,
    args.max_unfollow,
)


# Grab all following users
if args.all:
    bot.usersToAction.extend(bot.followings)
else:
    # Grab following users from given file
    if args.file:
        with open(args.file, "r+") as file:
            try:
                fileUsers = json.load(file)
            except:
                raise ValueError("\n JSON file is in incorrect format.")
            followedFileUsers = [v for v in bot.followings if v in fileUsers]
            bot.usersToAction.extend(followedFileUsers)

    # Grab following users who are followers
    if args.followers:
        bot.getFollowers(following=True)

    # Grab following users who aren't followers
    if args.non_followers:
        bot.getFollowers(following=True)
        nonFollowersFollowings = [v for v in bot.followings if v not in bot.usersToAction]
        bot.usersToAction.extend(nonFollowersFollowings)


# Write users to be unfollowed to file
filename = (
    "./logs/"
    + str(datetime.now().strftime("%m-%d-%Y__%H-%M"))
    + "__"
    + str(len(bot.usersToAction))
    + "-unfollowed-users.json"
)
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w+") as f:
    json.dump(bot.usersToAction, f, indent=4)

bot.unfollow()
