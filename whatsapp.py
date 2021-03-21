# Note: For proper working of this Script Good and Uninterepted Internet Connection is Required
# Keep all contacts unique
# Can save contact with their phone Number

# Import required packages
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import time
import os
import openpyxl as excel

# function to read contacts from a text file
def readContacts(fileName):
    lst = []
    file = excel.load_workbook(fileName)
    sheet = file.active
    firstCol = sheet['A']
    for cell in range(len(firstCol)):
        contact = str(firstCol[cell].value)
        contact = "\"" + contact + "\""
        lst.append(contact)
    return lst

# Target Contacts, keep them in double colons
# Not tested on Broadcast
targets = readContacts("contacts.xlsx")

# can comment out below line
print(targets)

# Driver to open a browser
print(os.path.abspath("chromedriver.exe"))
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"))

#link to open a site
driver.get("https://web.whatsapp.com/")

# 10 sec wait time to load, if good internet connection is not good then increase the time
# units in seconds
# note this time is being used below also
wait = WebDriverWait(driver, 10)
wait5 = WebDriverWait(driver, 5)
input("Scan the QR code and then press Enter")

# Message to send list
# 1st Parameter: Hours in 0-23
# 2nd Parameter: Minutes
# 3rd Parameter: Seconds (Keep it Zero)
# 4th Parameter: Message to send at a particular time
# Put '\n' at the end of the message, it is identified as Enter Key
# Else uncomment Keys.Enter in the last step if you dont want to use '\n'
# Keep a nice gap between successive messages
# Use Keys.SHIFT + Keys.ENTER to give a new line effect in your Message
msgToSend = [
                [19, 21, 0, "This is a WhatsApp automated message. Testing is being done to implement this for workshop publi. Please ignore." + Keys.SHIFT + Keys.ENTER]
            ]

# Count variable to identify the number of messages to be sent
count = 0
while count<len(msgToSend):

    # Identify time
    curTime = datetime.datetime.now()
    curHour = curTime.time().hour
    curMin = curTime.time().minute
    curSec = curTime.time().second

    # if time matches then move further
    if True:
        # utility variables to tract count of success and fails
        success = 0
        sNo = 1
        failList = []

        # Iterate over selected contacts
        for target in targets:
            print(sNo, ". Target is: " + target[1:-1])
            sNo+=1
            try:
                # Select the target
                x_arg = '//span[contains(@title,' + target + ')]'
                try:
                    wait.until(EC.presence_of_element_located((
                        By.XPATH, x_arg
                    )))
                    print('Target searched')
                except:
                    # If contact not found, then search for it
                    print('In except block searching for contact')
                    searBoxPath = "//div[@contenteditable='true']"
                    inputSearchBox = wait5.until(EC.presence_of_element_located((
                        By.XPATH, searBoxPath
                    )))
                    # inputSearchBox = driver.find_element_by_id("input-chatlist-search")
                    # time.sleep(0.5)
                    # click the search button
                    #
                    # driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div/button').click()
                    time.sleep(1)
                    # inputSearchBox.clear()
                    inputSearchBox.send_keys(target[1:len(target) - 1])
                    print('Target Searched')
                    # Increase the time if searching a contact is taking a long time
                    time.sleep(4)

                # Select the target
                driver.find_element_by_xpath(x_arg).click()
                print("Target Successfully Selected")
                time.sleep(2)

                # Select the Input Box
                # inp_xpath = "//div[@contenteditable='true']"
                inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
                input_box = wait.until(EC.presence_of_element_located((
                    By.XPATH, inp_xpath)))
                time.sleep(1)
                print('Input box located')

                # Send message
                # target is your target Name and msgToSend is you message
                input_box.send_keys("Hello, " + target[1:-1] + "."+ Keys.SHIFT + Keys.ENTER)
                input_box.send_keys(msgToSend[count][3]) # + Keys.ENTER (Uncomment it if your msg doesnt contain '\n')
                # Link Preview Time, Reduce this time, if internet connection is Good
                time.sleep(5)
                input_box.send_keys(Keys.ENTER)
                print("Successfully Send Message to : "+ target + '\n')
                success+=1
                time.sleep(0.5)

                # # click back button to clear search area
                # driver.find_elements_by_xpath('//*[@id="side"]/div[1]/div/button').click()
                # time.sleep(2)
                # print('Back button clicked')

            except:
                # If target Not found Add it to the failed List
                print("Cannot find Target: " + target)
                failList.append(target)
                pass

        print("\nSuccessfully Sent to: ", success)
        print("Failed to Sent to: ", len(failList))
        print(failList)
        print('\n\n')
        count+=1
driver.quit()