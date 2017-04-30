# phantominvites
Script to automate sending of Facebook page invites using Python and Mechanize/Selenium.

### Usage
`python phantominvites.py [Facebook Page ID] [Account List] [Max Threads]`

[Facebook Page ID] The ID of the page to send invites for.

[Account List] List of accounts, passwords, and user-agents to be used for sending invites.

[Max Threads] Maximum amount of threads for multithreading support.


### Userlist format
Userlist should be a textfile formatted as:

person@example.com::facebookpassword::useragent

#### Disclaimer
I wrote this years ago and it may or may not be functional still, I take no responsibility whatsoever for any consequences that may arise from using it, use at your own risk.
I mainly put it up as an example of using Selenium/Mechanize to automate processes on websites that explicitly seek to prevent such automation.
