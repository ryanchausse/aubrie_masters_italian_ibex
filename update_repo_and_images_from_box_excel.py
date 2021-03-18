import pandas as pd, os, time, base64, pysftp, glob, datetime, pathlib
from dateutil import tz
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from dotenv import load_dotenv
from boxsdk import JWTAuth, Client
from git import Repo

print("This script replaces the old Excel formula/column from the original experiment data spreadsheet. \
      The aim is to scrape the relevant fields \
      from the original spreadsheet, process them into a JSON field that needs be appended to \
      example_data.js (or perhaps another, better named file), and to upload these data \
      to IBEX farm which shows the project at https://spellout.net/ibexexps/aubrieamstutz/SPD/experiment.html. \
      It may be possible to update via the web UI via Selenium.")

# Assigning env variables for SFTP url, username, and password based on ENV variables
load_dotenv(dotenv_path='.env')

# Load all .env variables
box_jwt_config_location = str(os.environ.get('BOX_JWT_CONFIG_LOCATION'))
box_file_shared_link = str(os.environ.get('BOX_FILE_SHARED_LINK'))
box_local_dir = str(os.environ.get('BOX_LOCAL_DIR'))
box_user_id = str(os.environ.get('BOX_USER_ID'))
box_filename_without_version_or_extension = str(os.environ.get('BOX_FILENAME_WITHOUT_VERSION_OR_EXTENSION'))
experiment_data_file_name = str(os.environ.get('EXPERIMENT_DATA_FILE_NAME'))
expected_excel_local_path = box_local_dir + "/" + box_filename_without_version_or_extension + '*.xlsx'
expected_json_data_path = box_local_dir + "/" + experiment_data_file_name
ibex_farm_username = str(os.environ.get('IBEX_FARM_USERNAME'))
ibex_farm_password = str(os.environ.get('IBEX_FARM_PASSWORD'))
ibex_farm_project_name = str(os.environ.get('IBEX_FARM_PROJECT_NAME'))
sftp_domain = os.environ.get('SFTP_DOMAIN')
sftp_dir = str(os.environ.get('SFTP_DIR'))
local_dir = str(os.environ.get('LOCAL_DIR'))
ssh_login_name = os.environ.get('SSH_LOGIN_NAME')
ssh_password = os.environ.get('SSH_PASSWORD')
git_remote_repo_location = str(os.environ.get('GIT_REMOTE_REPO_LOCATION'))
git_local_repo_location = str(os.environ.get('GIT_LOCAL_REPO_LOCATION'))
git_branch = str(os.environ.get('GIT_BRANCH'))
local_repo_experiment_data_file_location = str(os.environ.get('LOCAL_REPO_EXPERIMENT_DATA_FILE_LOCATION'))
excel_column_range = str(os.environ.get('EXCEL_COLUMN_RANGE'))
excel_number_of_rows = int(os.environ.get('EXCEL_NUMBER_OF_ROWS'))
excel_sheet_name = str(os.environ.get('EXCEL_SHEET_NAME'))

# Get excel file from Box, download to ~/Downloads
excel_local_path = './'
for file in glob.glob(expected_excel_local_path):
    excel_local_path = file
# Optional
box_shared_link_password = str(os.environ.get('BOX_SHARED_LINK_PASSWORD'))

config_initial = JWTAuth.from_settings_file(box_jwt_config_location)
client_initial = Client(config_initial)

auth_user = config_initial.authenticate_user(box_user_id)
box_user = client_initial.user(user_id=box_user_id).get()
config = JWTAuth.from_settings_file(box_jwt_config_location, access_token=auth_user)
client = Client(config)
print('Impersonating as user: ' + client.user().get().name)

file = client.get_shared_item(box_file_shared_link)
box_file_id = file.id

