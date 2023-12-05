# ooberbot
__A Discord LLM bot that runs using [oobabooga's text-generation-webui](https://github.com/oobabooga/text-generation-webui)__

*Be warned, this bot is barebones and probably trash. I'm not great with programming or python in general. You have been warned.*

### Requirements:
- Python
- [oobabooga's text-generation-webui](https://github.com/oobabooga/text-generation-webui)
- Linux, *maybe* MacOS
- A brain
## Installation Instructions:
**1.** Open a terminal window and type:

```bash 
git clone https://github.com/notmugi/ooberbot && cd ooberbot
```
Or download the project from github manually and place it at your desired location.

 **2.** Next, type:

```bash
./install.sh
```

This should copy your ooberbot config to `~/.config/ooberbot`, and then install all the required python dependencies from `install.txt` using pip.

**3.** Assuming you already have a discord bot set up on the [Discord Developer portal](https://discord.com/developers/applications),
You will need to copy your bot's Discord Token into the "token" field in `~/.config/ooberbot/config.yaml`. 

**4.** Generate an invite link in the dev portal and invite your bot to your desired server. or DM it. up to you.

**5.** Find **textgen_default_cfg** and **textgen_user_cfg** in your `config.yaml` file. Set these to the corresponding 
file paths. wherever you decided to install the text-generation-webui.

That's it!

## Usage:

At this point, you are **free to start using ooberbot.**

![image](https://github.com/notmugi/ooberbot/assets/12789510/bd601350-af74-4718-8d9f-517e8915b029)


Simply type `python ooberbot.py` if you are still in the same folder, or `python /path/to/ooberbot.py` if you are not.

Currently, the bot is very barebones and will only reply to whatever message it sees, without any rate limiting or anything of that sort.

If you'd like to include your own video file, image, text file, gif, audio file, or any other file, for when the bot's history is reset, place it in ~/.config/ooberbot/vids and open `config.yaml`.
Find the line **"video_file_name"** and specify the filename there.
It supports whatever discord will embed. Images, audio, text files, videos, gifs, etc.  This behavior is disabled entirely through the included `config.yaml` file.

### Commands:
- You may pause the bots interactions with `/pause`
- you may resume them again with `/resume`
- You may clear the bots history using `/lobotomize`

## Config:

All config is stored in `~/.config/ooberbot/config.yaml` and is commented to explain all features.

Setting **"settings_type"** in `config.yaml` to `user` will use **settings.yaml** from your text-generation-webui. this is the settings file that gets used when you save your generation settings.
otherwise, it uses `default` which pulls from **settings-template.yaml** from your text-generation-webui. this is the default config, and should give your bot generic ai responses.

### Advanced configuration: 
If you'd like to add more settings from the webui's config files, feel free to implement more stuff in the `settings = {} field.` Just follow the current format such as: 
```python
"value1": textgencfg['value1'],
"value2": textgencfg['value2'],
"value3": textgencfg['value3']
```
However, your `"preset"` contains all the generation information, and `"instruction_template"` already contains your prompt. I'm not 
sure what else you may need, but i guess its free for you to edit, so have fun.
