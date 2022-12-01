from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_SSO():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome()
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://sso.flsouthern.edu/home/414")

    time.sleep(3.5)

    driver.find_element(By.ID, "branding-username").send_keys(username)
    driver.find_element(By.ID, "branding-password").send_keys(password)

    # id = branding-sumbit-button
    login_button = driver.find_element(By.ID, "branding-sumbit-button")
    login_button.click()

    time.sleep(3)

    try:
        security_button = driver.find_element(
            By.XPATH, r"""//*[@id="mfaDivId"]/form/div[2]/div[2]/div[1]"""
        )
        security_button.click()

        question = ""

        while True:
            question = driver.find_element(
                By.XPATH,
                r"""//*[@id="securityQuestionModal"]/div[3]/div/div/div[2]/div[2]/form/div[1]/div/p""",
            ).text
            print(question)

            if "movie" in question:
                break

            skip_button = driver.find_element(
                By.XPATH,
                r"""//*[@id="securityQuestionModal"]/div[3]/div/div/div[2]/div[2]/form/div[2]/button[2]""",
            )
            skip_button.click()

            time.sleep(2)

        # id for Answer: securityAnswer
        driver.find_element(By.ID, r"""securityAnswer""").send_keys("hot rod")
        time.sleep(3)

        submit_button = driver.find_element(
            By.XPATH,
            r"""//*[@id="securityQuestionModal"]/div[3]/div/div/div[2]/div[2]/form/div[2]/button[4]""",
        )
        submit_button.click()

        time.sleep(5)
        canvas_card = driver.find_element(
            By.XPATH,
            r"""//*[@id="contentDiv"]/div[7]/div/div/div[1]""",
        )
        canvas_card.click()

    # sometimes a security question won't be asked, so just click on the access canvas card
    except:
        print("no security question asked")
        time.sleep(3)

        canvas_card = driver.find_element(
            By.XPATH,
            r"""//*[@id="contentDiv"]/div[7]/div/div/div[1]""",
        )
        canvas_card.click()

        time.sleep(6)

        # for the love of god please load me into the dashboard with this
        driver.get("https://flsouthern.instructure.com/")
        time.sleep(4)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        tags = soup.find_all("span", class_="ergWt_bGBk")

        assignments = []
        for i in range(len(tags) - 1):
            s = str(tags[i].getText)
            if("due" in s):
                assignments.append(tags[i].getText())

        print(assignments)
        time.sleep(10)


login_SSO()

# now I will need to webscrape the html page
# br = RoboBrowser()
# br.open("https://flsouthern.instructure.com/", verify=True)

# link = "https://flsouthern.instructure.com/?login_success=1"
# time.sleep(3)
# src = str(br.parsed())
# soup = BeautifulSoup(src, "html.parser")

# driver = webdriver.Chrome()
# driver.get("https://flsouthern.instructure.com/?login_success=1")


# styles__secondary

# wait until something with this class shows up
# element = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "styles__secondary"))
# )


# test = soup.find_all("span", {"aria-hidden": "true"})

# print(len(test))
