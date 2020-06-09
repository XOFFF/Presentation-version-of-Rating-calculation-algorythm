import json
import datetime

from pip._vendor import requests

from Person import Person
import Functions
import FormulaCalculator
from os import walk
import time

listOfUsers = []
listOfUserId = []

date = 0
# typeOfRoom = 0

hoursAtWork = 8.0

waitTime = 1800  # seconds
startWorkTime = '17:56'  # hours and minutes
startWorkDays = [0, 1, 2, 3, 4, 5]  # Monday is 0, Tuesday is 1 ...

folder_path = 'cache files/cache/'
localhost = 'localhost:3000'
url_path = 'http://' + localhost + '/api/rating/'

f = []
for (dirpath, dirnames, filenames) in walk(folder_path):
    f.extend(filenames)
    print(f)


def getTrainDataFile():
    trainFile = open(r'C:/Users/marke/Downloads/server/uploadedData/training/recognizer/trainingData.yml', "wb")  # открываем файл для записи, в режиме wb
    ufr = requests.get("http://26.26.247.174:3000/api/camera/get-ml-file")  # делаем запрос
    trainFile.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
    trainFile.close()


def job():
    for eachFile in f:
        print(
            'Start to analyze file ............................................................................................................................................')
        # text = f.read()
        # Opening JSON file
        file = open(folder_path + eachFile, )

        dataFromJSON = json.load(file)
        file.close()

        # Implementing variables
        listOfUsersCache = []
        currentUserId = 0
        firstTime = 0
        lastTime = 0
        lastItem = False

        # listOfRooms = []
        # listOfRoomType = []
        typeOfRoom = 0
        dateOfCacheFiles = 0

        for item in dataFromJSON:
            listOfUsersCache.append((item['id'], item['Date time']))
            #     print(item)
            if item == dataFromJSON[0]:
                # Code to set room type to each room id
                typeOfRoom = Functions.setRoomWithType(eachFile, url_path)

                # typeOfRoom = item['Room id']
                # print(typeOfRoom)

            # Set dateOfCacheFiles
            if dateOfCacheFiles == 0:
                date = item['Date time'].split(' ')
                dateOfCacheFiles = date[0]
                print('lol')

        for eachItem in listOfUsersCache:
            print(eachItem)
            # Check if last item
            if eachItem == listOfUsersCache[-1]:
                lastItem = True
            # if first item from file
            if currentUserId == 0:
                currentUserId = eachItem[0]
                if eachItem[0] not in listOfUserId:
                    print('wow, new id!')
                    listOfUserId.append(currentUserId)
                firstTime = eachItem[1]
                lastTime = eachItem[1]

            if len(listOfUsers) == 0:
                Functions.addNewUserInfoToListOfUsers(typeOfRoom, listOfUsers, currentUserId, lastTime)

            # Functions.changeUserLastTimeFromListOfUsers(typeOfRoom, listOfUsers, currentUserId, lastTime)
            # Check if it is not first item from file  AND  if we got new user id in the item
            if eachItem[0] != currentUserId and len(listOfUsers) != 0: # and lastItem is False
                # Get the difference from first and last value with same user id from current item in file
                # print('First time:', firstTime)
                # print('Last time:', lastTime)
                difference = Functions.findDifference(firstTime, lastTime)
                # print('Difference:', difference)
                # difference = difference.total_seconds()
                # print('Difference in seconds:', difference)
                # Check if got the same user id before
                if currentUserId not in listOfUserId:
                    # Add new user to listOfUsers
                    listOfUserId.append(currentUserId)

                    Functions.addNewUserInfoToListOfUsers(typeOfRoom, listOfUsers, currentUserId, lastTime)
                    print('wow, new id!')
                # Now we set the difference time to exactly right typeOfRoom to the user in listOfUsers
                Functions.addTime(typeOfRoom, waitTime, listOfUsers, currentUserId, difference, firstTime, lastTime, lastItem, listOfUsersCache[0])
                # last sets after we got new User id in the item
                currentUserId = eachItem[0]
                # if eachItem != listOfUsersCache[-2] and eachItem != listOfUsersCache[-1]:
                firstTime = eachItem[1]

            # if last item from file
            if lastItem is True:
                print('last value', eachItem[1])

                # if listOfUsersCache[0] != listOfUsersCache[-1]:
                print('first diff')
                # set some variables for calculations for last item
                currentUserId = eachItem[0]
                lastTime = eachItem[1]
                # Now we set the difference time to exactly right typeOfRoom to the user in listOfUsers
                difference = Functions.findDifference(firstTime, lastTime)  # .total_seconds()
                print('second diff')
                Functions.addTime(typeOfRoom, waitTime, listOfUsers, currentUserId, difference, firstTime, lastTime, lastItem, listOfUsersCache[0])

            lastTime = eachItem[1]

    # Final steps
    Functions.changeUserRatingByControlQuastion(listOfUsers, dateOfCacheFiles, url_path)
    for user in listOfUsers:
        user['Rating'] = FormulaCalculator.calculateByFormula(hoursAtWork, user)

    Functions.saveIntoOutputFile(listOfUsers)

    Functions.setNewDataAboutUserToDB(listOfUsers, dateOfCacheFiles, url_path)
    for i in listOfUsers:
        print(i)


# Start work by time and day

jobTime = str(datetime.datetime.strptime(startWorkTime, '%H:%M').time())
a = jobTime.split(':')
jobTime = a[0] + ':' + a[1]
# day = ''
while True:
    timeNow = datetime.datetime.now().strftime('%H:%M')
    dayOfTheWeekNow = datetime.datetime.now().weekday()
    print('timeNow', timeNow)
    print('jobTime', jobTime)
    print('dayOfTheWeekNow', dayOfTheWeekNow)
    print('startWorkDays', startWorkDays)
    # print('day', day)
    print('dayOfTheWeekNow', dayOfTheWeekNow)
    if str(timeNow) == jobTime and dayOfTheWeekNow in startWorkDays: #and day != dayOfTheWeekNow
        print('WOW')
        job()
        getTrainDataFile()
    time.sleep(30)
    day = dayOfTheWeekNow


# job()
# trainFile = open(r'C:/Users/marke/Downloads/server/uploadedData/training/recognizer/trainingData.yml', "wb")  # открываем файл для записи, в режиме wb
# ufr = requests.get("http://26.26.247.174:3000/api/camera/get-ml-file")  # делаем запрос
# trainFile.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
# trainFile.close()

# getTrainDataFile()
# job()




# for user in listOfUsers:
#     user['Rating'] = FormulaCalculator.calculateByFormula(hoursAtWork, user)
# Functions.saveIntoOutputFile(listOfUsers)
# Functions.setNewDataAboutUserToDB(listOfUsers, date)