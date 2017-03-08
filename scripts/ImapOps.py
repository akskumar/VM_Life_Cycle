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


def open_connection():
    try:
        print 'Connecting to ' + imap_server
        connection = imaplib.IMAP4_SSL (imap_server)
    except Exception as e:
        print "Not able to make connection to IMAP server. Please imap server url"
        exit (1)
    else:
        try:
            connection.login (username, password)
        except Exception as e:
            print "Authentication failure. Please check Username/Password"
            exit (1)

        print "Connected to " + imap_server
        return connection


def parse_unseen_mails():
    """This method will look for unseen emails and parse the data given in body of email"""
    conn = open_connection ()
    conn.select ('INBOX')
    retcode, msgs = conn.search (None, "UNSEEN")
    print "unseen_messages: {0}".format(msgs)
    vm_configs = []
    if retcode and msgs:
        for msg in msgs[0].split():
            print "Processsing for {0} mail".format(msg)
            data_dict = {}
            response, data = conn.fetch (msg, '(RFC822)')
            conn.store(msg,'+FLAGS', r'(\Seen)')
            raw_data = email.message_from_string (data[0][1])
            from_addr = re.search (r'[\w\.-]+@[\w\.-]+', raw_data['from']).group (0)
            to_addr = re.search (r'[\w\.-]+@[\w\.-]+', raw_data['to']).group (0)
            subject = raw_data['subject']
            data_dict['from_addr']  = from_addr
            data_dict['to_addr'] = to_addr
            data_dict['subject'] = subject
            print "From: {0}, To: {1}, subject: {2}".format (from_addr, to_addr, subject)
            print "Is {0} is multipart: {1}".format(msg, raw_data.is_multipart())
            if not raw_data.is_multipart ():
                body = filter (lambda x: x != '', raw_data.get_payload ().split ('\r\n'))
            elif raw_data.is_multipart ():
                for part in raw_data.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload().split ('\r\n')
            print str (body)
            for line in body:
                    if line.startswith ('OS'):
                        data_dict['OS'] = line.split (':')[1].strip ()
                    if line.startswith ('HDD'):
                        data_dict['HDD'] = line.split (':')[1].strip ()
                    if line.startswith ('VCPU'):
                        data_dict['VCPU'] = line.split (':')[1].strip ()
                    if line.startswith ('RAM'):
                        data_dict['RAM'] = line.split (':')[1].strip ()
            vm_configs.append(data_dict)
        return vm_configs
    conn.close()

if __name__ == '__main__':
    print "Main Function"
    vm_config_parameters = parse_unseen_mails()

    print str(vm_config_parameters)
