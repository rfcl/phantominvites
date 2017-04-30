import cookielib
import mechanize
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Process
import sys
from os import getpid

#Basic variables
def getVars():
    global userid,page_id,accounts,url,maxthreads
    try:
        page_id = sys.argv[1]
    except(IndexError):
        print "Missing parameters.\nUsage: workingphantom.py [Facebook Page ID] [Account List] [Max Threads]"
    try:
        accounts = sys.argv[2]
    except(IndexError):
        print "Missing parameters.\nUsage: workingphantom.py [Facebook Page ID] [Account List] [Max Threads]"
    try:
        maxthreads = sys.argv[3]
    except(IndexError):
        print "Missing parameters.\nUsage: workingphantom.py [Facebook Page ID] [Account List] [Max Threads]"
    url = "https://m.facebook.com/"+ page_id + "/invite_friends/?start=0&cancel_uri=/profile.php?id=343434";
    userid = 0

def parseAccounts(accounts):
    users = list()
    accs = open(accounts, 'r').read()
    rows = accs.split("\n")
    for row in rows:
        data = row.split("::")
        if (len(data)<3):
            continue
        email = data[0]
        password = data[1]
        useragent = data[2]
        account = [email,password,useragent]
        users.append(account)
    return users

def daddyIssues():
    approval_code = raw_input("This account has two-step authentication and requires a 6 digit security code.\nPlease enter security code from phone or press enter to skip this account: ")
    if (approval_code == ""):
        userid = userid + 1
        run(fb_accs,userid)
    br.select_form(nr=0)
    br.form['approvals_code'] = approval_code
    print "Sending approval code..."
    br.submit()
    print "Sent."
    if (br.response().read().find("Remember Browser") > -1):
        br.select_form(nr=0)
        br.form['name_action_selected'] = ["save_device"]
        print "Telling Facebook to remember device."
        br.submit()
        try:
            br.select_form(nr=0)
        except mechanize._mechanize.FormNotFoundError:
            return
        print "Facebook says thanks."
        br.submit()
    if (br.response().read().find("This is Okay") > -1):
        br.select_form(nr=0)
        print "Facebook is worried about unusual activity, dealing with that shit."
        br.submit()
        br.select_form(nr=0)
        br.submit()
    return 0

def facebookAuth(email,password,useragent):
    global br,cookies
    #Initialize browser simulator
    cookies = cookielib.LWPCookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cookies)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.set_handle_refresh(False)
    br.addheaders = [('User-agent', useragent)]

    #Load the page
    print "Beginning authentication."
    r = br.open(url)

    #Fun stuff
    br.select_form(nr=0)
    br.form['email'] = email
    br.form['pass'] = password
    print "Credentials submitted."
    br.submit()
    if (br.response().read().find("Enter Security Code to Continue") > -1):
        daddyIssues()
    del br
    return 0

def sendInvites(useragent):
    try:
        print "Finally, back to work."
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (useragent)
        # driver = webdriver.PhantomJS(desired_capabilities=dcap)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("phantomjs.page.settings.userAgent",useragent)
        driver = webdriver.Firefox(profile)

        print "Loading cookies."
        driver.get("http://facebook.com/adasdsdsa3232432543332.php")
        for c in cookies:
            driver.add_cookie({'name':c.name, 'value':c.value, 'path':'/', 'domain':c.domain})

        print "Getting friend count"
        url = "https://m.facebook.com/send_page_invite/?pageid=" + page_id + "&offset=0&count=3000"
        driver.get(url)
        login_check = driver.page_source
        print login_check
        sys.exit()
        friends = len(driver.find_elements_by_class_name("ce"))
        print "Friends: " + str(friends)

        print "Loading invite page"
        url = "https://m.facebook.com/"+ page_id + "/invite_friends/?start=0&cancel_uri=/profile.php?id=343434";
        driver.get(url)
        print "Inviting everyone."
        cnt = 0
        start = 0
        for x in xrange(friends):
            print "Page suggested to" + str(x) + "friends."
            button = driver.find_elements_by_class_name("bi")[cnt]
            button.click()
            cnt = cnt + 1
            if (cnt == 9):
                start = start + 10
                url = "https://m.facebook.com/"+ page_id + "/invite_friends/?start=" + str(start) + "&cancel_uri=/profile.php?id=343434";
                driver.get(url)
                cnt = 0

    except(KeyboardInterrupt):
        choice = raw_input("\nKeyboard interruption detected. Would you like to terminate the program or just skip this user?\Please select 1 (terminate) or 2 (skip)")
        if (choice == "1"):
            sys.exit()
        elif (choice == "2"):
            try:
                userid = (userid + 1)
            except UnboundLocalError:
                userid = 1
            run(fb_accs,userid)
    try:
        userid = userid + 1

    except(UnboundLocalError):
        userid = 1
    return 0

def run(fb_acc):
    facebookAuth(fb_acc[0],fb_acc[1],fb_acc[2])
    sendInvites(fb_acc[2])

def initialize():
    global fb_accs
    getVars()
    fb_accs = parseAccounts(accounts)
    initThreads()

def initThreads():
    for fb_acc in fb_accs:
        p = Process(target=run, args=(fb_acc,))
        p.start()


initialize()
