import re
import requests 
import json

from mattermost_bot.bot import listen_to
from mattermost_bot.bot import respond_to


@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply('I can understand hi or HI!')


@respond_to('I love you')
def love(message):
    message.reply('I love you too!')


@listen_to('Can someone help me?')
def help_me(message):
    # Message is replied to the sender (prefixed with @user)
    message.reply('Yes, I can!')

    # Message is sent on the channel
    # message.send('I can help everybody!')

@listen_to('https://app.box.com/s/[0-9A-Za-z]*', re.IGNORECASE)
def box_file(message):

	channel_id = message.get_channel_id()

	print(channel_id)

	message_body = message.get_message()

	bearer = "<box_developer_token>"

	url = "https://api.box.com/2.0/shared_items"

	boxapi_header = "shared_link=" + message_body
	auth_header = "Bearer " + bearer

	headers = {'Boxapi':  boxapi_header, 'authorization': auth_header}

	response = requests.get(url, headers=headers)

	output = json.loads(response.text)
	print(output['id'])

	box_id = output['id']
	box_name = output['name']


# step  2



	url = "https://api.box.com/2.0/files/" + box_id + "/content"
	print(url)


	headers = {'authorization': auth_header}
	response = requests.get(url, headers=headers)

	send_file =  response.content


	# step 3


	url = "<url_of_the_mattermost>/api/v1/users/login"

	payload =  "{\n  \"name\": \"<team_name>\",\n  \"email\": \"sh*********@gmail.com\",\n  \"password\": \"b*********\"\n}"
	headers = {'content-type': "application/json"}

	response = requests.request("POST", url, data=payload, headers=headers)

	print(response.headers)

	token_id = response.headers['Token']

	print(token_id)


	# step 4-pre

	url = "<url_of_the_mattermost>/api/v1/users/me"

	auth_header = "Bearer " + token_id

	headers =  {'authorization': auth_header}

	response = requests.request("GET", url, headers=headers)

	print(response)


	# step 4


	url = "<url_of_the_mattermost>/api/v1/files/upload"

	auth_header = "Bearer " + token_id

	headers =  {'authorization': auth_header}

	files = {'files': send_file}

	data = {'channel_id': channel_id}

	response = requests.post(url, files=files, data=data, headers=headers)

	output = json.loads(response.text)
	print(output['filenames'])

	print(response.text)
	filenamesT = output['filenames']

	filenames = filenamesT[0]
	print(filenames)


	#step 5

	print("step 5")

	url = "<url_of_the_mattermost>/api/v1/channels/" + channel_id + "/create"

	auth_header = "Bearer " + token_id

	headers =  {'authorization': auth_header}

	string = filenames.split("/")

	time='1462822960652'
	joinString = string[2]+":"+time

	filenames = "[\"" + filenames + "\"]"

	payload = "{\"filenames\": " + filenames + ",\"message\":\"\",\"channel_id\": \"" + string[1] + "\",\"pending_post_id\": \"" + joinString + "\",\"user_id\": \"" + string[2] + "\" ,\"create_at\":" + time + "}"

	print payload

	response = requests.request("POST", url, data=payload, headers=headers)

	print response
