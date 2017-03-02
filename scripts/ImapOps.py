"""
This module contains functions related to IMAP Operation. Below Functions are defined
1- Connection to IMAP server
2- Parse the body of Unseen Email
3- Get the attachment and parse the attachment.
"""

from config_file import *
import imaplib
import email
import re
import re

def open_connection():
    try:
        print 'Connecting to ' +  imap_server
        connection = imaplib.IMAP4_SSL(imap_server)
    except Exception as e:
        print "Not able to make connection to IMAP server. Please imap server url"
        exit(1)
    else:
        try:
            connection.login(username, password)
        except Exception as e:
            print "Authentication failure. Please check Username/Password"
            exit(1)

        print "Connected to " + imap_server
        return connection
def parse_unseen_mails():
    """This method will look for unseen emails and parse the data given in body of email"""
    conn = open_connection()
    conn.select('INBOX')
    retcode, msgs = conn.search(None, "UNSEEN")
    total_msgs =  msgs[0].split()
    for msg in total_msgs:
        status, data = conn.fetch(msg, '(RFC822')
        if status == 'OK':
            raw_data = email.message_from_string(data[0][1])




if __name__ == '__main__':
    print "Main Function"
    conn = open_connection()
    print conn
