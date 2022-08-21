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

chrome_options = Options()
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--enable-crash-reporter")
chrome_options.add_argument("--headless")
#chrome_options.add_argument('--ignore-certificate-errors')
#chrome_options.add_argument('--allow-running-insecure-content')
driver = webdriver.Chrome(options=chrome_options)

#driver.get("chrome://net-internals/#hsts")

#time.sleep(1)

#driver.get_screenshot_as_file("screenshot.png")

#RemoveSecurity = driver.find_elements("xpath", '//*[@id="domain-security-policy-view-delete-input"]')

#RemoveSecurity[0].send_keys("www.ebay.com")
#RemoveSecurity[0].submit()

#exit()

inputs = ['rtx 3070', 'rtx 3060', 'rtx 3050', 'rx 6500', 'rx 6600', 'rx 6700']

driver.get("https://www.ebay.com/")

initialsearch = driver.find_elements("xpath", '/html/body/header/table/tbody/tr/td[5]/form/table/tbody/tr/td[1]/div[1]/div/input[1]')

for item in initialsearch:
    item.submit()

os.chdir('/home/charlotte/Documents/Programs/Python/EbayScrapper/Details/')
if os.path.exists(str(date.today())) == True:
    os.remove(str(date.today()))
f = open(str(date.today()).replace('-',''), 'a')

for item in inputs:
    input = item
    CombinedAverages = 0
    TestLoop = 0

    while TestLoop < 3:
        TestLoop = TestLoop + 1
        search = driver.find_elements("xpath",'/html/body/div[3]/header/table/tbody/tr/td[5]/form/table/tbody/tr/td[1]/div[1]/div/input[1]')

        for item in search:

            item.clear()

            item.send_keys(input + " graphics card")

            item.submit()

        prices = driver.find_elements("class name", "s-item__price")

        AddedPrices = 0
        NumberOfPrices = 0
        counter = 0
        #print("PRICES: " + str(prices[0]))
        #time.sleep(1)
        #driver.get_screenshot_as_file("screenshot.png")
        for data in prices:
            print(data)
            if (counter % 2) != 0 and counter <= 15:
                print("Added price:" + str(data.text))
                #if data.text.find(" ") != -1 or data.text.find("") != -1:
                #    print("Canceled line: " + str(data.text))
                #    continue
                if float((data.text).replace('$', '').replace(',', '')) > 2000.00:
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
