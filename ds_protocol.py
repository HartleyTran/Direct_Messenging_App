# ds_protocol.py

# Starter code from assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME: Hartley Tran
# EMAIL: hartlemt@uci.edu
# STUDENT ID: 55747472

import json
from collections import namedtuple
import time

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['cmd', 'token', 'resp'])


def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  '''
  try:
    json_obj = json.loads(json_msg)
    if "response" in json_obj: # extracts response msg
      if json_obj["response"]["type"] == 'ok':
        if "messages" in json_obj['response']:
          data = DataTuple('O', '', json_obj["response"]["messages"])
        else:
          data = DataTuple('O', json_obj["response"]["token"] if 'token' in json_obj["response"] else '', json_obj["response"]["message"])
      
      elif json_obj["response"]["type"] == 'error':
        data = DataTuple('E', '', json_obj["response"]["message"])
      
    elif "join" in json_obj: # extracts join msg
      if json_obj["response"]["type"] == 'ok':
        data = DataTuple('O', json_obj["response"]["token"] if 'token' in json_obj["response"] else '', json_obj["response"]["message"])
      elif json_obj["response"]["type"] == 'error':
        data = DataTuple('E', '', json_obj["response"]["message"])

  except json.JSONDecodeError:
    print("Json cannot be decoded.")
    data = DataTuple('E', '', 'Json cannot be decoded.')
  return data


def encode_json(cmd:str, entry:str=None, token:str=None, user:str=None, extra:str=None) -> str:
  '''
  Call json.dumps function on dict and covert into json msg

  '''
  if cmd == 'join':
    temp = {'join': {"username": user, "password": extra, "token": ''}}
  elif cmd == 'directmessage': 
    if extra == 'send':
      temp = {"token": token, 'directmessage': {"entry": entry, 'recipient': user, 'timestamp': str(time.time())}}
    else:
      temp = {"token": token, 'directmessage': extra}

  elif cmd in ['bio', 'post']:
    temp = {'token': token, cmd: {'entry': entry, 'timestamp': str(time.time())}}
  
  json_msg = json.dumps(temp)

  return json_msg
