import smtplib
import re
from configparser import ConfigParser
import phonenumbers
import json


def sendemailnotification(emaildict):
    #This function is used to send email Notification. We check the email regex and send the email via local smtp

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    sender = emaildict['emailfrom']
    if (re.search(regex, sender)):
        print(f"Valid from Email {sender}")
    else:
        return (f"Invalid From Email {sender}", emaildict)
    receivers = emaildict['emailto']
    if (re.search(regex, receivers)):
        print(f"Valid from Email {receivers}")
    else:
        return (f"Invalid From Email {receivers}", emaildict)

    try:
        # smtpObj = smtplib.SMTP('localhost')
        # smtpObj.sendmail(sender, receivers, message)
        print(f"Successfully sent email with message {emaildict['message']}")
        return (1)

    except Exception as e:
        return (f"Error: unable to send email with exception {e} ", emaildict)


def sendSlackNotification(slackdict):
    #This function is used to publish messages to valid slack channels
    # valid channels :  ['#validchannel', '#validchannel2', '#channel3', '#hello']
    slackConfigur = ConfigParser()
    slackConfigur.read('config.ini')
    validChannel = slackConfigur.get('slack', 'slackChannelList')
    if (slackdict['slackchannelname'] in validChannel):
        print('Valid slack channel')
        return (1)
    else:
        print("Invalid slack channel")
        return ("Invalid slack channel", slackdict)


def sendSmsNotification(smsdict):
    numParse = phonenumbers.parse(smsdict['phoneNumber'], None)
    if (phonenumbers.is_valid_number(numParse) is True):
        print("Valid Phone number. Sms successfully sent")
        return (1)
    else:
        print("Invalid phone number")
        return ("Invalid phone number ", smsdict)


def sendnotification(resultDict):
    #print (resultDict)
    successnotify = {}
    failurenotify = {}
    for i in range(len(resultDict)):
        # print(resultDict[i])
        if (resultDict[i]["notifytype"] == "email"):
            result = sendemailnotification(resultDict[i])
            if (result == 1):
                successnotify[i] = resultDict[i]
            else:
                failurenotify[i] = result
        elif (resultDict[i]["notifytype"] == "slack"):
            result = sendSlackNotification(resultDict[i])
            if (result == 1):
                successnotify[i] = resultDict[i]
            else:
                failurenotify[i] = result
        elif (resultDict[i]["notifytype"] == "sms"):
            result = sendSmsNotification(resultDict[i])
            if (result == 1):
                successnotify[i] = resultDict[i]
            else:
                failurenotify[i] = result
    print("Notification Successfully sent  : ", successnotify)
    print("Notification Failed to sent  : ", failurenotify)
    getInputs()

def sendBulkNotification(resultDict):
    #print (resultDict)
    successnotify = {}
    failurenotify = {}
    for (key,value) in resultDict.items():
        #print("Key: " + key)
        #print("Value: " + str(value))
        #print (value["notifytype"] )
        if (value["notifytype"] == "email"):
            result = sendemailnotification(value)
            if (result == 1):
                successnotify[key]=value
            else:
                failurenotify[key] = result
        elif (value["notifytype"] == "slack"):
            result = sendSlackNotification(value)
            if (result == 1):
                successnotify[key]=value
            else:
                failurenotify[key] = result
        elif (value["notifytype"] == "sms"):
            result = sendSmsNotification(value)
            if (result == 1):
                successnotify[key]=value
            else:
                failurenotify[key] = result
    print("Notification Successfully sent  : ", successnotify)
    print("Notification Failed to sent  : ", failurenotify)


def getInputs():
    notifyDict = {}
    #print(len(notifyDict))
    while (len(notifyDict) < 3):
        print('\n' * 1)
        notifytype = input("Enter the notification type : ").lower()
        if (notifytype == "email"):
            emailfrom = input("Enter From address : ").lower()
            emailto = input("Enter To address : ").lower()
            notifytype = "email"
            subject = input("Enter email subject : ").lower()
            message = input("Enter email message : ").lower()
            notifyDict[len(notifyDict)] = {'emailfrom': emailfrom, 'emailto': emailto, 'notifytype': notifytype,
                                           'subject': subject, 'message': message}
        elif (notifytype == "slack"):
            emailto = input("Enter To address : ").lower()
            slackchannelname = input("Enter Slack channel name : ").lower()
            url = "www.slack.com"
            message = input("Enter Slack message : ").lower()
            notifytype = "slack"
            notifyDict[len(notifyDict)] = {'emailto': emailto, 'slackchannelname': slackchannelname, 'url': url,
                                           'message': message, 'notifytype': notifytype}
        elif (notifytype == "sms"):
            phoneNumber = input("Please enter valid phone number : ")
            notifytype = "sms"
            messageSms = input("Please enter the message : ")
            notifyDict[len(notifyDict)] = {'phoneNumber': phoneNumber, 'notifytype': notifytype,
                                           'messageSms': messageSms}

        else:
            print(
                f"Given input {notifytype} is wrong. Please provide notification type from the list : Email, Slack or SMS")
    # print (notifyDict)
    print("Please wait while we are processing the request")
    sendnotification(notifyDict)

def getBulkInputs():
    #with open('C:\\Users\\Vinay.Mohan1\\PycharmProjects\\EY\\notification\\notify.json') as json_file:
    bulkconfigur = ConfigParser()
    bulkconfigur.read('config.ini')
    validpath = bulkconfigur.get('bulkjsonpath', 'path')
    with open(validpath) as json_file:
        data = json.load(json_file)
    print(data)
    sendBulkNotification(data)
    #print (data)


'''
-----Start of Program----
We have 2 modes for notification publication. Indivisual and Bulk. 
Indivisual : We need to provide valid inputs for each required field for notification type
Bulk : We load the system with prepopulated json data to publish notification.
'''

print("Hello Welcome to Notification channel")
inputType = ""
while inputType != "indivisual" or inputType != "bulk":
    print ("\n"*1)
    inputType = input("Please provide the type of notification data : Bulk or Indivisual ").lower()
    if (inputType == "indivisual"):
        getInputs()
    elif (inputType == "bulk"):
        getBulkInputs()

