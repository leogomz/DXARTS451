# -*- coding: utf-8 -*-
import os, subprocess, random

#pi rootDirectory = "/media/pi/5448-0E6A/"
#pi ffmpgDirectory = "/usr/bin/ffmpeg"
rootDirectory = "/Users/leonardgomez/Desktop/451a3/"
ffmpegDirectory = "/usr/local/bin/ffmpeg"

#Creates a single sequence or "channel" for a jazz track. Takes in a few parameters
#Takes in a folder of files to choose from, two names for output files, a boolean value for whether
#a new random is generated for amount of silence between samples and two int values for the range of time values for the random
def createJazzTrack(folder, outfile1, outfile2, newRand, time1, time2):
    file_count = getFolderLength(folder)
    r1 = random.randint(1, file_count)
    r2 = random.randint(time1, time2)
    f = open(outfile1 , "w")
    f.truncate(0)
    trackTime = 0.0
    #track time should be a minute or 60 seconds so the loop goes up to 80 to allow for a little extra and then is shortened later
    while trackTime < 80.0:
        f.writelines("file " + "'" + folder + str(r1) + ".wav" + "'" + '\n')
        #generate silence or white space between files dependent on generated value
        for j in range(0, r2):
            f.writelines("file " + "'" + rootDirectory + "s.wav" + "'" + '\n')
        trackTime = trackTime + getTime(folder + str(r1) + ".wav") + r2
        #generate new random value rather than the same value for consistent rhythm
        if newRand == True:
            r1 = random.randint(1, file_count)
            r2 = random.randint(time1, time2)
    subprocess.Popen([ffmpegDirectory, "-y", "-f", "concat", "-safe", "0", "-i", rootDirectory + outfile1, "-c", "copy", rootDirectory + outfile2], \
                     universal_newlines=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=False)
    #different volume dependent on folder that files are pooled from
    if folder == rootDirectory + "1/":
        subprocess.Popen([ffmpegDirectory, "-y", "-i", rootDirectory + outfile2, "-af", '"volume=0.75"', rootDirectory + outfile2], \
                        stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=False)     
    #different volume dependent on folder that files are pooled from
    if folder == rootDirectory + "2/":
        subprocess.Popen([ffmpegDirectory, "-y", "-i", rootDirectory + outfile2, "-af", '"volume=3.75"', rootDirectory + outfile2], \
                         stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=False)
    #different volume dependent on folder that files are pooled from
    if folder == rootDirectory + "rhythm/":
        subprocess.Popen([ffmpegDirectory, "-y", "-i", rootDirectory + outfile2, "-af", '"volume=4.75"', rootDirectory + outfile2], \
                         stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=False)           
    f.close()

#Creates a single audio track or channel that serves as a loop
#Takes in the loop folder as a parameter, and two output files
def createJazzLoop(folder, outfile1, outfile2):
    file_count = getFolderLength(folder)
    r1 = random.randint(1,file_count - 1)
    f = open(outfile1 , "w")
    f.truncate(0)
    trackTime = 0.0
    #track time should be a minute or 60 seconds so the loop goes up to 80 to allow for a little extra and then is shortened later
    while trackTime < 80.0:
        f.writelines("file " + "'" + folder + str(r1) + ".wav" + "'" + '\n')
        trackTime = trackTime + getTime(folder + str(r1) + ".wav")
    subprocess.Popen([ffmpegDirectory, "-y", "-f", "concat", "-safe", "0", "-i", rootDirectory + outfile1, "-c", "copy", rootDirectory + outfile2], \
                     universal_newlines=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=False)
    subprocess.Popen([ffmpegDirectory, "-y", "-i", rootDirectory + outfile2, "-af", '"volume=1.50"', rootDirectory + outfile2], \
                     stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=False)    

    f.close()
    
#Gets the time value for whatever passed in file. Returns a floating point of the time value
def getTime(file):
    command = '/usr/local/bin/ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(file)
    output = ""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    return float(output)

#Gets the length of the passed in folder in the directory and returns an int of whatever the length is
def getFolderLength(folder):
    path, dirs, files = os.walk(folder).next()
    file_count = len(files) - 1
    return file_count

