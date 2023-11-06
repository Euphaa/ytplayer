import subprocess
import os
import sys
from time import sleep
import pyperclip
import asyncio
import aioconsole

vidNum = 0

if not os.path.isfile('./yt-dlp.exe'):
    print('yt-dlp.exe not found. needs to be in root folder.')
    sys.exit()

def delVidFiles():
    # fileTypes = ['.mp4', ]
    with os.scandir() as entries:
        for entry in entries:
            if not entry.is_file(): continue
            if not entry.name.endswith('.mp4'): continue

            os.remove(entry.name)
    global sessionHistory
    sessionHistory = []
    print(f'deleted session history and all videos of type .mp4')

delVidFiles()

async def main():
    await asyncio.gather(clipboardOpener(), inputHandler())

async def clipboardOpener():
    global sessionHistory
    sessionHistory = []
    while True:
        clipboard = pyperclip.paste()
        if clipboard in sessionHistory:
            sleep(.5)
            continue

        if 'youtube.com/watch' in clipboard:
            print('playing from clipboard')
            playFromLink(clipboard)
            sessionHistory.append(clipboard)
        sleep(1)
            

async def inputHandler():
    pass
    while True:
        link = aioconsole.ainput('paste link here, or type "clear" to delete all the videos stored; use "stop" to exit.\n>')
        match link:
            case 'c':
                delVidFiles()
                continue
            case 'stop':
                sys.exit()
        
        playFromLink(link)

def runDlp(link):
    global vidNum
    vidNum += 1
    print('running dlp ---------------------------------------------------------')
    return subprocess.run(f'yt-dlp.exe -o {vidNum}.mp4 {link}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)



def playFromLink(link):
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
        return

    subprocess.run(f'start {name}', shell=True)

if __name__ == "__main__":
    asyncio.run(main())