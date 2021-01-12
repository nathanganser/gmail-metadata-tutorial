from get_clean_message_data import extract_data


def ongoing_gmail_sync(service):
    pageToken = None
    history_id = "some recent history id"

    # Get current situation
    history = service.users().history().list(userId="me", historyTypes='messageAdded',
                                             startHistoryId=history_id, pageToken=pageToken).execute()

    # Check if there has been a change
    if history:
        current_history_id = history_id
        print(f'Data has been imported up to: {current_history_id}')
        last_history_id = history.get('historyId')
        print(f'Inbox is already at level   : {last_history_id}')
        if last_history_id > current_history_id:
            # Import the new messages
            for change in history:
                email_id = change['messagesAdded'][0]['message']['id']
                thread_id = change['messagesAdded'][0]['message']['threadId']
                import_me = 'INBOX' or 'SENT' in change.get('messagesAdded')[0].get('message').get('labelIds')
                # you might not want to import messages that went to spam for example
                if import_me:
                    message = service.users().messages().get(userId="me", id=email_id, format='metadata').execute()

                    # but this message still needs cleaning, you can use our home made function
                    clean_message = extract_data(message)
                    # now you can do what you want, clean_message contains the sender, receiver, date, labels and
                    # subject


def initial_gmail_sync(service):
    pageToken = None
    messages_left = True

    # Get messages
    while messages_left:
        messages = service.users().messages().list(userId="me", pageToken=pageToken).execute()
        pageToken = messages.get('nextPageToken')
        # do something with the messages! Importing them to your database for example
        for message in messages:
            email_id = message['id']
            dirty_message = service.users().messages().get(userId="me", id=email_id, format='metadata').execute()
            clean_message = extract_data(dirty_message)
            # and now you can do what you want
            # clean_message contains 'from', 'subject', 'to', 'date', 'id' and 'history_id'

        if not pageToken:
            messages_left = False
            # you've reached the end of the inbox!
