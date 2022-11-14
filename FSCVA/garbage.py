from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import time


def login_SSO():
    # chrome_options = Options()
    # # from selenium.webdriver.chrome.service import service
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(options=chrome_options)

    # driver.get(
    #     r"""https://id.quicklaunch.io/authenticationendpoint/login.do?commonAuthCallerPath=%2Fpassivests&forceAuth=false&passiveAuth=false&tenantDomain=flsouthern.edu&wa=wsignin1.0&wct=2022-10-21T13%3A15%3A25Z&wctx=rm%3D0%26id%3Dpassive%26ru%3D%252fcas%252flogin%253fservice%253dhttps%25253A%25252F%25252Fsso.flsouthern.edu%25252Fadmin%25252Fsecured%25252F414%25252Fapi%25252Fauth%25253Furl%25253Dhttps%25253A%25252F%25252Fsso.flsouthern.edu%25252Fhome%25252F414&wtrealm=https%3A%2F%2Fcas-flsouthern.quicklaunch.io%2F&sessionDataKey=0f8b7a5d-4491-4530-9fc1-61c3da9512c3&relyingParty=https%3A%2F%2Fcas-flsouthern.quicklaunch.io%2F&type=passivests&sp=flsouthernedu&isSaaSApp=false&authenticators=BasicAuthenticator:LOCAL"""
    # )
    driver.get("https://sso.flsouthern.edu/home/414")

    time.sleep(3.5)

    username = ""
    password = ""

    driver.find_element(By.ID, "branding-username").send_keys(username)
    driver.find_element(By.ID, "branding-password").send_keys(password)

    # id = branding-sumbit-button
    login_button = driver.find_element(By.ID, "branding-sumbit-button")
    login_button.click()

    time.sleep(3)

    try:
        # //*[@id="mfaDivId"]/form/div[2]/div[2]/div[1]
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
        time.sleep(5)

        canvas_card = driver.find_element(
            By.XPATH,
            r"""//*[@id="contentDiv"]/div[7]/div/div/div[1]""",
        )
        canvas_card.click()

        time.sleep(6)
        print("saving page")

        # trying to find elemtns with selenium
        test = driver.find_elements(By.CLASS_NAME, "ergWt_bGBk")

        print(test)

        # load the page into beautiful soup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        assignments = soup.find_all("span", {"class": "Grouping-styles__title"})
        # assignments = soup.find_all("span", class_="Grouping-styles__title")

        print(assignments)

        time.sleep(10)


login_SSO()
# now I will need to webscrape the html page
# br = RoboBrowser()
# br.open("https://flsouthern.instructure.com/?login_success=1", verify=True)

# link = "https://flsouthern.instructure.com/?login_success=1"
# src = str(br.parsed())
# soup = BeautifulSoup(src, "html.parser")

# assignments = soup.find_all("span", {"aria-hidden": "true"})
# #                                       fOyUs_bGBk fbyHH_bGBk fbyHH_bSMN

# class_names = soup.find_all(
#     "span", class_="enRcg_bGBk enRcg_dfBC enRcg_eQnG enRcg_bLsb"
# )

# test = soup.find("div", {"class": "PlannerItem-styles__type"})
# # assignments = soup.find_all("a", {"class": r"""fOyUs_bGBk fbyHH_bGBk fbyHH_bSMN"""})
# # assignments = soup.find_all("a", class_="fOyUs_bGBk fbyHH_bGBk fbyHH_bSMN")
# print(test)
# for i in range(len(assignments)):
#     tag = assignments[i].b
#     # tag.string
#     print(tag.string)
# temp = assignments[0]

# print(assignments[0])

# x path for clicking on canvas if sso is successful
# //*[@id="contentDiv"]/div[7]/div/div/div[1]
