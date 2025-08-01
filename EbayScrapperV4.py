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

debug=False

if (debug == False):
    path = "/app" #The path you're storing the program in
    user = "" #The name of the user you are running this with
else:
    path = "/home/roosevelt/Downloads/EbayScrapper"
    user = "roosevelt"

chrome_options = Options()
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--enable-crash-reporter")
chrome_options.add_argument('--window-size=1200,800');
if (debug == False):
    chrome_options.add_argument("--headless")
#chrome_options.add_argument('--ignore-certificate-errors')
#chrome_options.add_argument('--allow-running-insecure-content')

driver = webdriver.Chrome(options=chrome_options)

#Ebay's advanced settings don't show up if the window is too small.
#driver.set_window_size(1920, 380)

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
time.sleep(2)

print("browser setup successfully!")

#initialsearch = driver.find_elements("xpath", '/html/body/header/table/tbody/tr/td[5]/form/table/tbody/tr/td[1]/div[1]/div/input[1]')

#for item in initialsearch:
#    item.clear()
#    item.submit()

#f = open("/app/Details/cat.txt", "a")
#f.write("boo!\n")
#f.close()

if (debug == False):
    os.chdir(path + '/Details/')
    if os.path.exists(str(date.today())) == True:
        os.remove(str(date.today()))
    f = open(str(date.today()).replace('-',''), 'w')
    f.write(str(len(inputs)*2) + "\n")
    f.write("\n")
    os.chdir(path)


FirstRun = True
for item in inputs:
    prices = []
    time.sleep(1)
    print("item: " + item)
    input = item
    CombinedAverages = 0
    counter = 0

    while len(prices) == 0: #repeat attempt search until items are successfully grabbed
        if (counter >= 3):
            print("3 failed attempts, rebooting browser...")
            driver.quit()
            driver = webdriver.Chrome(options=chrome_options)
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
            time.sleep(2)
            counter = 0

        print("attempting to search for item...")
        search = driver.find_element("xpath",'//*[@id="gh-ac"]')
        time.sleep(0.125)
        search.clear()
        time.sleep(0.125)
        search.send_keys(input + " graphics card")
        time.sleep(0.125)
        search.submit()

        time.sleep(2)
        prices = driver.find_elements(By.XPATH, ".//span[@class='s-item__price']/span")
        #prices = driver.find_elements(By.CSS_SELECTOR, "span.s-item__price")
        #print(prices)
        counter = counter + 1

    if (1==1): #pov you didn't want to fix the indentation
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

        print("AddedPrices: " + str(AddedPrices))
        print("NumberOfPrices:" + str(NumberOfPrices))

    if (debug==False):
        f.write(input + '\n')
        f.write(str(AddedPrices/NumberOfPrices) + '\n')
    print("Total Average for " + str(input) + ": " + str(AddedPrices/NumberOfPrices))

driver.quit()
f.close()
