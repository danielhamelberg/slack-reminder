import time
import os

# Import the necessary libraries for using the Slack API
# and for using text-to-speech on a Mac
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from Foundation import NSSpeechSynthesizer

# Set the Slack API token
SLACK_API_TOKEN = "your-api-token-here"

# Set the Slack channel to subscribe to
SLACK_CHANNEL_ID = "C1234567890"

# Set the threshold for the volume below which
# persistent toast notifications will be used
VOLUME_THRESHOLD = 15

# Initialize the Slack client
client = WebClient(token=SLACK_API_TOKEN)

# Initialize the text-to-speech synthesizer
synthesizer = NSSpeechSynthesizer.alloc().initWithVoice_(None)

def read_message(message):
  # Use the text-to-speech synthesizer to read out the message
  synthesizer.startSpeakingString_(message)

def notify_new_thread(thread):
  # Notify the user that a new thread has been started
  print("A new thread has been started: " + thread["title"])
  
  # Check if the volume is below the threshold
  if int(os.popen("osascript -e 'get volume settings'").read().split(",")[0]) < VOLUME_THRESHOLD:
    # Use a persistent toast notification to catch the user's attention
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(thread["title"], "New Thread"))

def notify_updated_thread(thread):
  # Notify the user that an existing thread has been updated
  print("An existing thread has been updated: " + thread["title"])
  
  # Check if the volume is below the threshold
  if int(os.popen("osascript -e 'get volume settings'").read().split(",")[0]) < VOLUME_THRESHOLD:
    # Use a persistent toast notification to catch the user's attention
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(thread["title"], "Updated Thread"))

def remind_unanswered_threads():
  # Remind the user of any unanswered threads
  print("Reminding the user of unanswered threads...")
  
  # Check if the volume is below the threshold
  if int(os.popen("osascript -e 'get volume settings'").read().split(",")[0]) < VOLUME_THRESHOLD:
    # Use a persistent toast notification to catch the user's attention
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format("You have unanswered threads", "Unanswered Threads"))

# Connect to the Slack API
# and subscribe to the #release-team channel
response = client.conversations_join(channel=SLACK_CHANNEL_ID)

# Get the latest message in the channel
response = client.conversations_history(channel=SLACK_CHANNEL_ID, limit=1)

# Get the latest message's timestamp
latest_message_timestamp = response["messages"][0]["ts"]

# Get the latest thread's timestamp
latest_thread_timestamp = response["messages"][0]["thread_ts"]

# Get the latest thread's title
latest_thread_title = response["messages"][0]["text"]

# Get the latest thread's ID
latest_thread_id = response["messages"][0]["thread_ts"]

# Get the latest thread's author
latest_thread_author = response["messages"][0]["user"]

# Get the latest thread's replies
latest_thread_replies = response["messages"][0]["replies"]

# Get the latest thread's reply count
latest_thread_reply_count = len(latest_thread_replies)

# Get the latest thread's reply authors
latest_thread_reply_authors = []

for reply in latest_thread_replies:
  latest_thread_reply_authors.append(reply["user"])

# Get the latest thread's reply timestamps
latest_thread_reply_timestamps = []

for reply in latest_thread_replies:
  latest_thread_reply_timestamps.append(reply["ts"])

# Get the latest thread's reply messages
latest_thread_reply_messages = []

for reply in latest_thread_replies:
  latest_thread_reply_messages.append(reply["text"])

# Get the latest thread's reply IDs
latest_thread_reply_ids = []

for reply in latest_thread_replies:
  latest_thread_reply_ids.append(reply["ts"])

# Get the latest thread's reply parent IDs
latest_thread_reply_parent_ids = []

for reply in latest_thread_replies:
  latest_thread_reply_parent_ids.append(reply["thread_ts"])

# Loop forever
while True:
  # Get the latest message in the channel
  response = client.conversations_history(channel=SLACK_CHANNEL_ID, limit=1)

  # Get the latest message's timestamp
  latest_message_timestamp = response["messages"][0]["ts"]

  # Get the latest thread's timestamp
  latest_thread_timestamp = response["messages"][0]["thread_ts"]

  # Get the latest thread's title
  latest_thread_title = response["messages"][0]["text"]

  # Get the latest thread's ID
  latest_thread_id = response["messages"][0]["thread_ts"]

  # Get the latest thread's author
  latest_thread_author = response["messages"][0]["user"]

  # Get the latest thread's replies
  latest_thread_replies = response["messages"][0]["replies"]

  # Get the latest thread's reply count
  latest_thread_reply_count = len(latest_thread_replies)

  # Get the latest thread's reply authors
  latest_thread_reply_authors = []

  for reply in latest_thread_replies:
    latest_thread_reply_authors.append(reply["user"])

  # Get the latest thread's reply timestamps
  latest_thread_reply_timestamps = []

  for reply in latest_thread_replies:
    latest_thread_reply_timestamps.append(reply["ts"])

  # Get the latest thread's reply messages
  latest_thread_reply_messages = []

  for reply in latest_thread_replies:
    latest_thread_reply_messages.append(reply["text"])

  # Get the latest thread's reply IDs
  latest_thread_reply_ids = []

  for reply in latest_thread_replies:
    latest_thread_reply_ids.append(reply["ts"])

  # Get the latest thread's reply parent IDs
  latest_thread_reply_parent_ids = []

  for reply in latest_thread_replies:
    latest_thread_reply_parent_ids.append(reply["thread_ts"])

  # Check if the latest message is a new thread
  if latest_message_timestamp == latest_thread_timestamp:
    # Check if the latest thread is a new thread
    if latest_thread_id not in latest_thread_reply_parent_ids:
      # Notify the user that a new thread has been started
      notify_new_thread({"title": latest_thread_title})

      # Read out the latest thread's title
      read_message(latest_thread_title)

    # Check if the latest thread is an updated thread
    elif latest_thread_reply_count > 0 and latest_thread_reply_timestamps[-1] > latest_thread_timestamp:
      # Notify the user that an existing thread has been updated
      notify_updated_thread({"title": latest_thread_title})
         
      # Read out the latest thread's title
      read_message(latest_thread_title)

      # Read out the latest thread's reply
      read_message(latest_thread_reply_messages[-1])

  # Check if the latest message is a new reply
  elif latest_message_timestamp in latest_thread_reply_timestamps:
    # Notify the user that an existing thread has been updated
    notify_updated_thread({"title": latest_thread_title})
         
    # Read out the latest thread's title
    read_message(latest_thread_title)

    # Read out the latest thread's reply
    read_message(latest_thread_reply_messages[-1])

  # Remind the user of unanswered threads
  remind_unanswered_threads()

  # Sleep for 3 minutes before checking again
  time.sleep(180)
