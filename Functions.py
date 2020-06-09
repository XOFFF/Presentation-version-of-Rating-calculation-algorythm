import datetime
import json

from pip._vendor import requests


def addNewUserInfoToListOfUsers(typeOfRoom, listOfUsers, currentUserId, lastTime):
    print('Add')
    print(lastTime)
    if typeOfRoom == 1:
        listOfUsers.append(
            dict({'User id': currentUserId,
                  'Time': {'On work': 0, 'On rest': 0},
                  'Last time': {'On work': 0, 'On rest': 0},  # lastTime
                  'Rating': 0}))
    elif typeOfRoom == 2:
        listOfUsers.append(
            dict({'User id': currentUserId,
                  'Time': {'On work': 0, 'On rest': 0},
                  'Last time': {'On work': 0, 'On rest': 0},
                  'Rating': 0}))

def changeUserLastTimeFromListOfUsers(typeOfRoom, listOfUsers, currentUserId, lastTime):
    for userInfo in listOfUsers:
        if userInfo['User id'] == currentUserId:
            if typeOfRoom == 1:
                userInfo['Last time']['On work'] = lastTime
            if typeOfRoom == 2:
                userInfo['Last time']['On rest'] = lastTime


def setRoomWithType(eachFile, url_path):
    url = url_path + 'get-rooms'
    x = requests.get(url)
    listOfRooms = json.loads(x.content)
    fileName = eachFile.split('_')
    fileName = fileName[1].split('.')
    for roomInfo in listOfRooms:
        print(roomInfo['roomid'])
        print('fileName id', fileName[0])
        if int(fileName[0]) == roomInfo['roomid']:
            print('Roomtype', roomInfo['roomtype'])
            return roomInfo['roomtype']
            break



def changeUserRatingByControlQuastion(listOfUsers, dateOfCacheFiles, url_path):
    # file = open("C:/Users/marke/Desktop/cache files/users_answers.json", )
    # dataWithAnswers = json.load(file)
    # file.close()
    # print(dataWithAnswers)

    url = url_path + 'get-daily-task-status'
    print('dateOfCacheFiles', dateOfCacheFiles)

    for userInfoFromList in listOfUsers:
        # for userAnswers in dataWithAnswers:
        print(str(userInfoFromList['User id']))
        myobj = '{"userid": "' + str(userInfoFromList['User id']) + '", "date": "' + str(dateOfCacheFiles) + '"}'
        print('myobj', myobj)
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        listOfUserInfo = json.loads(x.content)
        print('Hey! userid', listOfUserInfo['userid'], 'workfinished', listOfUserInfo['workfinished'])
        if userInfoFromList['User id'] == listOfUserInfo['userid'] and listOfUserInfo['workfinished'] == 1:
            userInfoFromList['Rating'] = 3


def findDifference(firstTime, lastTime):
    first_time = datetime.datetime.strptime(firstTime, '%Y-%m-%d %H:%M:%S.%f')
    later_time = datetime.datetime.strptime(lastTime, '%Y-%m-%d %H:%M:%S.%f')
    print('Difference between', firstTime, 'and', lastTime, 'is', (later_time - first_time).total_seconds())
    return (later_time - first_time).total_seconds()


def addTime(typeOfRoom, waitTime, listOfUsers, currentUserId, difference, firstTime, lastTime, lastItem, firstItem):
    if typeOfRoom == 1:
        for userInfo in listOfUsers:
            # Find user with current id in item
            if userInfo['User id'] == currentUserId:
                print('Time in list before changes', userInfo['Time']['On work'])
                # Check if we don't get any last time by user before
                if userInfo['Last time']['On work'] == 0:
                    changeUserLastTimeFromListOfUsers(typeOfRoom, listOfUsers, currentUserId, lastTime)
                # Check if last time we recognized in the same typeOfRoom and the item is not last and if spent time from last this user face recognition till now is more then 30 min (1800 sec)
                if lastTime != userInfo['Last time']['On work'] and lastItem is False and 0 < findDifference(userInfo['Last time']['On work'], firstTime) <= waitTime:
                    difference += findDifference(userInfo['Last time']['On work'], firstTime)
                    print('Add time when not recognized', difference)
                # Check if last item at the same time is first item and if spent time from last this user face recognition till now is more then 30 min (1800 sec)
                elif lastItem is True and 0 < findDifference(userInfo['Last time']['On work'], firstTime) <= waitTime: # and lastTime == firstItem[1]
                    difference += findDifference(userInfo['Last time']['On work'], firstTime)
                    print('Add time when not recognized', difference)
                # else:
                #     difference += findDifference(userInfo['Last time']['On work'], firstTime)
                #     print('Add time when not recognized', difference)
                print('Sum the difference', userInfo['Time']['On work'], '+', difference)
                userInfo['Last time']['On work'] = lastTime
                userInfo['Time']['On work'] += difference

    elif typeOfRoom == 2:
        for userInfo in listOfUsers:
            if userInfo['User id'] == currentUserId:
                if userInfo['Last time']['On rest'] == 0:
                    changeUserLastTimeFromListOfUsers(typeOfRoom, listOfUsers, currentUserId, lastTime)
                if lastTime != userInfo['Last time']['On rest'] and lastItem is False and 0 < findDifference(userInfo['Last time']['On rest'], firstTime) <= waitTime:
                    difference += findDifference(userInfo['Last time']['On rest'], firstTime)
                    print('Add time when not recognized', difference)
                elif lastItem is True and 0 < findDifference(userInfo['Last time']['On rest'], firstTime) <= waitTime:
                    difference += findDifference(userInfo['Last time']['On rest'], firstTime)
                    print('Add time when not recognized', difference)
                # else:
                #     difference += findDifference(userInfo['Last time']['On rest'], firstTime)
                #     print('Add time when not recognized', difference)
                print('Sum the difference', userInfo['Time']['On rest'], '+', difference)
                userInfo['Last time']['On rest'] = lastTime
                userInfo['Time']['On rest'] += difference


def saveIntoOutputFile(listOfUsers):
    data = []
    for userInfo in listOfUsers:
        data.append({
            'User id': userInfo['User id'],
            'User id': userInfo['User id'],
            'Time spent on work': userInfo['Time']['On work'],
            'Time spent on rest': userInfo['Time']['On rest'],
            'Rating by the day': userInfo['Rating']
        })
        print(userInfo)
    with open('cache files\\cache_output.json', 'w') as outfile:
        json.dump(data, outfile, indent=3)

def setNewDataAboutUserToDB(listOfUsers, dateOfCacheFiles, url_path):
    for userInfoFromList in listOfUsers:
        url = url_path + 'update-rating'
        myobj = '{"userid": "' + str(userInfoFromList['User id']) + '", "timeonrest": "' + str(userInfoFromList['Time']['On rest']) + '", "timeonwork": "'+ str(userInfoFromList['Time']['On work']) + '", "rating": "'+ str(userInfoFromList['Rating']) + '", "date": "' + str(dateOfCacheFiles) + '"}'
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data=myobj, headers=headers)
        listOfUserInfo = json.loads(x.content)
        print(listOfUserInfo)
        # print('Hey! userid', listOfUserInfo['userid'], 'timeonrest', listOfUserInfo['timeonrest'], 'timeonwork', listOfUserInfo['timeonwork'], 'rating', listOfUserInfo['rating'])