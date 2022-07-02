from multiprocessing.pool import TERMINATE
import time
import hashlib
from urllib.request import urlopen, Request
from plyer import notification
import sys

def sanitize(url_input):
    """
    Given a url (str), sanitize it and make it processable
    """

    # Sanitizing the input (might not include https://)
    if url_input[:8] != 'https://':
        if url_input[:4] == 'www.':         # Input: www.google.com
            url_input = url_input[4:]
            url_input = 'https://' + url_input
        elif url_input[:7] != 'http://':                               # Input: google.com
            url_input = 'https://' + url_input

    return url_input

print()
print('###############################################################')
print()
print(r'8888888888 888888888')
print(r'888        888')
print(r'888        888')
print(r'8888888    8888888b.  .d8888b  88888b.   8888b.  88888b.d88b.')
print(r'888             "Y88b 88K      888 "88b     "88b 888 "888 "88b')
print(r'888        Y88b  d88P      X88 888 d88P 888  888 888  888  888')
print(r'888         "Y8888P"   88888P" 88888P"  "Y888888 888  888  888')
print(r'                               888')
print(r'                               888')
print(r'                               888')    
print()
print('###############################################################')

# Asking how many urls to search
while True:
    try:
        num_input = int(input('\n[🔢] How many URL do you want to check? Type here: '))
        break
    except Exception:
        print('[❌ ERROR] Not an integer number')

# Asking the URL to check
if num_input == 1:
    url_input = input('[🌐] What URL do you want to check? Type here: ')
else:
    url_input = []
    for i in range(num_input):
        this_url = input(f'[🌐] URL #{i+1}: ')
        url_input.append(this_url)

# Loop to trap user until the URL is correct
while True:
    if type(url_input) != list:
        url_input = sanitize(url_input)

        # Requesting the url
        url = Request(url_input, headers={'User-Agent': 'Mozilla/5.0'})
        
        # Reading the response
        try:
            response = urlopen(url).read()
            break
        except Exception:
            url_input = input('[❌ ERROR] Something went wrong. Type the URL again: ')
    else:
        urls = []
        responses = []
        for this_url in url_input:
            this_url = sanitize(this_url)
        
            # Requesting the url
            url = Request(this_url, headers={'User-Agent': 'Mozilla/5.0'})
            urls.append(url)
            
            # Reading the response
            try:
                response = urlopen(url).read()
                responses.append(response)
            except Exception:
                print('[❌ ERROR] Something went wrong')
                sys.exit()
        break

# Asking how often to check
time_input = input('[⏰] How often do you want to check? Type in seconds: ')

while True:
    try:
        time_input = int(time_input)
        break
    except ValueError:
        time_input = input('[❌ ERROR] Something went wrong. Please type an integer value: ')
 
# Using the hash to monitor changes 
if num_input == 1:
    currentHash = hashlib.sha224(response).hexdigest()
else:
    currentHashes = []
    for response in responses:
        currentHash = hashlib.sha224(response).hexdigest()
        currentHashes.append(currentHash)

print("\n[🚀 RUNNING]")

# Keeping track of the number of times checked
i = 1
while True:
    print(f'\t[⏱️ TIMES CHECKED] {i}', end='\r')
    if num_input == 1:
        try:
            # Reading the response
            response = urlopen(url).read()
            
            # Create current hash
            currentHash = hashlib.sha224(response).hexdigest()
            
            # Waiting for the set amount of time
            time.sleep(time_input)
            
            # Reading the response again
            response = urlopen(url).read()
            
            # Create a new hash
            newHash = hashlib.sha224(response).hexdigest()
    
            # Check whether the hash has changed or not
            if newHash == currentHash:
                i += 1
                continue
            else:
                print("\t[✅ CHANGE DETECTED]")
                # Giving a notification to the user
                notification.notify(
                    title = '[✅ CHANGE DETECTED]',
                    message = f'Something changed in "{url}", go check it out!',
                    app_icon = './imgs/icon.ico',
                    timeout = 10
                )
                break
        # Handle exceptions
        except Exception:
            print("[❌ ERROR] An error occured")
            break
    else:
        try:
            for response in responses:
                # Reading the response
                response = urlopen(url).read()
                
                # Create current hash
                currentHash = hashlib.sha224(response).hexdigest()
                
                # Reading the response again
                response = urlopen(url).read()
                
                # Create a new hash
                newHash = hashlib.sha224(response).hexdigest()
        
                # Check whether the hash has changed or not
                if newHash != currentHash:
                    print("\t[✅ CHANGE DETECTED]")
                    # Giving a notification to the user
                    notification.notify(
                        title = '[✅ CHANGE DETECTED]',
                        message = f'Something changed in "{url}", go check it out!',
                        app_icon = './imgs/icon.ico',
                        timeout = 10
                    )
                    sys.exit()
            # Waiting for the set amount of time
            time.sleep(time_input)
            i += 1
        # Handle exceptions
        except Exception:
            print("[❌ ERROR] An error occured")
            break