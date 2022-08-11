import os
import json
import subprocess
from random import randint
import xerox

workingDirectory = "/home/fred/Python/MinecraftSoundLoader/"

def cutOffFile(filepath):
    return filepath[:-len(filepath.split("/")[-1]) - 1]



noSetup = True
for root, dir, files in os.walk(workingDirectory):
    if 'setup.json' in files:
        noSetup = False

if noSetup:
    setupDictionary = {'randomOrder':True}
    print('welcome to the minecraft sound pack creator!')
    input("your first step is to move the template folder from this directory to your resourcepack directory! press ENTER after you're done: ")
    input("now rename the folder to what you want your sound pack to be called. after that press ENTER: ")
    satisfied = False
    while not satisfied:
        setupDictionary['soundDirectory'] = input("ok, now please enter the absolute file path of the sound packs assets folder. it should look something like '...../.minecraft/resourcepacks/YourSoundpack/assets/' : ")
        for root2, dir2, files2 in os.walk(setupDictionary['soundDirectory']):
            if not 'sounds' in files2:
                satisfied = True
        if not satisfied:
            print("sorry, that didn't work. Please check and try again.")
    satisfied = False
    while not satisfied:
        setupDictionary['indexDirectory'] = input("ok, great! now I just need your minecraft main assets folder. it should look like '...../.minecraft/assets/' : ")
        for root2, dir2, files2 in os.walk(setupDictionary['indexDirectory']):
            if not 'objects' in files2:
                satisfied = True
        if not satisfied:
            print("sorry, that didn't work. Please check and try again.")
    print("alright, the setup is done!")
    setupFile = open(workingDirectory + 'setup.json', 'w')
    json.dump(setupDictionary, setupFile)
    setupFile.close()
else:
    print('Good day! I hope you are keen to record some minecraft sounds!')
    setupFile = open(workingDirectory + 'setup.json', 'r')
    setupDictionary = json.load(setupFile)
    setupFile.close()

indexFile = open(setupDictionary['indexDirectory'] + 'indexes/1.19.json')
indexes = json.load(indexFile)
fileNumber = len(indexes['objects'].keys())
commandsFile = open(workingDirectory + "commands.txt", 'r')
commands = commandsFile.read()
commandsFile.close()

quit = False
while not quit:

    done = False
    fastMode = False
    ready = False
    while not ready:
        answer = input("please type in a command. If you don't know any, you can type in 'help' to see useful commands: ")
        if answer == 'help':
            print(commands)
        elif answer == 'start' or answer == '':
            print("alright, let's start!")
            ready = True
        elif answer == 'completion':
            print(len(completedSounds), 'sounds completed')
            print(len(indexes['objects']), 'sounds in total')
            print(str(round(len(completedSounds) / len(indexes['objects']) * 100, 1)) + '% completed!')
        elif answer == 'list':
            for sound in completedSounds:
                print(' -> '.join(sound.split('/')[2:])[:-5])
        elif answer == 'fastmode' or answer == 'gotta go fast':
            fastMode = True
            ready = True
        elif answer == 'order':
            setupDictionary['randomOrder'] = not setupDictionary['randomOrder']
            print("sound loading order set to: " + ['sorted', 'random'][setupDictionary['randomOrder']])
        elif answer == 'quit':
            print("ok then. I'll see you next time!")
            ready = True
            done = True
            quit = True
        else:
            print("sorry, I don't know that command.")

    while not done:

        completedSoundsFile = open(workingDirectory + 'completedSounds.txt', 'r+')
        completedSounds = completedSoundsFile.read().splitlines()

        ind = 0
        completed = True
        while completed:
            if setupDictionary['randomOrder']:
                randomFileName = list(indexes['objects'].keys())[randint(0, fileNumber)]
            else:
                randomFileName = list(indexes['objects'].keys())[ind]
            if randomFileName in completedSounds:
                completed = True
                print('got that already!')
            elif randomFileName[-2] == "g":
                completed = False
            ind += 1

        randomFileHash = indexes['objects'][randomFileName]['hash']

        for root, dir, files in os.walk(setupDictionary['indexDirectory'] + 'objects/'):
            if randomFileHash in files:
                path = os.path.join(root, randomFileHash)

        randomFilePath = cutOffFile(randomFileName)
        directories = randomFilePath.split('/')
        ind = 0
        for dir in directories:
            checkingDir = setupDictionary['soundDirectory'] + '/'.join(directories[:ind])
            if not dir in os.listdir(checkingDir):
                os.mkdir(checkingDir + '/' + dir)

            ind += 1

        if not fastMode:
            answered = False
            while not answered:
                answer = input('should I reveal the sound to you? y/n: ')
                if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == '':
                    print("the sound is:")
                    soundString = ''
                    for dir in randomFileName.split('/')[2:]:
                        soundString += dir + ' -> '
                    print(soundString[:-8])
                    answered = True
                elif answer == 'n' or answer == 'N' or answer == 'no':
                    print("ok, good luck guessing!")
                    answered = True
                else:
                    print("sorry, you will have to repeat that.")

            input("The file path you should save your recorded sound in will be copied to your clipboard! press ENTER to start audacity: ")

        xerox.copy(setupDictionary['soundDirectory'] + randomFileName, xsel=True)
        subprocess.run(['audacity', path])

        if not fastMode:
            answered = False
            while not answered:
                answer = input('did you record the sound well and saved it as the original? y/n: ')
                if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == '':
                    print('great job! I will mark it as done!')
                    completedSoundsFile.write('\n' + randomFileName)
                    completedSounds.append(randomFileName)
                    answered = True
                elif answer == 'n' or answer == 'N' or answer == 'no':
                    print("that's ok, maybe next time. I won't mark that as done, so you can do it later!")
                    answered = True
                else:
                    print("sorry I didn't understand that, you need to say yes or no.")
            print('so...')
        else:
            completedSoundsFile.write('\n' + randomFileName)
            completedSounds.append(randomFileName)

        answered = False
        while not answered:
            answer = input('are you ready for the next one? y/n: ')
            if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == '':
                print("great! let's go!")
                answered = True
            elif answer == 'n' or answer == 'N' or answer == 'no':
                print("ok...")
                done = True
                answered = True
            else:
                print("sorry, you will have to repeat that.")

        completedSoundsFile.close()

setupFile = open(workingDirectory + 'setup.json', 'w')
json.dump(setupDictionary, setupFile)
setupFile.close()