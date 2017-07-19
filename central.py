#AUTHOR: Jason Yatfai Zhang
#GITHUB: risingjason

import discord
import asyncio
import enum

#NEW UPDATE TO DISCORD NO LONGER ALLOWS BOT TO BE LOGGED IN THROUGH EMAIL AND PASSWORD
#Copy and paste your bot's token into infos.txt
#Bot tokens are obtained through the Discord Developer website
fp_token = open("token.txt", "r")
token = fp_token.read()
fp_token.close()

client = discord.Client()

online_message = "Bot v2.0 Currently in Development"

@client.event
async def on_ready():
	print("Bot is running as the user '{}'".format(client.user.name))
	channel = client.get_all_channels()
	for channel in client.get_all_channels():
		if channel.type is discord.ChannelType.text: #notifies all registered text channels that the bot is online
			#utf-8 compatibility paste .encode("utf-8") after channel.name
			print("Bot is running on server: {}, name: {}, id: {}, type: {}".format(channel.server, channel.name, channel.id, channel.type)) 
			if channel.name == "general":
				# prints a Bot Online status too all text channels in every server
				await client.send_message(channel, online_message)

@client.event
async def on_message(msg):
	cmds = msg.content.split(' ') # seperates the message word by word
	cmd = cmds[0].lower() # takes the first word (most commands are called using the first word of message)
	mentions = msg.raw_mentions

	#waits for any of the commands in core to be called upon
	if cmd in core.commands:
		await core.commands[cmd](client, msg, cmds)

print("Starting bot...")
client.run(token)