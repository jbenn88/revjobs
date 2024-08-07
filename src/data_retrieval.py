from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import lxml
from datetime import datetime
# import io
# import os
# import pathlib
from time import sleep
# from win10toast import ToastNotifier
from config.config import get_config

def check_for_jobs():
    config = get_config()
    url = 'https://www.rev.com/workspace/findwork'

    # Set up web driver #
    options = Options()
    options.headless = False
    s = Service("/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(service=s, options=options)
    driver.get(config['url'])

    # Log in #
    # username_xpath = '//*[@id="email-input"]'
    # next_button_xpath = '//*[@id="submit-button"]' # "submit-button"
    # password_xpath = '//*[@id="password-input"]' # "password-input"
    # sign_in_xpath = '//*[@id="submit-button"]' # "submit-button"

    driver.find_element(By.XPATH, config['username_xpath']).send_keys(config['username'])
    driver.find_element(By.XPATH, config['next_button_xpath']).click()
    WebDriverWait(driver, 1000000).until(EC.element_to_be_clickable((By.XPATH, config['password_xpath']))).send_keys(config['password'])
    driver.find_element(By.XPATH, config['sign_in_xpath']).click()
    # WebDriverWait line found at: https://stackoverflow.com/questions/56085152/selenium-python-error-element-could-not-be-scrolled-into-view
    # to solve issue of element not being scrolled into view

    sleep(5) # Will not find element without waiting
    # Click "No, thanks" on notification pop up
    # notifications_popup_xpath = '//*[@id="pushActionRefuse"]'
    driver.find_element(By.XPATH, config['notifications_popup_xpath']).click()
    # Retrieve job data #
    # number_of_jobs_xpath = '/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/span[1]/a[1]/span[2]'
    # new: /html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/span[1]/a[1]/span[2]
    # class: "num-active-rows"
    # number_of_line_jobs_xpath = '/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/span[1]/a[3]/span[2]'
    # new: /html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/span[1]/a[3]/span[2]
    # class: "num-active-rows"

    number_of_jobs = driver.find_element(By.XPATH, config['number_of_jobs_xpath']).text
    number_of_line_jobs = driver.find_element(By.XPATH, config['number_of_line_jobs_xpath']).text

    # Set filter to ignore Verbatim jobs
    more_button_xpath = '/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div/div[1]/div[5]/div/div/div/i'
    # new xpath: /html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div/div[1]/div[5]/div/div/div/i
    #more_button_class = 'pl2 fa pr2 fa-chevron-down'
    driver.find_element(By.XPATH, config['more_button_xpath']).click()
    verbatim_checkbox_xpath = '/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div/label/input'
    # new xpath: /html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div/label/input
    # verbatim clickbox info: input type="checkbox"
    driver.find_element(By.XPATH, config['verbatim_checkbox_xpath']).click()

    # Collects time length of all jobs available
    times = []

    all_time_divs = driver.find_elements(By.XPATH, config['time_divs_paths'])
    for div in all_time_divs:
        times.append(str(div.text))

    under_ten_count = 0
    under_five_count = 0
    for time in times:
        if (int(time[:2]) < 10):
            under_ten_count += 1
        if (int(time[:2]) < 5):
            under_five_count += 1

    # Retrieves number of audio and video jobs available
    media_types = []
    all_audio_divs = driver.find_elements(By.XPATH, config['audio_divs_paths'])
    all_video_divs = driver.find_elements(By.XPATH, config['video_divs_paths'])
    audio_jobs = len(all_audio_divs)
    video_jobs = len(all_video_divs)

    # Retrieves number of unclaims per job
    unclaim_divs = driver.find_elements(By.XPATH, config['unclaim_divs_paths'])
    unclaims = []
    zero_unclaim_count = 0
    one_unclaim_count = 0
    two_unclaim_count = 0
    for div in unclaim_divs:
        unclaims.append(int(div.text))
    for unclaim in unclaims:
        if (unclaim == 0):
            zero_unclaim_count += 1
        if (unclaim == 1):
            one_unclaim_count += 1
        if (unclaim == 2):
            two_unclaim_count += 1


    number_of_jobs_with_one_or_two_unclaims = one_unclaim_count + two_unclaim_count
    if (len(unclaims)) > 0:
        percentage_of_jobs_with_under_two_unclaims = (number_of_jobs_with_one_or_two_unclaims / len(unclaims))
    else:
        percentage_of_jobs_with_under_two_unclaims = 0.0
    driver.close()

    # Format data
    number_of_jobs = number_of_jobs.replace("(", "").replace(")", "")
    number_of_line_jobs = number_of_line_jobs.replace("(", "").replace(")", "")

    # Save information to file #
    time_and_date = datetime.now()
    string_time_and_date = time_and_date.strftime("%A %m/%d %I:%M %p")
    hour_of_time_now = time_and_date.strftime("%I")
    file_name = "../output/job_data.txt"

    with open(file_name, "a+") as source_file:
        source_file.write(string_time_and_date + " " + number_of_jobs + " " + number_of_line_jobs + "\n")

'''
### Send notifications to desktop (Windows 10)

# Sends first notification with number of total jobs and line jobs
# Customized to send if greater than X number of total jobs


toast = ToastNotifier()

if (int(number_of_jobs) > 10):
    toast.show_toast("Rev Jobs Available", "There are " + number_of_jobs + " total jobs, and " + number_of_line_jobs + " line jobs currently available.")
    toast.show_toast("Jobs with 0 unclaims: " + str(zero_unclaim_count) + "/" + str(len(unclaims)) + " | Jobs with 1-2 unclaims: " + str(number_of_jobs_with_one_or_two_unclaims) + "/" + str(len(unclaims)) +"(" + str(percentage_of_jobs_with_under_two_unclaims * 100) + "%)")


# Send second notification with number of jobs under 5 and 10 minutes
if (under_ten_count > 5 or under_five_count > 2):
    toast.show_toast("There are " + str(under_ten_count) + " jobs under 10 minutes and " + str(under_five_count) + " jobs under 5 minutes.")

# TODO: Add number of jobs:
#       - below X minutes in length
#       - number of video jobs
#       - number of audio jobs
#       - number and percentage of jobs with [0 - X] unclaims
# TODO: Write documentation and set up to be portable/usable by other rev members
# TODO: Add option to show short list of jobs with certain attributes
#           - (zero unclaims, under X minutes, video file etc)
#                   - ability to claim from that notification/list
'''