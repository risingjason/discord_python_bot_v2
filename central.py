#!/usr/bin/env python

#AUTHOR: Jason Yatfai Zhang
#GITHUB: risingjason

import discord
import asyncio
import enum
import os
import sys
from os.path import getmtime

#NEW UPDATE TO DISCORD NO LONGER ALLOWS BOT TO BE LOGGED IN THROUGH EMAIL AND PASSWORD
#Copy and paste your bot's token into infos.txt
#Bot tokens are obtained through the Discord Developer website
fp_token = open("token.txt", "r")
token = fp_token.read()
fp_token.close()

client = discord.Client()

online_message = "`Bot v2.0 Currently in Development`"

# added text channels filter list to avoid spamming multiple text channels
allowed_text_channels = ["93456386729451520", "169666525404463105"]

@client.event
async def on_ready():
	print("Bot is running as the user '{}'".format(client.user.name))
	channel = client.get_all_channels()
	for channel in client.get_all_channels():
		if channel.type is discord.ChannelType.text: #notifies all registered text channels that the bot is online
			if channel.id in allowed_text_channels:
				#utf-8 compatibility paste .encode("utf-8") after channel.name
				print("Bot is running on server: {}, name: {}, id: {}, type: {}".format(channel.server, channel.name, channel.id, channel.type))
			
				#if channel.name == "general": # use this to only send to specifil text channels
				# prints a Bot Online status too all text channels in every server
				await client.send_message(channel, online_message)

@client.event
async def on_message(msg):
	cmds = msg.content.split(' ') # seperates the message word by word
	cmd = cmds[0].lower() # takes the first word (most commands are called using the first word of message)
	mentions = msg.raw_mentions

	#waits for any of the commands in core to be called upon
	#if cmd in core.commands:
	#	await core.commands[cmd](client, msg, cmds)

print("Starting bot...")
client.run(token)

# does not work. find another way
# allows bot to restart after any of the listed files are updated
# WATCHED_FILES = [__file__, "connect4.py", "player.py"]
# WATCHED_FILE_MTIMES = [(f, getmtime(f)) for f in WATCHED_FILES]

# while True:
# 	for f, mtime in WATCHED_FILE_MTIMES:
# 		if getmtime(f) != mtime:
# 			print("FILES UPDATED.... RESTARTING")
# 			os.execv(sys.executable, ['python3'] + sys.argv)
# # TODO: either solve restarting bot issue or not have the functionality at all