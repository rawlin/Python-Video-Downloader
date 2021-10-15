from selenium import webdriver
import time
import selenium
import selenium.common.exceptions
import json
import os
import shutil
import urllib.request
import urllib
import credentials
from progress import ProgressBar

# Coding with mitch url
starting_url = "https://codingwithmitch.com/login/?next=/courses/modularizing-android-apps/you-start/"
email = credentials.email
pwd = credentials.pwd
# Enter credentials into login
id_for_email = "id_email"
id_for_pwd = "password"
counter = 0
map = {}
file_name = "courses.json"
downloaded_courses_dir_name = "downloaded_course"


def main():

    # Check if json file with course download links exists
    if os.path.isfile(file_name):
        download_course()
        return

    # Using Chrome to access the website
    driver = webdriver.Chrome()
    driver.get(url=starting_url)

    # time.sleep(120) # Sleep for 20 seconds while I enter in credentials

    driver.find_element_by_id(id_for_email).send_keys(email)
    driver.find_element_by_id(id_for_pwd).send_keys(pwd)

    # Wait for captcha complete.....
    time.sleep(60)
    print("COUNTER IS UP......")

    # Pause player
    # driver.execute_script('document.getElementById("player").pause()')

    counter = 0
    add_values_to_map(driver, counter)
    print(map)

    # Dump json file to file system
    f = open(file_name, "w")
    f.write(json.dumps(map))
    download_course()


def add_values_to_map(driver, counter):
    counter += 1
    element = driver.find_elements_by_class_name(
        "btn.btn-primary.m-0")[0].get_attribute('href')
    map[counter] = element
    xp_path = "//*[contains(text(), 'Next Lecture')]"

    try:
        driver.find_element_by_xpath(xp_path).click()
        add_values_to_map(counter)
    except selenium.common.exceptions.NoSuchElementException as err:
        print(err)
        return
    except selenium.common.exceptions.ElementNotInteractableException as err:
        print(err)
        return


def download_course():
    ''' Download video files one by one'''
    courses = {}
    # Read json file
    with open(file_name) as json_file:
        # object_hook is used to make the key of type int
        courses = json.load(json_file,
                            object_hook=lambda d: {int(k)
                                                   if k.lstrip('-').isdigit() else k: v for k, v in d.items()
                                                   }
                            )

    # Check if download directory exists
    try:
        os.makedirs(downloaded_courses_dir_name)

    except OSError as err:
        print(err)
        print("DIRECTORY ALREADY EXISTS!!!! PLEASE DELETE DIRECTORY TO DOWNLOAD")
        user_input = input("Enter Y/y if you want to delete directory\n")

        if user_input.isalpha and user_input.lower() == 'y':
            # Delete exisitig directory
            shutil.rmtree(downloaded_courses_dir_name)
        else:
            print("Cannot proceed without deleting existing directory")
            return

    # Iterate and download
    counter_one = 1
    counter_two = 1
    for course in courses:

        if courses[course] == None:
            counter_one += 1
            counter_two = 1

        
        
        if courses[course] == None:
            continue

        # Generate video title
        video_title = str(counter_one) + "." + str(counter_two)+".mp4"
        print(video_title)
        
        # Download video

        counter_two += 1
        try:

            print("Downloading video %s ....." % courses[course])
            rq = urllib.request.urlretrieve(courses[course], filename=os.path.join(downloaded_courses_dir_name, video_title), reporthook=ProgressBar())
            print(rq)
          

        except Exception as err:

            print(err)
            return

if __name__ == "__main__":
    main()