# Buffer local Downloads/filename to determine if date/time modified has changed.
# If so, exit 0
local_file_create_time = time.ctime(os.path.getctime(excel_local_path))
local_file_modified_time = time.ctime(os.path.getmtime(excel_local_path))
dt_box_modified = datetime.datetime.fromisoformat(file.content_modified_at).astimezone(tz.tzlocal())
dt_local_modified = datetime.datetime.strptime(local_file_modified_time, "%a %b %d %H:%M:%S %Y").astimezone(tz.tzlocal())
modified_recently = dt_box_modified > dt_local_modified

# Write file content to file, else exit(0)
if not modified_recently:
    print('No change to file. Exiting...')
    #exit(0)

with open(excel_local_path, 'wb') as open_file:
    client.with_shared_link(box_file_shared_link, box_shared_link_password).file(box_file_id).download_to(open_file)
    open_file.close()

# Read experimental data, print to terminal
df = pd.read_excel(excel_local_path, sheet_name=excel_sheet_name, header=0, usecols=excel_column_range, nrows=excel_number_of_rows)
print(df)

# Original, working excel formula for json column:
# =CHAR(91)&CHAR(91)&""""&A2&""""&", "&B2&CHAR(93)&", ""AcceptabilityJudgment"", {s: {html: ""<div style=\""width: 50em;\""><!––  trial_type="&A2&"  item_number="&B2&"  pron="&E2&"  cond="&F2&"  cond_code="&D2&"  attested="&K2&"  ––><p style=\""text-align: center;\"" hidden>"&SUBSTITUTE(H2,CHAR(10),"<br \> ")&"</p><center><img style=\""text-align:center;\"" src=\""https://ryanchausse.com/aubrie_masters/images/conversation_pics/"&B2&"_"&C2&".png\"" alt=\""" & SUBSTITUTE(H2,CHAR(10),"<br \> ") & " " & I2 & " " & J2 & "\"" /></center></div>""}}],"

# Parse df, format as json value that needs to go into example_data.js
# e.g. [["test", 6], "AcceptabilityJudgment", {s: {html: "<div style=\"width: 50em;\"><!––  trial_type=test  item_number=6  pron=We  cond=b  cond_code=Rt.Null  attested=Y  ––><p style=\"text-align: center;\" hidden>How was the rest of your Saturday?</p><center><img style=\"text-align:center;\" src=\"https://ryanchausse.com/aubrie_masters/images/conversation_pics/6_7.png\" alt=\"How was the rest of your Saturday? Had a nice dinner and then we went to see some live music after we saw the movie with you. \" /></center></div>"}}],
# which translates to:
# [["<<trial.type>>", <<Item.n>>], "AcceptabilityJudgment", {s: {html: "<div style=\"width: 50em;\"><!––  trial_type=<<trial.type>>  item_number=<<Item.n>>  pron=<<Pron>>  cond=<<cond>>  cond_code=<<cond.code>>  attested=<<attested (Y/N)>>  ––><p style=\"text-align: center;\" hidden><<Intro>></p><center><img style=\"text-align:center;\" src=\"https://ryanchausse.com/aubrie_masters/images/conversation_pics/<<Item.n>>_<<list>>.png\" alt=\"<<Intro>> <<Response1>> <<Response2>>\" /></center></div>"}}],

