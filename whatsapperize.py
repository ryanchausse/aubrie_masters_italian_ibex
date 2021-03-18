import pandas as pd, os, time, base64, pysftp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from dotenv import load_dotenv

print("This script will open an excel spreadsheet in the local Downloads folder, pull out the experiment data, \
       and create an image of the conversation in WhatsApp \
       based on an interaction via https://www.fakewhats.com/generator with Selenium. The image will then \
       be uploaded to https://ryanchausse.com/aubrie_masters/images/conversation_pics/<x.png>, where x is \
       a unique composite key, probably '<item number>_<list number>', or somesuch.")

# Assigning env variables for SFTP url, username, and password based on ENV variables
load_dotenv(dotenv_path='.env')
sftp_domain = os.environ.get('SFTP_DOMAIN')
sftp_dir = str(os.environ.get('SFTP_DIR'))
local_dir = str(os.environ.get('LOCAL_DIR'))
ssh_login_name = os.environ.get('SSH_LOGIN_NAME')
password = os.environ.get('PASSWORD')

# Read experimental data, print to terminal
df = pd.read_excel('~/Downloads/experiment_data_revised.xlsx', sheet_name='Sheet1', header=0, usecols="A:K", nrows=64)
print(df)

# Create sftp connection with host.

# 1. Create unique filename in the format '<item number>_<list number>'
# 2. Gather image using https://www.fakewhats.com/generator from Intro, Response 1, and Response2 columns
# 3. Upload image to sftp://ryanchausse.com/aubrie_masters/images/

for index, row in df.iterrows():
    # Selenium to scrape the page, enter input data
    driver = webdriver.Firefox()
    driver.get('https://www.fakewhats.com/generator')
    time.sleep(1)
    wait_for_loading_div_gone = WebDriverWait(driver, timeout=10).until(
        ec.invisibility_of_element_located(
            (By.XPATH, '//a[contains(@class,"loader")]')
        )
    )
    print('Past loader visibility check for ' + str(row['Intro']))

    # Enter message text
    message_propername_element = driver.find_element_by_id("name")
    # message_propername_element.send_keys(str(row['Proper.Name1']))
    driver.execute_script("document.getElementById('name').value='" + str(row['Proper.Name1']) + "'")
    message_propername_element.send_keys(Keys.RETURN)
    time.sleep(1)
    message_link_element = driver.find_element_by_xpath('//a[contains(@href,"#panel4")]')
    message_link_element.click()
    time.sleep(1)

    message_textarea_element = driver.find_element_by_id("message-text")
    message_textarea_element.send_keys(str(row['Intro']))
    message_add_to_conversation_element = driver.find_element_by_css_selector(".sendMessage")
    message_add_to_conversation_element.click()
    time.sleep(1)
    if row['Response1']:
        message_textarea_element.clear()
        switch_speaker_button_element = driver.find_element_by_css_selector("label[for='green-message']")
        switch_speaker_button_element.click()
        time.sleep(1)
        message_textarea_element.send_keys(str(row['Response1']))
        if row['Response2'] is not None and str(row['Response2']) != 'nan':
            time.sleep(1)
            message_textarea_element.send_keys(' ' + str(row['Response2']))
            time.sleep(1)
        message_add_to_conversation_element.click()
        time.sleep(1)

    download_button_element = driver.find_element_by_css_selector("a.line-button-white")
    download_button_element.click()
    time.sleep(4)

    # get the image source
    imgfilename = str(row['Item.n']) + "_" + str(row['list']) + '.png'
    print('imgfilename ' + imgfilename)
    imgsrc = driver.find_element_by_css_selector('img').get_attribute('src')
    imgdata = imgsrc.replace('data:image/png;base64,', '')

    # download
    with open(local_dir + '/' + imgfilename, 'wb') as fh:
        fh.write(base64.b64decode(imgdata))

    time.sleep(1)
    driver.close()
    driver.quit()
    time.sleep(1)
    # upload to remote server
    cnopts = pysftp.CnOpts(knownhosts='./known_hosts')
    with pysftp.Connection(sftp_domain, username=ssh_login_name, password=password, cnopts=cnopts) as sftp:
        sftp.put_r(local_dir, sftp_dir)

print("Done.")
