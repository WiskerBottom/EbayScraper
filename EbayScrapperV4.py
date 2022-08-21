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

path = "" #The path you're storing the program in
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

inputs = ['rtx 3070', 'rtx 3060', 'rtx 3050', 'rx 6500', 'rx 6600', 'rx 6700', 'rtx 2080', 'rtx 2070', 'gtx 1080', 'gtx 1070', 'gtx 980', 'gtx 970', 'gtx 780', 'gtx 770', 'gtx 680', 'gtx 670', 'gtx 580', 'gtx 480', 'gtx 470']
inputs.sort()


driver.get("https://www.ebay.com/")

#time.sleep(10)
#Advanced Settings button click
driver.find_element("xpath", '/html/body/header/table/tbody/tr/td[5]/form/table/tbody/tr/td[4]/a').click()
#Sold Listings Only button click
driver.find_element("xpath", "/html/body/div[3]/div[4]/div/div/div/div/form/fieldset[2]/label[3]/input").click()

#Do a initial search to apply filter
InitialSearch = driver.find_element("xpath", "/html/body/div[3]/div[4]/div/div/div/div/form/fieldset[1]/div[1]/input")
InitialSearch.clear()
InitialSearch.send_keys("Graphics Card")
InitialSearch.submit()

time.sleep(1)

#initialsearch = driver.find_elements("xpath", '/html/body/header/table/tbody/tr/td[5]/form/table/tbody/tr/td[1]/div[1]/div/input[1]')

#for item in initialsearch:
#    item.clear()
#    item.submit()

os.chdir(path + '/Details/')
if os.path.exists(str(date.today())) == True:
    os.remove(str(date.today()))
f = open(str(date.today()).replace('-',''), 'w')
f.write(str(len(inputs)*2) + "\n")
f.write("\n")
os.chdir(path)


FirstRun = True
for item in inputs:
    input = item
    CombinedAverages = 0
    TestLoop = 0

    while TestLoop < 3:
        TestLoop = TestLoop + 1

        if FirstRun == True:
            search = driver.find_element("xpath",'/html/body/div[5]/div[1]/div[1]/div[1]/header/table/tbody/tr/td[5]/form/table/tbody/tr/td[1]/div[1]/div/input[1]')

            search.clear()

            search.send_keys(input + " graphics card")

            search.submit()
            
            FirstRun = False
        else: 
            search = driver.find_element("xpath",'/html/body/div[3]/header/table/tbody/tr/td[5]/form/table/tbody/tr/td[1]/div[1]/div/input[1]')

            search.clear()

            search.send_keys(input + " graphics card")

            search.submit()

        prices = driver.find_elements("class name", "s-item__price")

        AddedPrices = 0
        NumberOfPrices = 0
        counter = 0
        #print("PRICES: " + str(prices[0]))
        #time.sleep(1)
        driver.get_screenshot_as_file(path)
        for data in prices:
            #print(data)
            if (counter % 2) != 0 and counter <= 15:
                print("Added price:" + str(data.text))
                #if data.text.find(" ") != -1 or data.text.find("") != -1:
                #    print("Canceled line: " + str(data.text))
                #    continue
                if data.text.find("to") != -1:
                    print("Canceled line: " + str(data.text))
                    continue
                elif float((data.text).replace('$', '').replace(',', '')) > 2000.00:
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
        CombinedAverages = CombinedAverages + AddedPrices/NumberOfPrices

    f.write(input + '\n')
    f.write(str(CombinedAverages/3) + '\n')
    #print("Total Average for " + str(input) + ": " + str(CombinedAverages/3))

driver.quit()
