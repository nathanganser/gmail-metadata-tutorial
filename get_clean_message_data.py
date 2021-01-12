import re
import os
import json
import datetime
from pprint import pprint


def extract_data(message: dict):
    """
    takes a raw gmail message as a dictionary and returns the refactored version
    :param message: dict
    :return: dict
    """

    # get the data which can be taken directly from the raw message
    new_message = {
        "id": message.get('id'),
        "history_id": message.get('historyId'),
        "thread_id": message.get('threadId'),
        "labels": message.get('labelIds'),
        "date": str(datetime.datetime.fromtimestamp(int(message.get('internalDate')) / 1000)),
        "to": [],
        "subject": None,
        "from": None,
        "from_name": None
    }

    # check the headers to get the rest of the fields
    for header in message['payload']['headers']:
        # get name and emails of the recipients
        if header['name'] == 'To':
            val = header['value']
            tos = val.split(',')
            for to in tos:
                try:
                    name = to[:to.index('<')].strip()
                    email = re.findall(r'(?<=<)(.*?)(?=>)', to)[0]
                    new_message['to'].append({'name': name, 'email': email})
                except:
                    new_message['to'].append({'name': None, 'email': to})

        # get names and emails of cc
        if header['name'] == 'Cc':
            val = header['value']
            tos = val.split(',')
            for to in tos:
                try:
                    name = to[:to.index('<')].strip()
                    email = re.findall(r'(?<=<)(.*?)(?=>)', to)[0]
                    new_message['to'].append({'name': name, 'email': email})
                except:
                    new_message['to'].append({'name': None, 'email': to})

        # get names and emails of bcc
        if header['name'] == 'Bcc':
            val = header['value']
            tos = val.split(',')
            for to in tos:
                try:
                    name = to[:to.index('<')].strip()
                    email = re.findall(r'(?<=<)(.*?)(?=>)', to)[0]
                    new_message['to'].append({'name': name, 'email': email})
                except:
                    new_message['to'].append({'name': None, 'email': to})

        #  get the subject
        if header['name'] == 'Subject':
            new_message['subject'] = header['value']

        # get the name and email of sender
        if header['name'] == 'From':
            val = header['value']

            try:
                name = val[:val.index('<')].strip()
                email = re.findall(r'(?<=<)(.*?)(?=>)', val)[0]

                new_message['from'] = email
                new_message['from_name'] = name
            except:
                new_message['from'] = val
    if new_message.get('from') and new_message.get('subject') and new_message.get('to') and new_message.get('date') and new_message.get('id') and new_message.get('history_id'):
        return new_message
    else:
        return None