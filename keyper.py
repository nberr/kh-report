###########################################################################################
# Description: take the generated reports from keyper and homenet                         #
#              and determine which keys are in keyper but not in homenet                  #
# Author: Nicholas Berriochoa                                                             #
# Start Date: 21 August 2020                                                              #
# Changes: added comments - 24 August 2020                                                #
#          added automation for logging in and generating reports - 24 August 2020        #
###########################################################################################
import getpass
import pandas as pd
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

homenet_user = input("Enter homenet user: ")
homenet_password = getpass.getpass("Enter homenet password: ")
keyper_password = getpass.getpass("Enter keyper password (4 digits): ")

driver = webdriver.Chrome('/mnt/c/Drivers/chromedriver.exe')

# open keyper UI
driver.get('http://10.10.218.170')

# login
pw_box = driver.find_element_by_name('txtPassword')
pw_box.send_keys(keyper_password)
submit_box = driver.find_element_by_name('btnLogin')
submit_box.click()

# navigate to report generator
driver.get('http://10.10.218.170/Reports/Reports_AdHocHome.aspx')

# download the report
excel_button = driver.find_element_by_name('ctl00$contentMain$dgShared$ctl08$imgbtnExporttoExcel0')
excel_button.click()

# navigate to homenet
driver.get('https://homenetauto.signin.coxautoinc.com/?solutionID=HME_prod&clientId=efb6cb5b4f2a401a8225c9f2e8c6313c')

# login
homenet_username = driver.find_element_by_name('username')
homenet_username.send_keys(homenet_user)

homenet_next = driver.find_element_by_id('signIn')
homenet_next.click()

wait = WebDriverWait(driver, 10)
homenet_pw = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
homenet_pw.send_keys(homenet_password)

homenet_signIn = driver.find_element_by_id('signIn')
homenet_signIn.click()

# navigate to inventory
wait_longer = WebDriverWait(driver,100)
rooftop = wait_longer.until(EC.element_to_be_clickable((By.ID, 'ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_WidgetsColumn1_ctl03_InventoryStatsGrid_row1_VirtualRooftopName_VirtualRooftopFilterButton')))

driver.get('https://www.homenetiol.com/inventory/browse-vehicles/list?filter={VirtualRooftopID:.-2235151}')

homenet_export = driver.find_element_by_id('ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_ctl00_HeaderButtons_ExportToExcelActionButton')
homenet_export.click()

# wait to finish the download
time.sleep(5)

# close the web browser
driver.quit()

# pull the necessary data from the files

# homenet file
date = datetime.now().strftime('%-m-%d-%Y')
homenet_file = 'InventoryReport-' + date + '.xls'
homenet_list = pd.read_html('../Downloads/' + homenet_file)[0]['Stock'].tolist()
# print(homenet_list)
os.remove('../Downloads/' + homenet_file)

# keyper file
keyper_list = pd.read_csv('../Downloads/temp.csv').name.tolist()
# print(keyper_list)
os.remove('../Downloads/temp.csv')


# for each value in the keyper list, check if it is in homenet.
# if it is in homenet, remove the value from both lists
for i in keyper_list[:]:
  if i in homenet_list[:]:
     keyper_list.remove(i)
     homenet_list.remove(i)

# sort the list in alphabetical order and print each value
keyper_list.sort()

# write the list to a file
output = open('../Desktop/output.txt', 'w+')
output.write('\n'.join(keyper_list))
output.close()
