from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from Scrapper_headlines import article_market
from dotenv import load_dotenv
import os

def scrap_article(number):    
    load_dotenv()
    PASSWORD = os.getenv("PASSWORD")
    
    titles = article_market(number)

    # Initialize browser
    driver = webdriver.Chrome()

    # Go to login page
    driver.get("https://www.ft.com/login")

    # Fill in login fields
    driver.find_element(By.ID, "enter-email").send_keys("maxime.masson@edhec.com")
    driver.find_element(By.ID, "enter-email-next").click()

    # Wait for page to load
    wait = WebDriverWait(driver, 50)
    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'sso-redirect-button')))
    driver.find_element(By.ID, "sso-redirect-button").click()

    # Fill in login fields
    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'i0116')))
    driver.find_element(By.ID, "i0116").send_keys("maxime.masson@edhec.com")
    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'idSIButton9')))
    driver.find_element(By.ID, "idSIButton9").click()
    driver.find_element(By.ID, "i0118").send_keys(PASSWORD)

    # Submit login form
    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'idSIButton9')))
    driver.find_element(By.ID, "idSIButton9").click()
    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'idSIButton9')))
    driver.find_element(By.ID, "idSIButton9").click()

    #Scrap articles
    for i in range(len(titles)):
        print("Scrapping article ",i + 1)
        driver.get("https://www.ft.com" + titles[i][1])
        titles[i].append(driver.find_element(By.CSS_SELECTOR, "#site-content > div.article__content > div.article__content-body.n-content-body.js-article__content-body > div").text)
        
    driver.close()
    
    return titles