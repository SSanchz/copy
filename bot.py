import discord
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define the channels
# IMPORTANT: Replace these with the ACTUAL channel IDs.
# You can get channel IDs by enabling Developer Mode in Discord's
# User Settings -> Advanced, then right-clicking a channel and selecting "Copy ID".
SOURCE_CHANNEL_ID = 123456789012345678  # Replace with your source channel ID
DESTINATION_CHANNEL_ID = 987654321098765432  # Replace with your destination channel ID

# Define the intents your bot needs
# GUILDS: To connect to a guild (server)
# GUILD_MESSAGES: To receive messages in guilds
# MESSAGE_CONTENT: To read the content of messages (required for reading messages)
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True # Crucial for reading message content

# Create a Discord client instance
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Event that fires when the bot has successfully connected to Discord."""
    print(f'{client.user} has connected to Discord!')
    print(f'Bot is ready to listen for messages.')

    # Optionally, you can set the bot's status here
    await client.change_presence(activity=discord.Game(name="forwarding messages"))

@client.event
async def on_message(message):
    """Event that fires every time a message is sent in a channel the bot can see."""
    # Ignore messages from the bot itself to prevent infinite loops
    if message.author == client.user:
        return

    # Check if the message is from the source channel
    if message.channel.id == SOURCE_CHANNEL_ID:
        print(f"Received message from source channel ({message.channel.name}): {message.content}")

        # Get the destination channel
        destination_channel = client.get_channel(DESTINATION_CHANNEL_ID)

        if destination_channel:
            # Construct the message to be sent to the destination channel
            # You can customize this message as you like.
            # For example, to include the author's name:
            # formatted_message = f"**{message.author.name}**: {message.content}"
            formatted_message = f"{message.content}" # Simple forwarding of content

            try:
                # Send the message to the destination channel
                await destination_channel.send(formatted_message)
                print(f"Successfully forwarded message to destination channel ({destination_channel.name}).")
            except discord.Forbidden:
                print(f"Error: Bot does not have permission to send messages in channel {destination_channel.name}.")
            except Exception as e:
                print(f"An error occurred while sending message: {e}")
        else:
            print(f"Error: Could not find destination channel with ID {DESTINATION_CHANNEL_ID}.")

# Run the bot
client.run(TOKEN)
