# Bonfire - Discord Bot

## What is Bonfire?

Bonfire is a Discord bot that mimics Spotify Premium's listen-along feature. Allowing people to listen along with someone to their songs played in Spotify.

## How does it work?

By "pairing" the bot to someone, it takes the Spotify activity details and plays the song in a voice channel. Allowing other people to join the channel and listen along.

## How to get the bot?

How can I invite Binfire to my Discord server?

Unfortunately, due to how this bot is built, it cannot be invited. Because, as of the moment, it cannot handle multiple servers at once. However, you can quickly install the bot and get it up and running on either your personal computer or a server.

### Installation

This bot requires [**Python**](https://www.python.org/downloads/) to run since it's built using it. (Make sure to click on the option to add Python to PATH.)
You can use `sudo apt install python3` or `sudo yum install python3` if you are on Linux.

On a Command Line interface such as Command Prompt/Powershell or Bash, navigate to the folder you want to install Bonfire in.

Enter the following commands.

#### Clone the repo

```console
$ git clone https://github.com/BinethAtukorala/Bonfire.git
$ cd Bonfire
```

#### Install requirements

```console
$ pip install -r requirements.txt
```

Here's a [resource](https://realpython.com/python-virtual-environments-a-primer/) if you want to setup a Virtual Enviroment to run the bot in and avoid changing global Python settings.

#### Set `config.json`

Open the `config.json` file and set the following fields.

* `discord`
    * `token` - Set your Discord Bot Token. If you don't have one, here's [how to get one](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/). (Follow steps up to *How to Invite Your Bot to Join a Server*)
    * `prefix` - Set the prefix that Bonfire should use. This will be prefixing all the commands you want the bot to interact with.
* `spotify`
    * `id` - Set your Spotify API Client ID. Here's [how to get it](https://support.heateor.com/get-spotify-client-id-client-secret/).
    * `secret` - Set your Spotify API Client secret.

#### Run the bot

```console
$ python3 run.py
```

#### aaand.... Done!

Now invite the bot to your Discord Server and have fun. Create an OAuth link for your bot using the Discord Developers Dashboard. [Here's how](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/#:~:text=How%20to%20Invite%20Your%20Bot%20to%20Join%20a%20Server).

## Known Issues
* Doesn't seek to the current position of the song if the `start` command is used after the song has already begun.
* Low quality audio on networks with poor internet connection.

## Contributing

Contributions to Bonfire are always welcome, whether it be improvements to the documentation or new functionality, please feel free to make the change and create a pull request.