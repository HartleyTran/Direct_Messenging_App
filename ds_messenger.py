# NAME: Hartley Tran
# EMAIL: hartlemt@uci.edu
# STUDENT ID: 55747472


import socket
from ds_protocol import encode_json, extract_json

dsuserver = '168.235.86.101'
port = 3021

class DirectMsgError(Exception):
  """
  DirectMsgError is a custom exception handler that catches error specifcally for handling with 
  direct messaging. It is raised when attempting to join or send 'directmessage' requests to the DS server.
  """
  pass



class DirectMessage(dict):
  """
  DirectMessage class works similar to Post class in Profile.py
  this mainly will be used to store and display messages from the user profile
  """
  def __init__(self, recipient:str=None, message:str=None, timestamp:float=0):
    self.recipient = recipient
    self.entry = message
    self.timestamp = timestamp

    dict.__init__(self, recipient=self.recipient, entry=self.entry, timestamp=self.timestamp)


class DirectMessenger:
  """
  DirectMessenger class is mainly used to store server info. Sends requests to send messages to
  another user and receives responses to retrieve messaging history 
  """
  def __init__(self, dsuserver=None, username=None, password=None):
    """
    Sends join request and sets token from response message
    """
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
    self.token = None
    
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((self.dsuserver, port))

        join_msg = encode_json(cmd='join', user=self.username, extra=self.password)

        send = client.makefile('w')
        recv = client.makefile('r')

        send.write(join_msg + '\r\n')
        send.flush()

        resp = recv.readline()
        data = extract_json(resp)
        print(data.resp)
        self.token = data.token
    except Exception as ex:
      raise DirectMsgError('An error occurred while attempting to join the DS server.', ex)

  def send(self, message:str, recipient:str) -> bool:
    """
    Sends directmessage request to server, send a message to another user
    returns true if message successfully sent, false if send failed.
    """
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((self.dsuserver, port))
      
        new_msg = encode_json(cmd='directmessage', extra='send', token=self.token, entry=message, user=recipient)
      
        send = client.makefile('w')
        recv = client.makefile('r')

        send.write(new_msg + '\r')
        send.flush()

        resp = recv.readline()
        data = extract_json(resp)
        print(data.resp)
        if data.cmd == 'E':
          return False
        elif data.cmd == 'O':
          return True
    except Exception as ex:
      raise DirectMsgError('An error occured while attempting to send a direct message.', ex)
		
  def retrieve_new(self) -> list[DirectMessage]:
    """
    Sends directmessage request to server, receive all new messages in profile
    returns a list of DirectMessage objects containing all new messages
    """
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((self.dsuserver, port))

        new_msg = encode_json(cmd='directmessage', extra='new', token=self.token)

        send = client.makefile('w')
        recv = client.makefile('r')

        send.write(new_msg + '\r')
        send.flush()

        resp = recv.readline()
        data = extract_json(resp)
        if data.cmd == 'E':
          return False
        elif data.cmd == 'O':
          messages = []
          for msg in data.resp:
            temp = DirectMessage(msg['from'], msg['message'], msg['timestamp'])
            messages.append(temp)
          return messages
    except Exception as ex:
      raise DirectMsgError('An error occured while attempting to retreive new messages.', ex)
 
  def retrieve_all(self) -> list[DirectMessage]:
    """
    Sends directmessage request to server, receive all messages in profile
    returns a list of DirectMessage objects containing all messages
    """
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((self.dsuserver, port))

        new_msg = encode_json(cmd='directmessage', extra='all', token=self.token)

        send = client.makefile('w')
        recv = client.makefile('r')

        send.write(new_msg + '\r')
        send.flush()

        resp = recv.readline()
        data = extract_json(resp)
        if data.cmd == 'E':
          return False
        elif data.cmd == 'O':
          messages = []
          for msg in data.resp:
            temp = DirectMessage(msg['from'], msg['message'], msg['timestamp'])
            messages.append(temp)
          return messages
    except Exception as ex:
      raise DirectMsgError('An error occured while attempt to retreive messages.', ex)