#Creates the audio sequences by calling both the createJazzTrack and createJazzLoop functions
#Creates 3 tracks and pools from different folders based on an algorithm that creates a more
#intense and wild sequence everytime the loop iterates
def createAudioSequences():
    for i in range (1,4):
        #string to build up ffmpeg command to call later
        inputsCommand = '-y '
        #int to keep track of how many audio channels have been made
        inputsCount = 0
        #There are two main pools of jazz samples to choose from, one is more tame and soft while the other is aggressive and avant garde
        #The algorithm pools from the softer pool only on the first iteration and the value k keeps track of which folder to choose from based on i
        #After the first iteration, start creating loops
        k = 1
        if i > 1 :
            createJazzLoop(rootDirectory + "loop/", "lout" + str(i) + ".txt", "louts" + str(i) + ".wav")
            inputsCommand = inputsCommand + "-i " + rootDirectory + "louts" + str(i) + ".wav "
            inputsCount = inputsCount + 1
        #On second iteration incorporate vocal track with more frequency
        if i == 2 :
            createJazzTrack(rootDirectory + "vocal/", "vocal" + str(i) + ".txt", "vocal" + str(i) + ".wav", True, 10, 20)
            inputsCommand = inputsCommand + "-i " + rootDirectory + "vocal" + str(i) + ".wav "
            inputsCount = inputsCount + 1
        #On third iteration incorporate vocal track with more frequency
        if i == 3 :
            k = 2
            createJazzTrack(rootDirectory + "vocal/", "vocal" + str(i) + ".txt", "vocal" + str(i) + ".wav", True, 1, 4)
            inputsCommand = inputsCommand + "-i " + rootDirectory + "vocal" + str(i) + ".wav "
            inputsCount = inputsCount + 1
        #Creates more jazzTracks dependent on how many times the initial loop has iterated
        for j in range(1, (i * 2) + 1):
            createJazzTrack(rootDirectory + str(k) + "/", str(i) + str(j) + ".txt", str(i) + str(j) + ".wav", True, j, j * 2)
            inputsCommand = inputsCommand + "-i " + rootDirectory + str(i) + str(j) + ".wav "
            inputsCount = inputsCount + 1
            if i == 1 :
                createJazzTrack(rootDirectory + str(k) + "/", str(i) + str(j) + "2.txt", str(i) + str(j) + "2.wav", True, j, j * 2)
                inputsCommand = inputsCommand + "-i " + rootDirectory + str(i) + str(j) + "2.wav "               
                inputsCount = inputsCount + 1
            if i == 3 :
                createJazzTrack(rootDirectory + str(k) + "/", str(i) + str(j) + "2.txt", str(i) + str(j) + "2.wav", True, 1, 4)
                inputsCommand = inputsCommand + "-i " + rootDirectory + str(i) + str(j) + "2.wav "               
                inputsCount = inputsCount + 1
        createJazzTrack(rootDirectory + "rhythm/", "rout" + str(i) + ".txt", "routs" + str(i) + ".wav", False, i, i * 2)
        inputsCommand = inputsCommand + "-i " + rootDirectory + "routs" + str(i) + ".wav "
        inputsCount = inputsCount + 1

        inputsCommand = '/usr/local/bin/ffmpeg ' + inputsCommand + '-filter_complex amix=inputs=' + str(inputsCount) + ':duration=first:dropout_transition=0 ' + rootDirectory + 'out' + str(i) + '.wav'
        print (inputsCommand) 
        subprocess.Popen(inputsCommand, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=True)

#Create 3 video sequence based on a gradual transistion to more close and intimate and "happy" shots with initial shots being more distant and neutral
#Pooling from 3 different folders of videos labeled 1, 2, 3, all matching the intended transition which then correspondes with the for loop                         
def createVideoSequences():
    for i in range(1, 4):
        file_count = getFolderLength(rootDirectory + str(i + 2))
        r1 = random.randint(1,file_count - 1)
        #keep track of old random to avoid repeats
        r2 = r1
        outfile1 = str(i + 2) + ".txt"
        outfile2 = str(i) + ".mp4"
        f = open(outfile1, "w")
        f.truncate(0)
        trackTime = 0.0
        vidCount = 0
        #track time should be a minute or 60 seconds so the loop goes up to 80 to allow for a little extra and then is shortened later
        while trackTime < 80.0:
            f.writelines("file " + "'" + rootDirectory + str(i + 2) + "/" + str(r1) + ".mp4" + "'" + '\n')
            trackTime = trackTime + getTime(rootDirectory + str(i + 2) + "/" + str(r1) + ".mp4")
            r1 = random.randint(1,file_count - 1)
            while r1 == r2:
                r1 = random.randint(1,file_count - 1)
            r2 = r1
        subprocess.Popen([ffmpegDirectory, "-y", "-f", "concat", "-safe", "0", "-i", rootDirectory + outfile1, "-c", "copy", rootDirectory + outfile2], \
                         universal_newlines=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=False)
        f.close()

#Combines the audio and video tracks generated from the other functions
#Creates three combined audio and video track based on a for loop
def combineAudioVideo():
    for i in range(1, 4):
        command = '/usr/local/bin/ffmpeg -y -i ' + rootDirectory+ str(i) + '.mp4' + ' -i ' + rootDirectory + 'out' + str(i) + '.wav' + ' -map 0:v:0 -map 1:a:0 -b:a 192k -shortest ' + rootDirectory + "v" + str(i) + '.mp4'
        subprocess.check_output(command, universal_newlines=True, shell=True, stderr=subprocess.STDOUT)

#Shortens the generated output from combineAudioVideo to be the intended 60 seconds per video
#Creates three shortened videos based on a for loop                         
def shortenAudioVideo():
    for i in range(1, 4):
        command = '/usr/local/bin/ffmpeg -ss 0 -y -i ' + rootDirectory + 'v' + str(i) + '.mp4' + ' -c copy -t 60 ' + rootDirectory + 'cut' + str(i) + '.mp4'
        subprocess.check_output(command, universal_newlines=True, shell=True, stderr=subprocess.STDOUT)        

#Combines the shortened videos from the shortenAudioVideo function to have a final three minute video
def concatenateAudioVideoSequences():
    outfile1 = "final.txt"
    outfile2 = "final.mp4"
    f = open(outfile1, "w")
    f.truncate(0)
    for i in range(1, 4):
        f.writelines("file " + "'" + rootDirectory + "cut" + str(i) + ".mp4" + "'" + '\n')

    subprocess.Popen([ffmpegDirectory, "-y", "-f", "concat", "-safe", "0", "-i", rootDirectory + outfile1, "-c", "copy", rootDirectory + outfile2], \
                     universal_newlines=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=False)
    f.close()
                     
createAudioSequences()
createVideoSequences()
combineAudioVideo()
shortenAudioVideo()
concatenateAudioVideoSequences()
