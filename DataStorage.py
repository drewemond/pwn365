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

import re

# Credential format: [Username, Password, Domain, Verified, email_pull, AD Groups]
class Credential:
    """Object that manages all of the information that a single credential contains.

    """

    def __init__(self, username, password, domain, verified, email_pull, ad_groups):
        """Creates a credential instance.

        :param username:   (String)  The username
        :param password:   (String)  The Password for the user
        :param domain:     (String)  The Domain that the user is in (google.com)
        :param verified:   (Boolean) Tells whether or not the credentials have been verified; true, if the credential pair is valid
        :param email_pull: (Boolean) Tells whether or not you have already pulled the user's email
        :param ad_groups:  (String)  The Active Directory groups that the user is in (Will come from Azure)
        """
        self.username   = username
        self.password   = password
        self.domain     = domain
        self.verified   = verified
        self.email_pull = email_pull
        self.ad_groups  = ad_groups

    def display_cred (self):
        """Displays the credential in a readable format.

        """
        print(self.username + ", " + self.password + ", " + self.domain + ", " + str(self.verified) + ", " + str(self.email_pull) + ", " + self.ad_groups)

    def export(self):
        """Returns a readable string with all of the credential's information.

        :return: (String) Contains all of the relevant information
        """
        return (self.username + ", " + self.password + ", " + self.domain + ", " + self.verified + ", " + self.email_pull + ", " + self.ad_groups + "\n")


class CredentialList:
    """Contains a list of credentials, and anything that needs to be performed on said list.

    """

    def __init__(self):
        """Initializes CredentialList instance

        """
        self.master_list = {}

    def remove_user(self, username):
        """Removes a given user from the master_list.

        :param username: (String) The user that you wish to remove.
        """
        del self.master_list[user]

    def search_user(self, username):
        """Returns a Boolean stating whether or not a credential is present in master_list

        :param username: (String) The username you are searching for.

        :return: (Boolean) Whether or not the username was found.
        """
        try:
            self.master_list[username]
            return True
        except KeyError:
            return False

    def get_password(self, username):
        """Find the password for a specified user.

        :param username: (String) The username of the user you wish to retrieve the password for
        :return:         (String) The password of the user, returns 'None' if the user is not found
        """
        try:
            return self.master_list[username].password
        except KeyError:
            print('Could not find "password" for user: ' + username + ', username not in list.')

    def set_password(self, username, password):
        """Manually change the password for specified user.

        :param username: (String) The username of the user you wish to change
        :param password: (String) The password that you want to replace
        """
        try:
            self.master_list[username].password = password
        except KeyError:
            print('Could not set "password" for user: ' + username + ', username not in list.')

    def set_verify(self, username, validity):
        """Manually change whether or not the credential is verified.

        :param username: (String)  The user whose validity you wish to change
        :param validity: (Boolean) What you want to change the specified user's validity to
        """
        try:
            self.master_list[username].verified = verified
        except KeyError:
            print('Could not set "verified" for user: ' + username + ', username not in list.')

    def get_domain(self, username):
        """Find the domain for a specified user.

        :param username: (String) The username of the user you wish to retrieve the domain for
        :return:         (String) The domain of the user
        """
        try:
            return self.master_list[username].domain
        except KeyError:
            print('Could not find "domain" for user: ' + username + ', username not in list.')

    def set_domain(self, username, domain):
        """Manually set the domain for a specified user.

        :param username: (String) The user that you want to edit
        :param domain:   (String) What you want to change the specified user's domain to
        """
        try:
            self.master_list[username].domain = domain
        except KeyError:
            print('Could not set "domain" for user: ' + username + ', username not in list.')

    def add_cred(self, username, password, domain, verified, email_pull, ad_groups):
        """Adds a new credential to the list.

        :param username:   (String)  The username
        :param password:   (String)  The Password for the user
        :param domain:     (String)  The Domain that the user is in (google.com)
        :param verified:   (Boolean) Tells whether or not the credentials have been verified; true, if the credential pair is valid
        :param email_pull: (Boolean) Tells whether or not you have already pulled the user's email
        :param ad_groups:  (String)  The Active Directory groups that the user is in (Will come from Azure)
        """
        newCred = Credential(username, password, domain, verified, email_pull, ad_groups)
        newCred.display_cred()
        self.master_list[username] = newCred

    def display_all(self):
        """Displays all of the stored credentials in a pretty format.

        """
        print("        User       ||     Password     ||      Domain      ||  Verified  ||  Email Pull  ||     AD Groups      ")
        print("-------------------++------------------++------------------++------------++--------------++--------------------")
        for cred in self.master_list.keys():
            cred_info =[self.master_list[cred].username,
                        self.master_list[cred].password,
                        self.master_list[cred].domain,
                        self.master_list[cred].verified,
                        self.master_list[cred].email_pull,
                        self.master_list[cred].ad_groups]
            print('{0:18} || {1:16} || {2:16} || {3:10} || {4:12} || {5:25}'.format(*cred_info))

    def export_file(self, file_name):
        """Exports all of the credentials currently stored to a specified file.

        :param file_name: (String) The name of the file that you wish to import credentials from
        """
        try:
            with open(file_name, 'w') as f:
                for user in self.master_list.keys():
                    f.write(self.master_list[user].export())
        except IOError:
            print("That directory doesn't exist. Please try again.")


    # TODO: Return Instance of CredentialList
    def import_file(self, file_name):
        """Takes a CSV as input and populates the master_list with the credentials.

        :param file_name: (String) The name of the file that you wish to import credentials from
        """
        with open(file_name, 'r') as f:
            for line in f:
                data = re.sub(r'\n', '', line).split(',')
                print(data)
                for num in range(0,len(data)):
                    data[num] = data[num].strip()
                self.add_cred(*data)
