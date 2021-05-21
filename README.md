# Discord-Bot-Codedrills
Discord bot for practicing cp-problems with your friends

# Instructions for adding the bot to your server

1. Create a bot account from, https://discord.com/developers/applications and give it general chat and message priviliges.
2. Change the TOKEN in .env file to your bot's token.
3. Make sure to delete the contents of 'contests' folder.
4. Host the bot on replit.
5. Add bot to your server.

# Commands/Features
Use these commands in the text channel to interact with the bot
1. !add _username_ : add user (must be a valid codeforces handle)
2. !all : shows list of all users
3. !topics : shows list of topics
4. !start _topicname_ : Start a contest of 10 problems from the topic
5. !lb _ID_ : display the leaderboard for the contest(running/previous) with the given ID. (ID of the contest is displayed by the bot in !start)
6. !end : end the ongoing contest
7. !prob _ID_: display the problem-set of the contest with given ID.(running/previous)


The data-base is stored in contests folder
