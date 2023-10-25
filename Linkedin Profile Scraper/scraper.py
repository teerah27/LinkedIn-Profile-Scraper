import csv
import time
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome()
sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)

# Task 1.1: Import username and password
username = "LINKEDIN_EMAIL"
password = "LINKEDIN_PASSWORD"

# Task 1.2: Key in login credentials
email_field = driver.find_element(By.ID, 'username')
email_field.send_keys(username)

password_field = driver.find_element(By.NAME, 'session_password')
password_field.send_keys(password)

# Task 1.3: Click the Login button
signin_field = driver.find_element(By.XPATH, '//*[@type="submit"]')
signin_field.click()

data = []

with open('mydata.csv', 'r') as csvfile: # read csv file containing url of the LinkedIn profile
    csvreader = csv.reader(csvfile)
    for url in csvreader:
        # Task 1: Login to Linkedin
        sleep(2)
        profile_url = url[0]
        driver.get(profile_url)
        start = time.time()
        initialScroll = 0
        finalScroll = 1000

        while True:
            driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
            # this command scrolls the window starting from the pixel value stored in the initialScroll
            # variable to the pixel value stored at the finalScroll variable
            initialScroll = finalScroll
            finalScroll += 1000

            # we will stop the script for 3 seconds so that the data can load
            time.sleep(2)
            end = time.time()
            # We will scroll for 10 seconds.
            if round(end - start) > 10:
                break

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 1 NAME
        intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
        name_loc = intro.find("h1")
        name = name_loc.get_text().strip()

        # 2 Title
        title = soup.find('div', {"class": "text-body-medium break-words"}).get_text().replace('\n', '').strip()

        # 3 LOCATION
        loc = soup.find('span', {'class': 'text-body-small inline t-black--light break-words'})
        location = loc.get_text().strip()

        # 4 EXPERIENCE
        experiences = []

        try:
            experience_div = soup.find('div', {"id": "experience"})
            exp_list = experience_div.findNext('div').findNext('div', {"class": "pvs-list__outer-container"}).findChild(
                'ul').findAll('li',
                                {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})

            for each_exp in exp_list:
                exp_temp = {
                    each_exp.findNext('span', {"class": "t-14 t-normal t-black--light"}).findNext(
                        'span').get_text().replace('\n', '').strip()  # timeframe
                }
                experiences.append(exp_temp)

        except AttributeError:
            pass

        # 5 EDUCATION LEVEL AND HISTORY
        educations = []
        try:
            education_div = soup.find('div', {"id": "education"})
            edu_list = education_div.findNext('div').findNext('div', {"class": "pvs-list__outer-container"}).findChild(
                'ul').findAll('li',
                                {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})

            for each_edu in edu_list:
                col_edu = each_edu.findNext("a",
                                            {
                                                "class": "optional-action-target-wrapper display-flex flex-column full-width"})
                edu_temp = {
                    col_edu.findNext('span', {"class": "t-14 t-normal"}).findNext(
                        'span').get_text().strip(),  # coursename
                }
                educations.append(edu_temp)

        except AttributeError:
            pass

        # 6 lICENSE AND CERTIFICATIONS
        certifications = []
        try:
            cert_div = soup.find('div', {"id": "licenses_and_certifications"})
            cert_list = cert_div.findNext('div').findNext('div', {"class": "pvs-list__outer-container"}).findChild(
                'ul').findAll('li',
                                {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})

            for cert in cert_list:
                col_cert = cert.findNext("div", {"class": "display-flex flex-column full-width align-self-center"})
                cert_temp = {
                    col_cert.findNext('div').findNext('span').findNext('span').text.replace('\n', '').strip()
                    # cert name
                }
                certifications.append(cert_temp)

        except AttributeError:
            pass

        # 7 SKILLS
        skills = []
        try:
            skills_div = soup.find('div', {"id": "skills"})
            skills_list = skills_div.findNext('div').findNext('div',
                                                                {"class": "pvs-list__outer-container"}).findChild(
                'ul').findAll('li',
                                {
                                    "class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})

            # Added code to expand the 'Show more' button for skills
            try:
                show_more_skills = driver.find_element_by_css_selector(
                    '#ember679 > div > div > div > div > section > button'
                )
                if show_more_skills.is_displayed():
                    show_more_skills.click()
                    time.sleep(2)
                    src = driver.page_source
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
            except Exception as e:
                pass
            # End of added code

            for skill in skills_list:
                col_skill = skill.findNext("a", {"data-field": "skill_card_skill_topic"})
                skill_temp = {
                    col_skill.findNext('div').findNext('span').findNext('span').text.replace('\n', '').strip()
                    # skills name
                }
                skills.append(skill_temp)

        except AttributeError:
            pass

        # 8 LANGUAGES
        languages = []

        try:
            Lang_div = soup.find('div', {"id": "languages"})
            lang_list = Lang_div.findNext('div').findNext('div', {"class": "pvs-list__outer-container"}).findChild(
                'ul').findAll('li',
                                {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})

            for lang in lang_list:
                lang_temp = {
                    lang.findNext("div", {"class": "display-flex align-items-center mr1 t-bold"}).findNext(
                        'span').get_text().strip()
                }
                languages.append(lang_temp)

        except AttributeError:
            pass


        data.append({
            "Name": name,
            "Title": title,
            "Location": location,
            "Experiences": experiences,
            "Education": educations,
            "Certifications": certifications,
            "Skills": skills,
            "Languages": languages

        })

driver.quit()
print(data)

