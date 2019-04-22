from Command     import Command
from DataStorage import CredentialList

creds = CredentialList()

#####################################################

print('\n'*100)

print(Command.leet_sauce)
while True:
    continueLastSession = raw_input('Would you like to import the data from the last session? (y/n) ')
    if continueLastSession == 'y':
        session_file = raw_input('What file would you like to load from? ')
        print('Starting new session from ' + session_file)
        try:
            creds.import_file(session_file)
            break
        except IOError:
            print("That was an invalid path. Please try again.")
        break
    elif continueLastSession == 'n':
        print('Starting new Session...' )
        break
    else:
        print('That was invalid input. Try again. ')


###########################

while(True):
    new_cmd = Command.get_command(creds)
    new_cmd.execute_command()
