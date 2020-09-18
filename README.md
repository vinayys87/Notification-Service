# Generic Notification System

Beta version of Notification system can be used for sending out communication via Email, Slack and SMS. The code is written in Python 3

# Prerequisites : 
  - Windows / Linux / Mac OS
  - Python 3 or higher
  - SMTP installed in the server / External SMTP 
  - Provider for SMS service

# Setup Python
  - Setup steps for Linux : https://docs.python.org/3/using/unix.html 
  - Setup steps for Windows : https://docs.python.org/3/using/windows.html#python-launcher-for-windows
  - Setup steps for Mac OS : https://docs.python.org/3/using/mac.html

# Python Modules installation
  - phonenumbers : https://pypi.org/project/phonenumbers/

# Code setup
  - Download the Notification git repository to your system
  - Make sure you have installed all the prerequisite modules
  - Please provide the path of notify.json for the variable 'path' in config.ini

# Publish Notification
Notification publication system requires an input : Bulk , Indivisual
  - Indivisual notification Publish
    After we give an input as 'Indivisual', the code prompts for type of notification. For each of the notification types, it requires specific inputs. 
    
    - Email
    - Slack
    - SMS
    
    Once you provide the input, it requests for next set. Currently we have configured to publish 3 notification at a time. 
  - Bulk Notification Publish
    Bulk notification relies on the input provided in the notify.json. Bulk notification loads the data from the json file,parse it and perform appropriate actions
