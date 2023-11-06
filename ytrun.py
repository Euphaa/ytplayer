import subprocess
import os
import sys

if not os.path.isfile('./yt-dlp.exe'):
    print('yt-dlp.exe not found. needs to be in root folder.')
    sys.exit()

def runDlp(link):
    return subprocess.run(f'yt-dlp.exe {link}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

def delVidFiles():
    fileTypes = ['.mp4', ]
    with os.scandir() as entries:
        for entry in entries:
            if not entry.is_file(): continue
            if not entry.name.endswith('.mp4'): continue
            os.remove(entry.name)
    print(f'deleted all videos of type .mp4')

while True:
    link = input('paste link here, or type "clear" to delete all the videos stored; use "stop" to exit.\n>')
    match link:
        case 'clear':
            delVidFiles()
            continue
        case 'stop':
            sys.exit()

    result = runDlp(link)
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
    
    subprocess.run(f'start {newname}', shell=True)
