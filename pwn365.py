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
