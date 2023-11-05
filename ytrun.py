import subprocess
import os
import sys

if not os.path.exists('./vid'):
    os.makedirs('./vid')

if not os.path.isfile('./yt-dlp.exe'):
    print('yt-dlp.exe not found. needs to be in root folder.')
    sys.exit()

while True:
    link = input('paste link here, or type "clear" to delete all the videos stored:\n> ')
    if link.lower() == 'clear':
        print("this hasn't been made a thing yet sry ):")
        os.walk()
        continue

    result = subprocess.run(f'yt-dlp.exe {link}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    lines = result.stdout.split('\n')
    name = ''
    
    for line in lines:
        print(line)
            
        if '[download] Destination: ' in line:
            name = line.removeprefix('[download] Destination: ')
            break

    
        
    if not os.path.isfile(name):
        print('error finding or downloading video')
        continue
    
    newname = name.replace(' ', '')
    os.rename(name, newname)
    print(f'start {newname}')
    
    subprocess.run(f'start {newname}', shell=True)
