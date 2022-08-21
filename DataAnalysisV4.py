import os
import os.path
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
import time
import random
import datetime
from datetime import date

def SearchFile(Query, PathToFile):
    Query = str(Query)
    m = open(PathToFile, 'r')
    ReadoutOfInformation = m.readlines()
    HeaderFound = False
    for f in ReadoutOfInformation:
        if HeaderFound == True:
            m.close()
            return(f.replace('\n',''))
        if Query + '\n' == f:
            HeaderFound = True
    m.close()

y_axis = []
x_axis = []
key_list = []

user = '' #change this to the name of the user that will run this program.
path = '' #change this to be the path that the program will be running this.

os.chdir(path + 'Details/')

dates = []
CardNames = []
prices = []
#File correction cannot handle files with duplicate entries
#File correction will also fail if the longest file does not have a correct header

print("Only 75 days can be proccessed into a single image, please enter the LAST day you want to include.")
FinalDate = int(input())
print("(Optional), enter a earlier date if you want less than 75 days of info, if left blank it defaults to 20 days after your initial date.") #it doesn't yet pranked
InitialDate = input()

MaxFileSize = 0
MaxFileName = 0
for file in os.listdir(path + 'Details/'):
    dates.append(int(file))
    f = open(str(file), 'r')
    contents = f.readlines()
    if len(contents)-2 > MaxFileSize:
        MaxFileSize = len(contents)-2
        MaxFileName = str(file)
    f.close()
dates.sort()

counter = 0
for date in dates:
    if date == FinalDate:
        InitialDate = dates[counter-20]
    counter += 1

print(InitialDate)

print("MaxFileSize " + str(MaxFileSize) + " in " + MaxFileName)

#exit() #Stage 1

for file in os.listdir(path + 'Details/'):
    #print(file)
    f = open(str(file), 'r')
    contents = f.readlines()
    #print(contents)
    m = open(str(MaxFileName), 'r')
    MaxContents = m.readlines()
    f.close()
    m.close()

    try:
        int(contents[0].replace("\n",""))
        #print("contents[0] is a number for: " + str(file))
        HeaderType = "int"
    except:
        if str(file) == MaxFileName:
            print("chosen max file: " + str(file) + " has a incorrect header, please manually correct this.")
            exit()
        print("contents[0] is NOT a number for: " + str(file))
        HeaderType = "string"

    if len(contents)-2 < MaxFileSize or HeaderType == "string": #MaxFileSize only counts the data not total length so we need to subtract the length of the header
        f = open(str(file), 'w')
        f.write(MaxContents[0])
        f.write('\n')

        #for entry in range(0, len(MaxContents) - len(contents)): #Prevents index out of range errors when checking for missing cards
        #    contents.append('BLANK')

        MissingInfo = {}
        print("correcting: " + str(file))
        print(len(contents))
        print(len(MaxContents))
        UnsortedContents = contents
        UnsortedMaxContents = MaxContents
        BlankOffset = 0
        for index in range(0, len(MaxContents)-len(contents)):
            contents.append("BLANK")
            BlankOffset += 1
        counter = 0

        for item in MaxContents:
            if counter == 0 or counter == 1:
                counter+=1
                continue

            #print("item from MaxContents: " + str(item))
            if (counter % 2) == 0: #If the item is a card not price
                print("item: " + item.replace('\n', '') + " has been determined to be a card")
                IsDupe = False
                for card in contents: #Check if card already exists in CombinedData
                    print("card to be checked against " + item.replace("\n","") + ": " + contents[counter].replace("\n", ""))
                    if card == item:
                        print(item.replace("\n", "") + " already present detected!")
                        IsDupe = True
                        break
                if IsDupe == False:
                    print(item.replace("\n","") + " is missing from " + str(file))
                    MissingInfo[item] = 'None\n'
            counter += 1

        print("MissingInfo: ", MissingInfo)

        Info = {}
        print(contents)
        counter = 0
        for item in range(0,int(len(contents)/2-BlankOffset/2)+1):
            print("counter: ", counter)
            if counter == 0 or counter == 1:
                counter += 1
                continue
            Info[contents[counter]] = contents[counter+1]
            counter += 2
        print("Info: ", Info)

        for key in MissingInfo.keys():
            Info[key] = MissingInfo[key]

        print("Full Info: ", Info)

        SortedList = {}
        SortingList = []

        for key in Info.keys():
            SortingList.append(key)

        SortingList.sort()

        for key in SortingList:
            SortedList[key] = Info[key]

        print("SortedList: ", SortedList)

        for key in SortedList.keys():
            f.write(key)
            f.write(SortedList[key])

        f.close()

