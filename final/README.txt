HOW TO OPERATE
----------------------------------------------
1. Start by running the final.py module

2. When the user interface appears, go to the top left to the button labeled "File"

3. Under "File," there is "New" which will let you create a new DSU profile and there is "Open..." which will let you open an existing DSU profile.
	-- If you choose to create a new DSU profile, you will then need to complete your profile information by going into the "Edit" button where you can then choose to edit your username, password, or server IP.
	-- If whitespaces or an empty entry is submitted, the pop-up will close but nothing will change
	-- Clicking on any of the "Edit" options before opening a DSU file will open a pop-up window that tells you to open a DSU file first
	-- At minimum, the profile must have a valid username and password to send messages to the DSU server. The footer status will change and tell you when you have connected to the DS server

4. To start a new conversation with another person, click on the "Add User" button at the bottom left.
	-- A pop-up window will appear that will allow you to enter a user's username
		This will add the new user to the TreeView widget on the left, and then when clicked you will be able to send a message to them
	-- If whitespaces or an empty entry is submitted, the pop-up will close but nothing will be added
	-- Clicking on this button before opening a DSU file will open a pop-up window that tells to open a profile first
	-- If a username that is already in the TreeView is entered, the message history with that user will be brought up

5. To send a message to another user, click on one of the users in the TreeView widget.

6. Type in the Entry widget at the bottom left and click the "Send" button when you want to send the message to the user select from step 5
	-- The Entry editor will not be cleared and sent if no user is selected or if you are offline (not connected to server)	 
		The entry box will clear when a user is selected and then the "Send" button is clicked
	-- You can also tell who you will send a message to with the Label above the Messages box that gives you the username of the person you selected/added
	-- A message will not be sent if the user does not type anything in the entry box (ie: the box is empty or only whitespaces)

7. The "Update" button next to the "Send" button will immediately update the message box for any new messages from the user.
	-- This is done by clearing the Event Loop of any previous calls for updating the message box, and immediately calling a new one
	-- Update can also be used to reconnect to the DS server when getting online when you were once offline
		Updating after connecting to the server will update the message box with any new messages


final.py
---------------------------------------------------
This module is the main program the initializes the user interface.
It is built on from a5.py from the Assignment 5.
The new subclass I created is called Pop, which can be seen from line 20 to 64.
	This handles any pop-up windows, which are currently only for editing profile or adding a new user to message.
I used try/except at lines 369 to 375, lines 412 to 424, lines 470 to 474, and lines 505 to 532 when attempting to connect to the DS server and access any messages.
	If the attempt fails due to no internet connect, the footer status will change to "Unable to connect to DS server" and will instead load up any mesages that are in the current DSU profile.
Some sources I referred to to enhance my GUI are TkDocs and the Codemy.com channel on Youtube.
	These sources specifically helped me better understand how to operate the tkinter widgets, create the pop-up window, and create tags for specific text.


ds_messenger.py
---------------------------------------------------
This module is called when the user is sending a message to another user or retrieving any messages sent to them.
I created a custom Exception class called DirectMsgError, which is raised whenever sending "directmessage" or "join" request to the DS server fails.
I used try/excepts whenever I was attempting to send a JSON message to the DS server. When it fails it will raise the DirectMsgError.
When the DirectMessenger class is instantiated, it sends a join message that will set the self.token to the received token from the server's response


ds_protocol.py
---------------------------------------------------
This module was built on from the ds_protocol module from a3.
It has been extended to support "directmessage" requests.
It enables the ds_messenger to easily send any server requests by converting any commands in to a JSON msg with encode_json, and processes any commands received in JSON to be converted into a DataTuple.
	The DataTuple has three attributes: 'cmd', 'token', and 'resp'
		cmd will either be E - 'error' and O - 'ok'
		token will be the token sent from the server
		resp will be the msg accompanied with JSON (ie: "Direct message sent" or the list of messages sent from other users)


Profile.py
---------------------------------------------------
This module is nearly identical to the Profile.py from previous assignments.
I have only added a command that allows the profile to store messages when the load_profile command is called.
	the _posts variable stores any messages that the user sends, while the _messages stores any messages the user received.