json_to_append = ''
for index, row in df.iterrows():
    if str(row['trial.type']) == "filler" or str(row['trial.type']) == "practice":
        row_to_json_string = "[\"" + str(row['trial.type']) + "\" " \
                             ", \"AcceptabilityJudgment\", {s: {html: \"<div style=\\\"width: 50em;\\\"><!––  trial_type=" + \
                             str(row['trial.type']) + " item_number=" + str(row['Item.n']) + " attested=" + \
                             str(row['attested (Y/N)']) + " ––><p style=\\\"text-align: center;\\\" hidden>" + \
                             str(row['Intro']) + "</p><center><img style=\\\"text-align:center;\\\" src=\\\"https://ryanchausse.com/aubrie_masters/images/conversation_pics/" + \
                             str(row['Item.n']) + "_" + str(row['list']) + ".png\\\" alt=\\\"" + \
                             (str(row['Intro']) if row['Intro'] and str(row['Intro']) != 'nan' else '') + " " + \
                             (str(row['Response1']) if row['Response1'] and str(row['Response1']) != 'nan' else '') + " " + \
                             (str(row['Response2']) if row['Response2'] and str(row['Response2']) != 'nan' else '') + \
                             "\\\"/></center></div>\"}}],"
    else:
        row_to_json_string = "[[\"" + str(row['trial.type']) + "\", " + str(int(row['Item.n'])) + \
                             "], \"AcceptabilityJudgment\", {s: {html: \"<div style=\\\"width: 50em;\\\"><!––  trial_type=" + \
                             str(row['trial.type']) + " item_number=" + str(int(row['Item.n'])) + " list_number=" + str(int(row['list'])) + " pron=" + str(row['Pron']) + \
                             " cond=" + str(row['cond']) + " cond_code=" + str(row['cond.code']) + " attested=" + \
                             str(row['attested (Y/N)']) + " ––><p style=\\\"text-align: center;\\\" hidden>" + \
                             str(row['Intro']) + "</p><center><img style=\\\"text-align:center;\\\" src=\\\"https://ryanchausse.com/aubrie_masters/images/conversation_pics/" + \
                             str(int(row['Item.n'])) + "_" + str(int(row['list'])) + ".png\\\" alt=\\\"" + \
                             (str(row['Intro']) if row['Intro'] and str(row['Intro']) != 'nan' else '') + " " + \
                             (str(row['Response1']) if row['Response1'] and str(row['Response1']) != 'nan' else '') + " " + \
                             (str(row['Response2']) if row['Response2'] and str(row['Response2']) != 'nan' else '') + \
                             "\\\"/></center></div>\"}}],"
    json_to_append += row_to_json_string + "\n"
    print('')
print(json_to_append)

# Now replace all experiment JSON data with our new json_to_append
# then append "];" so it is properly formatted JSON at end of file, and write to file.

txt = pathlib.Path(local_repo_experiment_data_file_location).read_text()
old_file_data = txt.split('// Begin experiment data:')[0]
json_to_append = "// Begin experiment data: \n" + json_to_append + "];"
new_file_data = old_file_data + json_to_append

with open(local_repo_experiment_data_file_location, 'w') as json_data_file:
    json_data_file.write(new_file_data)

time.sleep(2)

# Update our github repo to include the new JSON data
try:
    with open(local_repo_experiment_data_file_location, 'w') as repo_json_data_file:
        repo_json_data_file.write(new_file_data)
except Exception as e:
    print(type(e))
    print(str(e))
print(os.getcwd())
repo = Repo(git_local_repo_location)
repo.git.add(update=True)
repo.index.commit('Changed: experiment data')
origin = repo.remote(name='origin')
origin.push()


# Now, log into IBEX farm with Selenium and replace all files with our repo update
print('Replacing JSON data file in IBEX farm...')

# Log in to IBEX Farm using Selenium and click to sync repo with IBEX platform
driver = webdriver.Firefox()
driver.get('https://spellout.net/ibexfarm/login')
time.sleep(1)
username_element = driver.find_element_by_name("username")
username_element.send_keys(ibex_farm_username)
time.sleep(1)
password_element = driver.find_element_by_name("password")
password_element.send_keys(ibex_farm_password)
time.sleep(1)
log_in_button = driver.find_element_by_name("submit")
log_in_button.click()
time.sleep(2)
experiment_link = driver.find_element_by_link_text(ibex_farm_project_name)
experiment_link.click()
time.sleep(2)
update_from_git_element = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/span[1]')
update_from_git_element.click()
time.sleep(1)
driver.execute_script("document.getElementById('git_url').value='" + git_remote_repo_location + "'")
driver.execute_script("document.getElementById('git_branch').value='" + git_branch + "'")
git_sync_element = driver.find_element_by_id('gitsync')
git_sync_element.click()
time.sleep(5)
driver.close()
driver.quit()