#exit() #Stage 2

#for file in dates:
#    x = open(str(file), 'r')
#    contents = x.readlines()
#    #print(contents)
#    if len(contents) < int(contents[0].replace('\n', '')):
#        print(str(file) + " has corrupted data skipping...")
#        continue
#    counter = 0
#    for f in contents:
#        #print(str(counter) + " Outer Loop")
#        if counter == 1 or counter == 0:
#            counter += 1
#            continue
#        if (counter % 2) == 0:
#            card = f
#            CardNames.append(card.replace('\n', ''))
#            #print(card)
#
#
#        if (counter % 2) != 0:
#            price = f
#            #if counter == 3:
#                #print(prices)
#            if price.replace('\n', '') == 'None':
#                prices.append(np.nan)
#                #print(prices)
#            else:
#                prices.append(float(price.replace('\n', '')))
#            #print(f)


#print("dates: ", dates)
#print("CardNames: ", CardNames)
#print("prices: ", prices)

#Operating directory is in /Details
DayPricesDict = {}
stringdates = [] #used farther down when graphing actually happens
for day in dates:
    if day > InitialDate and day <= FinalDate:
        print(str(day) + " within InitialDate and FinalDate.")
        stringdates.append(str(day)[4:-2] + '-' + str(day)[-2:])
    else:
        #print(str(day) + " NOT witin InitialDate and FinalDate, DATA EXPUNGED")
        continue
    f = open(str(day), 'r')
    contents = f.readlines()
    TmpDayPrices = []
    FileLength = int(contents[0].replace('\n',''))
    counter = 0
    for price in contents:
        if counter == 0 or counter == 1:
            counter += 1
            continue
        else:
            #print(price)
            if price.replace('\n', '') == 'None':
                TmpDayPrices.append(np.nan)
            else:
                TmpDayPrices.append(price.replace("\n", ""))
        counter += 1
    #print("TmpDayPrices: ", TmpDayPrices)
    DayPricesDict[day] = TmpDayPrices


print("\nDayPriceDict: ", DayPricesDict)

#exit() #Stage 3

CombinedData = {}
for day in DayPricesDict:
    print("\nprocessing: " + str(day))
    #print(DayPricesDict[day])
    counter = 0
    for item in DayPricesDict[day]:
        #print("item: " + str(item))
        if (counter % 2) == 0: #If the item is a card not price
            #print("item: " + str(item) + " has been determined to be a card")
            IsDupe = False
            for card in CombinedData: #Check if card already exists in CombinedData
                #print("card to be checked against " + item + ": " + card)
                if card == item:
                    #print("Dupe detected!")
                    IsDupe = True
                    break
            if IsDupe == False: #If it doesn't add it and a corresponding list
                print("adding " + item + " to CombinedData")
                CombinedData[item] = []
            elif CombinedData == {}:
                print("adding " + item + " to EMPTY CombinedData")
                CombinedData[item] = []
        else:
            card = DayPricesDict[day][counter-1]
            price = DayPricesDict[day][counter]
            #print("Card: " + card)
            #print("List of x card: ", CombinedData[card])
            #print("Price of x card: ", price)
            #print("CombinedData: ", CombinedData)
            CombinedData[card].append(float(price))
        counter += 1

print(CombinedData)

for card in CombinedData.keys():
    print(card + " has " + str(len(CombinedData[card])) + " prices.")

#exit() #Stage 4

#stringdates = []
#for date in dates:
#    stringdates.append(str(date)[4:-2] + '-' + str(date)[-2:])

print(stringdates)

plt.rcParams["figure.figsize"] = (len(stringdates),10)

for card in CombinedData.keys():
    #print("len(stringdates): " + str(len(stringdates)))
    #print("len(CombinedData[card]): " + str(len(CombinedData[card])))
    #print("card: ", card)
    #print("CombinedData[card]: ", CombinedData[card])
    plt.plot(stringdates, CombinedData[card], label = card)

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('gpu pricing')
plt.legend()
plt.savefig(path + 'Gpu_Price_Graph.png', dpi=300)

