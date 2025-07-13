from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from datetime import date
import time
import os


path = "/app" #The path you're storing the program in
user = "" #The name of the user you are running this with

chrome_options = Options()
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--enable-crash-reporter")
chrome_options.add_argument("--headless")
#chrome_options.add_argument('--ignore-certificate-errors')
#chrome_options.add_argument('--allow-running-insecure-content')
driver = webdriver.Chrome(options=chrome_options)

#Ebay's advanced settings don't show up if the window is too small.
driver.set_window_size(1024, 768)

#exit()

inputs = [] #inputs are now taken from the inputs.txt file

f = open("inputs.txt", "r")
for line in f.readlines():
    if line == "" or line == "\n":
        continue
    inputs.append(line.replace("\n",""))

driver.get("https://www.ebay.com/")
time.sleep(1)

#Advanced Settings button click
driver.find_element("xpath", '//*[@id="gh-f"]/div[2]/a').click()
time.sleep(1)

#Sold Listings Only button click
driver.find_element("xpath", """//*[@id="s0-1-17-5[1]-[2]-LH_Sold"]""").click()
time.sleep(1)

#Do a initial search to apply filter
InitialSearch = driver.find_element("xpath", """//*[@id="_nkw"]""")
InitialSearch.clear()
InitialSearch.send_keys("Graphics Card")
InitialSearch.submit()
time.sleep(1)

#initialsearch = driver.find_elements("xpath", '/html/body/header/table/tbody/tr/td[5]/form/table/tbody/tr/td[1]/div[1]/div/input[1]')

#for item in initialsearch:
#    item.clear()
#    item.submit()

#f = open("/app/Details/cat.txt", "a")
#f.write("boo!\n")
#f.close()

os.chdir(path + '/Details/')
if os.path.exists(str(date.today())) == True:
    os.remove(str(date.today()))
f = open(str(date.today()).replace('-',''), 'w')
f.write(str(len(inputs)*2) + "\n")
f.write("\n")
os.chdir(path)


FirstRun = True
for item in inputs:
    time.sleep(1)
    print("item: " + item)
    input = item
    CombinedAverages = 0
    TestLoop = 0

    while TestLoop < 1: # I don't know why there are multiple loops every search returns the same thing?
        TestLoop = TestLoop + 1

        if FirstRun == True:
            search = driver.find_element("xpath",'//*[@id="gh-ac"]') #yes this used to matter and now it doesn't, but I'm not changing it

            search.clear()

            search.send_keys(input + " graphics card")

            search.submit()
            
            FirstRun = False
        else: 
            search = driver.find_element("xpath",'//*[@id="gh-ac"]')

            search.clear()

            search.send_keys(input + " graphics card")

            search.submit()
	
        time.sleep(5)
        prices = driver.find_elements(By.XPATH, ".//span[@class='s-item__price']/span[@class='POSITIVE']")

        AddedPrices = 0
        NumberOfPrices = 0
        counter = 0
        #print("PRICES: " + str(prices[0]))
        #driver.get_screenshot_as_file(path)
        for data in prices:
            if counter <= 20: #there used to be a AND here making it only do every other item I removed this and it sill seems to work
                print("Added price:" + str(data.text))
                #if data.text.find(" ") != -1 or data.text.find("") != -1:
                #    print("Canceled line: " + str(data.text))
                #    continue
                if data.text.find("to") != -1:
                    print("Canceled line: " + str(data.text))
                    continue
                elif float((data.text).replace('$', '').replace(',', '')) > 4500.00:
                    print("Canceled line: " + str(data.text))
                    continue
                elif data.text.find("HDD") != -1 or data.text.find("SSD") != -1:
                    print("Canceled line: " + str(data.text))
                    continue
                else:
                    AddedPrices = AddedPrices + float((data.text).replace('$', '').replace(',', ''))
                    NumberOfPrices = NumberOfPrices + 1
            counter = counter + 1

        #print("Average selling price for test " + str(TestLoop) + ": "  + str(AddedPrices/NumberOfPrices))

        print("CombinedAverages:" + str(CombinedAverages))
        print("AddedPrices: " + str(AddedPrices))
        print("NumberOfPrices:" + str(NumberOfPrices))
        CombinedAverages = CombinedAverages + AddedPrices/NumberOfPrices #for when using multiple search loops

    f.write(input + '\n')
    f.write(str(CombinedAverages/TestLoop) + '\n')
    print("Total Average for " + str(input) + ": " + str(CombinedAverages/TestLoop))

driver.quit()
