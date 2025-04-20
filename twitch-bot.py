import os
import twitchio
import datetime
import time
from twitchio.ext import commands, routines

#create a twitch dev account and create an application https://dev.twitch.tv/console/extensions/create
#use http://localhost:4343/oauth/callback as your OAuth Redirect URL
#get your client id and paste it into the link below
#https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=#YOUR-CID#&redirect_uri=http://localhost:4343/oauth/callback&scope=channel:bot
#when you paste the link in browser, you will be authenticate and be redirected to an empty page with your Oauth Token in the URL

#you will need python 3.7+ and pip
#then pip install twitchio
#this uses twitchio 2.10, will not work with twitchio 3

#Twitch credentials
OAUTH_TOKEN = # Replace with your OAuth token
CLIENT_ID = # Replace with your Client ID
CHANNEL_NAME = # Replace with the channel name

# File output commands, i use this in conjuntion with advanced scene switcher
# when the file is created ADVSS can take an action, and use a cleanup script when done
OUTPUT_FOLDER = r"C:\YOUR_FOLDER"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
# List of commands to monitor for file output (in uppercase)
COMMANDS = [
    "!FILE","!REFRESH"
]

RESPONSE = {
    "!COMMANDS":"!LIBRARY | !LARRY | !FEEDERS | !OTHERS | !REFRESH | !LINKS | !DIVEST",
    "!LIBRARY":"Chunka Luta Library is a collection of reading recommended by anti-colonial activists of Turtle Island - https://mega.nz/folder/cuMwjRyK#eDPayQSdYFwaCh9qr8zzPw",
    "!LARRY":"https://beacons.ai/llarry",
    "!STREETCAT":"https://streetcatlove.github.io",
    "!MAMA":"https://bsky.app/profile/mamaemmedia.bsky.social",
    "!ADRIENNE":"https://allmylinks.com/adriennevixen",
    "!SMESH":"https://linktr.ee/leninsmesh",
    "!NEURORIOT":"https://neuroriot.net",
    "!DIVEST":"#DivestFromTwitch https://streetcatlove.github.io/divest",
    "!BLOCK":"a helpful userscript can block unwanted video interferences https://github.com/pixeltris/TwitchAdSolutions",
    "!MULTI":"how to multi-stream - https://streetcatlove.github.io/hellostreetcat/multi"
}

TIMER = [
    "Timer X:00",
    "Timer X:12",
    "Timer X:24",
    "Timer X:36",
    "Timer X:48"
]

class TwitchChatBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=OAUTH_TOKEN,
            client_id=CLIENT_ID,
            prefix="!",
            initial_channels=[CHANNEL_NAME]
        )
        self.clock_routine.start()
        
    @routines.routine(seconds=60.0, wait_first=True)  # Check every minute
    async def clock_routine(self):
        now = datetime.datetime.now()
        channel = self.get_channel('street_cat_love')
        if now.minute == 0:
            await channel.send(TIMER[0])
        elif now.minute == 12:
            await channel.send(TIMER[1])
        elif now.minute == 24:
            await channel.send(TIMER[2])
        elif now.minute == 36:
            await channel.send(TIMER[3])
        elif now.minute == 48:
            await channel.send(TIMER[4])

    async def event_ready(self):
        print(f"Logged in as {self.nick} and monitoring {CHANNEL_NAME}'s chat...")

    async def event_message(self, message):

        # Convert the message to uppercase for case-insensitive comparison
        message_content_upper = message.content.upper()

        # Check if the message is a command (case-insensitive)
        if message_content_upper in COMMANDS:
            print(f"Command detected: {message_content_upper} from {message.author.name}")
            self.create_command_file(message_content_upper)
        
        if message_content_upper in RESPONSE:
            print(f"Response triggered: {message_content_upper} : {RESPONSE[message_content_upper]} from {message.author.name}")
            await message.channel.send(RESPONSE[message_content_upper])

    def create_command_file(self, command):
        # Create a file for the detected command (filename in uppercase)
        file_path = os.path.join(OUTPUT_FOLDER, f"{command[1:]}.txt")
        with open(file_path, "w") as file:
            file.write(f"Command {command} was detected in chat.\n")
        print(f"File created: {file_path}")

# Run the bot
if __name__ == "__main__":
    bot = TwitchChatBot()
    bot.run()
