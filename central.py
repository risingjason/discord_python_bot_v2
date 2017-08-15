#!/usr/bin/env python

#AUTHOR: Jason Yatfai Zhang
#GITHUB: risingjason

import discord
import commands
import asyncio
import enum
import os
import sys

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
master_user = "91115380646354944"

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
				#await client.send_message(channel, online_message)

@client.event
async def on_message(msg):
	cmds = [x.lower() for x in msg.content.split(" ")] # parses string and makes them lowercase
	cmd = cmds[0] # first word is always !command; used to access commands.py module
	mentions = msg.raw_mentions # might be of use in the future
	# print(cmds)
	#waits for any of the commands in commands.py to be called upon
	#if msg.channel.id in allowed_text_channels:

	if cmd in commands.commands and msg.author.id == master_user :
		await commands.commands[cmd](client, msg, cmds)

print("Starting bot...")
client.run(token)