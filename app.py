#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 10:30:31 2023

@author: kiranchandra
"""


import time
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st


from dotenv import load_dotenv





def is_element_present(driver, how, what):
    """Returns True if element is present"""
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def GetElement(driver, elementTag, locator="ID"):
    """Wait max 15 secs for element and then select when it is available"""
    try:
        def _get_element(_tag, _locator):
            _by = getObj(_locator)
            if is_element_present(driver, _by, _tag):
                return WebDriverWait(driver, 15).until(
                    lambda d: driver.find_element(_by, _tag))

        element = _get_element(elementTag, locator.upper())
        if element:
            return element
        else:
            print("Element not found with %s : %s" % (locator, elementTag))
            return None
    except Exception as e:
        print(e)
    return None


def getObj(locatorType):
    """This map defines how elements are identified"""
    map = {
        "ID" : By.ID,
        "NAME" : By.NAME,
        "XPATH" : By.XPATH,
        "TAG" : By.TAG_NAME,
        "CLASS" : By.CLASS_NAME,
        "CSS" : By.CSS_SELECTOR,
        "LINKTEXT" : By.LINK_TEXT
    }
    return map[locatorType]

def WaitTillElementPresent(driver, elementTag, locator="ID", timeout=30):
    """Wait till element present. Default 30 seconds"""
    result = False
    driver.implicitly_wait(0)
    locator = locator.upper()

    for i in range(timeout):
        time.sleep(0.99)
        try:
            if is_element_present(driver, getObj(locator), elementTag):
                result = True
                break
        except Exception as e:
            print('Exception when WaitTillElementPresent : %s' %e)
            pass

    if not result:
        print("Element not found with %s : %s" % (locator, elementTag))
    driver.implicitly_wait(3)
    return result


def tearDown(driver):
    try:
        driver.close()
        print("Driver Closed Successfully")
    except Exception as e:
        print(e)
        pass

    try:
        driver.quit()
        print("Driver Quit Successfully")
    except Exception as e:
        print(e)


def LoadNaukri():
    """Open Chrome to load Naukri.com"""
    options = Options()
 #   options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")  # ("--kiosk") for MAC
    options.add_argument("--disable-popups")
    options.add_argument("--disable-gpu")



    # updated to use ChromeDriverManager to match correct chromedriver automatically
    driver = None
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    except:
        driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(NaukriURL)
    return driver


def naukriLogin():
    """ Open Chrome browser and Login to Naukri.com"""
    status = False
    driver = None

    try:
        driver = LoadNaukri()

        if "naukri" in driver.title.lower():
            print("Website Loaded Successfully.")

        emailFieldElement = None
        if is_element_present(driver, By.ID, "emailTxt"):
            emailFieldElement = GetElement(driver, "emailTxt", locator="ID")
            time.sleep(1)
            passFieldElement = GetElement(driver, "pwd1", locator="ID")
            time.sleep(1)
            loginXpath = "//*[@type='submit' and @value='Login']"
            loginButton = driver.find_element_by_xpath(loginXpath)

        elif is_element_present(driver, By.ID, "usernameField"):
            emailFieldElement = GetElement(driver, "usernameField", locator="ID")
            time.sleep(1)
            passFieldElement = GetElement(driver, "passwordField", locator="ID")
            time.sleep(1)
            loginXpath = '//*[@type="submit"]'
            loginButton = driver.find_element_by_xpath(loginXpath)

        else:
            print("None of the elements found to login.")

        if emailFieldElement is not None:
            emailFieldElement.clear()
            emailFieldElement.send_keys(username)
            time.sleep(1)
            passFieldElement.clear()
            passFieldElement.send_keys(password)
            time.sleep(1)
            loginButton.send_keys(Keys.ENTER)
            time.sleep(1)
            
             # Added click to Skip button
            print("Checking Skip button")
            skipAdXpath = "//*[text() = 'SKIP AND CONTINUE']"
            if WaitTillElementPresent(driver, skipAdXpath, locator="XPATH", timeout=10):
                 GetElement(driver, skipAdXpath, locator="XPATH").click()
                 
        status = True
        return (status, driver)
                 
    except Exception as e:
        print(e)
    return (status, driver)

def uploadResume(driver):
    driver.switch_to.default_content()
    
    time.sleep(5)
    # Hover over the "My Naukri" dropdown menu
    my_naukri_menu = driver.find_element_by_link_text('View profile')
    my_naukri_menu.click()
    
    time.sleep(5)

    # Click on the "Upload New Resume" button
    upload_resume_button =driver.find_element_by_link_text('Update')
    driver.execute_script("arguments[0].click();", upload_resume_button)
    
    file_input = driver.find_element_by_xpath("//input[@type='file']")
    file_input.send_keys(resumePath)
    
    driver.implicitly_wait(10)

   
def mailNotify():
    
    # Email configuration
    
    # Email content
    subject = "Notification: Job Automation Complete"
    message = "This is to notify you that the job automation process has completed successfully."
    
    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    
    # Add the message body
    msg.attach(MIMEText(message, "plain"))
    
    # Create a secure SSL/TLS connection with the SMTP server
    smtp_server = "smtp.gmail.com"  # Update with your email provider's SMTP server
    smtp_port = 587  # Update with the appropriate port number    
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, mail_password)
    
        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email notification sent successfully!")

    except smtplib.SMTPException as e:
        print("Failed to send email notification:", e)

    finally:
    # Close the SMTP connection
        server.quit()


def main():
    print("-----Naukri.py Script Run Begin-----")
    driver = None
    try:
        status, driver = naukriLogin()
        
        if status:
            uploadResume(driver)
            mailNotify()
       
    except Exception as e:
        print(e)

    finally:
        tearDown(driver)
        

    print("-----Naukri.py Script Run Ended-----\n")


if __name__ == "__main__":
    
    load_dotenv("variables.env")
    
    # Variables and creds
    username = st.secrets['username']
    password = st.secrets['password']
    mob = st.secrets['mob']  # Type your mobile number here
    sender_email = st.secrets['sender_email']
    receiver_email = st.secrets['receiver_email']
    mail_password = st.secrets['mail_password']

    path = os.getcwd()
    resumePath = path + r"/CV.pdf"


    NaukriURL = "https://login.naukri.com/nLogin/Login.php"
    main()