print('Done with sync, moving on to image gathering and upload to ryanchausse.com')
#
# # Read experimental data, print to terminal
# df = pd.read_excel(excel_local_path, sheet_name=excel_sheet_name, header=0,
#                    usecols=excel_column_range, nrows=excel_number_of_rows)
# # Automate this eventually using pandas functions, e.g.:
# # count_row = df.shape[0]  # Gives number of rows
# # count_col = df.shape[1]  # Gives number of columns
# print(df)
#
# # 1. Create unique filename in the format '<item number>_<list number>'
# # 2. Gather image using https://www.fakewhats.com/generator from Intro, Response 1, and Response2 columns
# # 3. Upload image to sftp://ryanchausse.com/aubrie_masters/images/
#
# for index, row in df.iterrows():
#     # Selenium to scrape the page, enter input data
#     driver = webdriver.Firefox()
#     driver.get('https://www.fakewhats.com/generator')
#     time.sleep(1)
#     wait_for_loading_div_gone = WebDriverWait(driver, timeout=10).until(
#         ec.invisibility_of_element_located(
#             (By.XPATH, '//a[contains(@class,"loader")]')
#         )
#     )
#     print('Past loader visibility check for ' + str(row['Intro']))
#
#     # Enter message text
#     message_propername_element = driver.find_element_by_id("name")
#     # message_propername_element.send_keys(str(row['Proper.Name1']))
#     driver.execute_script("document.getElementById('name').value='" + str(row['Proper.Name1']) + "'")
#     message_propername_element.send_keys(Keys.RETURN)
#     time.sleep(1)
#     message_link_element = driver.find_element_by_xpath('//a[contains(@href,"#panel4")]')
#     message_link_element.click()
#     time.sleep(1)
#
#     message_textarea_element = driver.find_element_by_id("message-text")
#     message_textarea_element.send_keys(str(row['Intro']))
#     message_add_to_conversation_element = driver.find_element_by_css_selector(".sendMessage")
#     message_add_to_conversation_element.click()
#     time.sleep(1)
#     if row['Response1'] and str(row['Response1']) != 'nan':
#         message_textarea_element.clear()
#         switch_speaker_button_element = driver.find_element_by_css_selector("label[for='green-message']")
#         switch_speaker_button_element.click()
#         time.sleep(1)
#         message_textarea_element.send_keys(str(row['Response1']))
#         if row['Response2'] and str(row['Response2']) != 'nan':
#             time.sleep(1)
#             message_textarea_element.send_keys(' ' + str(row['Response2']))
#             time.sleep(1)
#         message_add_to_conversation_element.click()
#         time.sleep(1)
#
#     download_button_element = driver.find_element_by_css_selector("a.line-button-white")
#     download_button_element.click()
#     time.sleep(4)
#
#     # get the image source
#     # Handle filler images (int type for list number will error)
#     imgfilename = str(int(row['Item.n'])) + "_" + str(int(row['list'])) + '.png'
#     print('imgfilename ' + imgfilename)
#     imgsrc = driver.find_element_by_css_selector('img').get_attribute('src')
#     imgdata = imgsrc.replace('data:image/png;base64,', '')
#
#     # download
#     with open(local_dir + '/' + imgfilename, 'wb') as fh:
#         fh.write(base64.b64decode(imgdata))
#
#     time.sleep(1)
#     driver.close()
#     driver.quit()
#     time.sleep(1)
#     # upload to remote server
#     cnopts = pysftp.CnOpts(knownhosts='./known_hosts')
#     with pysftp.Connection(sftp_domain, username=ssh_login_name, password=ssh_password, cnopts=cnopts) as sftp:
#         sftp.put_r(local_dir, sftp_dir)

print("Done.")
