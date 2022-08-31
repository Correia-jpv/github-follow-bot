<h2>GitHub Follow Bot</h2>&nbsp;<img align="right" width="35%" src="logo.png">

<h2> Table of Contents</h2>

- [Disclaimer](#disclaimer)
- [Getting Started](#getting-started)
	- [Install Requirements](#install-requirements)
	- [Authenticate](#authenticate)
		- [Get a GitHub Personal Access Token](#get-a-github-personal-access-token)
		- [Add your GitHub username and PAT to `.env` file](#add-your-github-username-and-pat-to-env-file)
- [How to Use](#how-to-use)
	- [Follow](#follow)
		- [Target user's followers](#target-users-followers)
		- [Followers of the most popular users from a country](#followers-of-the-most-popular-users-from-a-country)
		- [From a file](#from-a-file)
	- [Unfollow](#unfollow)
		- [All](#all)
		- [Followers](#followers)
		- [Non-followers](#non-followers)
		- [From a file](#from-a-file-1)
	- [Options](#options)
		- [Maximum follows/unfollows](#maximum-followsunfollows)
		- [Speed](#speed)
- [Future Implementation](#future-implementation)
- [Contributing](#contributing)
- [Resources](#resources)

## Disclaimer

**This is a PoC and was developed for educational purposes only. You may get your account banned. Use at your own risk.**

> ### Spam and Inauthentic Activity on GitHub
> Automated excessive bulk activity and coordinated inauthentic activity, such as spamming, are prohibited on GitHub. Prohibited activities include:
> - (...)
> - inauthentic interactions, such as fake accounts and automated inauthentic activity
> - rank abuse, such as automated starring or following

[From GitHub Acceptable Use Policies](https://docs.github.com/en/github/site-policy/github-acceptable-use-policies#4-spam-and-inauthentic-activity-on-github)

## Getting Started

### Install Requirements

```
pip install -r requirements.txt
```

### Authenticate

#### Get a GitHub Personal Access Token

Make sure to enable the `user` scope and all subscopes inside of that permission.

[How to get your GitHub PAT](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)

#### Add your GitHub username and PAT to `.env` file

Create a `.env` file on the project's root directory or edit `.env.sample` (rename to `.env`) and add your username and PAT.
```
GITHUB_USER=YOUR_GITHUB_USERNAME
TOKEN=YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
```

## How to Use

### Follow

#### Target user's followers
```
python bot_follow.py -t <TARGET_USER>
```
#### Followers of the most popular users from a country
([list of valid countries](https://github.com/gayanvoice/top-github-users#readme))
```
python bot_follow.py -p <COUNTRY_NAME>
```
#### From a file
Follow users from a pre-generated file (JSON)
```
python bot_follow.py -f <FILENAME>
```

### Unfollow

note: Unfollow order is FIFO, as in the most recently followed user will be the last to be unfollowed.

#### All
Unfollow all your followings
```
python bot_unfollow.py -a
```
#### Followers
Only unfollow users who already follow you
```
python bot_unfollow.py -fo
```
#### Non-followers
Only unfollow users who don't follow you back
```
python bot_unfollow.py -nf
```
#### From a file
Unfollow users from a pre-generated file (JSON)
```
python bot_unfollow.py -f <FILENAME>
```

### Options

#### Maximum follows/unfollows
Set the maximum number of follow/unfollow actions
```
-m 300
```

#### Speed

A random delay (in seconds) is performed after follow/unfollow actions or when the account is rate limited.
You can change these delays to your liking with the following arguments:

- Minimum delay between actions
	```
	-smin 20
	```
- Maximum delay between actions
	```
	-smax 120
	```
- Minimum delay when rate limited
	```
	-slmin 600
	```
- Maximum delay when rate limited
	```
	-slmin 1500
	```

## Future Implementation

- Schedule - Bot only performs actions between set time and sleeps after off-schedule
- Max follow per source - Follow max `n` per popular user
- Add follow source - Follow users per topic
- Add follow source - Grab followers from users listed in a file
- Email followed users - Send an email to followed users with templates (colaboration, follow back or custom)
- Star `n` repositories of followed users

## Contributing

Contributions are welcome! Read the [contribution guidelines](https://github.com/Correia-jpv/.github/blob/main/CONTRIBUTING.md#contributing) first.

Wish there was another feature? Feel free to open an [feature request issue](/../../issues/new?assignees=Correia-jpv&labels=enhancement&template=feature-request.md&title=%5BREQUEST%5D) with your suggestion!

If you find a bug, kindly open an [bug report issue](/../../issues/new?assignees=Correia-jpv&labels=bug&template=bug_report.md&title=%5BBUG%5D) as described in the contribution guidelines.

## Resources

- [GitHub API](https://docs.github.com/en/rest)
- [Top GitHub Users By Country](https://github.com/gayanvoice/top-github-users)
- [GitHub-Follow-Bot](https://github.com/TheDarkAssassins/Github-Follow-Bot)
