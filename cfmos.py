#!/usr/bin/env python

# Check For Mail On Server
# sends email notice to given email address when there is new mail on the server
# email notice contains message on server
# @rdar

import smtplib
import cfmos_config

def main():
    mailbox_path = '/var/mail/' + cfmos_config.re_mailbox_name()
    user_home_path = '/home/' + cfmos_config.re_mailbox_name()
    fo = open(mailbox_path,"r")
    s = fo.read()
    messages = s.split("From:")
    count = len(messages)
    fo.close #we don't need to leave this file open any longer
    #get difference in length to determine how many new messages there are
    try:
        records = open(user_home_path+'/cfmos_records.txt',"r+") 
    except:
        #file doesn't exist yet, let's create it
        records = open(user_home_path+'/cfmos_records.txt',"w+") 
    prev_record = records.read()
    count_list = prev_record.split(":")
    prev_count = count_list[1] if count_list and len(count_list) > 1 and count_list[1].isdigit() else False
    diff_count = count - int(prev_count) if prev_count else 0
    if diff_count > 0:
        # We only need to do anything if there is at least 1 new message
        notification_string = ''
        lc = 1
        while lc <= diff_count:
            if messages[-lc].find('sending email') < 0:
                #here we are collecting all new messages except "sending email" messages
                notification_string += messages[-lc]
            lc += 1
        send_email(notification_string)
    #write new count
    records.seek(0)
    records.write('count:'+str(count))
    records.close()
    return


def send_email(message):
    #send email notification
    if message:
        email = cfmos_config.send_email_to()
        notification = smtplib.SMTP('localhost')
        head = """From: Notification of mail on server<do-not-reply@cfmos.com>
    To: <%s>
    Subject: New mail on server

    """ % (email)
        notification.sendmail('do-not-reply@cfmos.com',email,message)
    return

#run main function
if __name__ == "__main__":
    main()
