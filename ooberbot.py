import os
import json
import requests
import yaml
import discord
import discord.ext
from discord import app_commands
from platformdirs import *

# Written by: mugi1
# INSTRUCTIONS: README.MD
# or on github idk doesnt really matter, just follow the instructions

### Change the config dir here. default location is in ~/.config/ooberbot
### This handles loading our YAML config file.
with open (user_config_dir()+'/ooberbot/config.yaml', 'r') as oobercfg:
    botCfg = yaml.safe_load(oobercfg)
    
# specifically this is where we grab all the yaml data for our Discord bot.
hist_length = botCfg['history_length']
msg_logging = botCfg['do_message_logging']
base_url = botCfg['textgen_base_url']
cfg_def_loc = botCfg['textgen_default_cfg']
cfg_usr_loc = botCfg['textgen_user_cfg']
settings = botCfg['settings_type']
lobotomyVid = botCfg['history_reset_video']
videoname = botCfg['video_file_name']
status_type = botCfg['bot_status_type'] 
bot_status = botCfg['bot_status']
isPaused = botCfg['silent_default']
url = base_url+"/v1/chat/completions"

# Open the textgen webui config yamls.
if settings == 'default':
    with open (botCfg['textgen_default_cfg'], 'r') as textgencfgfile:
        textgencfg = yaml.safe_load(textgencfgfile)
else:
    if settings == 'user':
        with open (botCfg['textgen_user_cfg'], 'r') as textgencfgfile:
            textgencfg = yaml.safe_load(textgencfgfile)
      
# Set discord intents
intents = discord.Intents.default()
intents.message_content = True
AIBot = discord.Client(intents=intents)

# Set up discord command tree
tree = app_commands.CommandTree(AIBot)
AIBot.tree = tree

# Set some textgen webui vars
history = []
headers = {
    "Content-Type": "application/json"
}

# Initialized when bot is started
@AIBot.event
async def on_ready():
    # set up some bot stuff. here we print out login, set the activity status and sync our slash commands.
    print(f'logged in as {AIBot.user}')
    await AIBot.change_presence(activity = discord.Activity(type=status_type, name="to the voices"))
    await AIBot.tree.sync()
# Set up our first command. this is the reset history command.
@AIBot.tree.command(name="lobotomize", description="reset osaka's brain!")
async def lobotomize(interaction: discord.Interaction) -> None:
    # check if we are enabling the posting of a video when we reset history. if not, just print text.
    if lobotomyVid:
        await interaction.response.send_message(file=discord.File(f'{user_config_dir()}/ooberbot/vids/{videoname}'), content="Sata andagi!!!")
    else:
        await interaction.response.send_message("Sata andagi!!!")
    print(f'history before clear:\n{history}')
    history.clear()
    print(f'history after clear:\n{history}')

# command numero two. this pauses ooberbot.
@AIBot.tree.command(name="pause", description="Shut that bitch up !!")
async def pause(interaction: discord.Interaction) -> None:
    global isPaused
    isPaused = True
    await interaction.response.send_message(f'ermmm i wont talk anymore..')

# command numero C, resumes ooberbot's yapping.     
@AIBot.tree.command(name="resume", description="Make the bot a chatterbox once more.")
async def pause(interaction: discord.Interaction) -> None:
    global isPaused
    isPaused = False
    await interaction.response.send_message("SATAA ANDAGIII SATAA ANDAGIII SATAA ANDAGIII SATAA ANDAGIII")

# this code runs whenever a message is sent in any channel it can access, or dmed to the bot.
@AIBot.event
async def on_message(message):

    # check if bot's history is too long. keep this short to save resources.
    if len(history) >= hist_length:
        del history[-1]

    # check if message came from bot. if it did, do not reply.
    if message.author == AIBot.user:
        return
        
    # is the bot paused? if not, we can send messages.
    if not isPaused:
        async with message.channel.typing():

            # append the first part of the user message for the LLM.    
            history.append({"role": "user", "content": message.content})

            # every message, grab these settings. (these update on a per-message basis.)
            # tweak your settings in the webUI, get good results, save them, and they will apply to the bot.
            settings = {
                "mode": textgencfg['mode'],
                "preset": textgencfg['preset'],
                "instruction_template": textgencfg['instruction_template'],
                "character": textgencfg['character'],
                "messages": history
            }

            # set up bot response and send POST request with necessary info
            response = requests.post(url, headers=headers, json=settings, verify=False)
            # grab the bot's reply from the choices json in the post request
            bot_message = response.json()['choices'][0]['message']['content']
            # throw it into the history list. gives our LLM the necessary context.
            history.append({"role": "assistant", "content": bot_message})

            # send response as message
            await message.channel.send(bot_message)
            if msg_logging:
                # print messages for logging if that's enabled.
                print("\n"f'{message.author}: '+f'{message.content}')
                print("Bot response: "+f'{bot_message}')
            else:
                return
    else: 
        if isPaused:
            return
            
   

# run muddafucka (put your discord token in an environment file, or type it before running the python script)
# e.g either in your .zshrc, .bashrc, or by running the script like:
# DISCORD_TOKEN=tokenhere python ~/bot/main.py
AIBot.run(botCfg['token'])
