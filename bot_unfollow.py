import argparse
from datetime import datetime
from dotenv import load_dotenv
import json
import os
from GithubAPIBot import GithubAPIBot

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--all", help="Unfollow all your followers")
parser.add_argument("-f", "--file", help="Followers File to Unfollow")
parser.add_argument("-m", "--max-unfollow", help="Max Number of People to Unfollow")
parser.add_argument(
    "-smin", "--sleep-min", help="Min Number of range to randomize sleep seconds between actions", action="store_true"
)
parser.add_argument(
    "-smax", "--sleep-max", help="Max Number of range to randomize sleep seconds between actions", action="store_true"
)
parser.add_argument(
    "-slmin",
    "--sleep-min-limited",
    help="Min Number of range to randomize sleep seconds when account limited",
    action="store_true",
)
parser.add_argument(
    "-slmax",
    "--sleep-max-limited",
    help="Max Number of range to randomize sleep seconds when account limited",
    action="store_true",
)
args = parser.parse_args()

sleepSecondsActionMin = int(args.sleep_min or 3)
sleepSecondsActionMax = int(args.sleep_max or 9)
sleepSecondsLimitedMin = int(args.sleep_min_limited or 90)
sleepSecondsLimitedMax = int(args.sleep_max_limited or 300)

load_dotenv()
USER = os.getenv("USER")
TOKEN = os.getenv("TOKEN")


bot = GithubAPIBot(
    USER,
    TOKEN,
    sleepSecondsActionMin,
    sleepSecondsActionMax,
    sleepSecondsLimitedMin,
    sleepSecondsLimitedMax,
    args.max_unfollow,
)


# Grab all users to unfollow from given user
if args.all:
    bot.usersToAction.extend(bot.followings)
else:
    # Grab users from given file
    if args.file:
        bot.usersToAction.extend(args.file)
    # Grab all users who already follow back
    if args.file:
        bot.usersToAction.extend(args.file)


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
