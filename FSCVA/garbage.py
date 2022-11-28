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

    username = "sclaycomb"
    password = "Harley351@chai"

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
            print(tags[i].getText())
        #     s = str(tags[i])
            if("due" in s):
                assignments.append(tags[i].getText())
        #         print(assignments[i])
        #     del assignments[i]

        # //*[@id="global_nav_dashboard_link"]

        time.sleep(10)

        # soup = BeautifulSoup(driver.page_source, "html.parser")
        # print(soup.prettify())

        # soup = BeautifulSoup(driver.page_source, "html.parser")
        # assignments = soup.find_all("span", class_="ergWt_bGBk")
        # print(assignments)

        # # class="ergWt_bGBk"
        # test = driver.find_elements(By.CLASS_NAME, "ergWt_bGBk")
        # print(test)

        # wait = WebDriverWait(driver, 10)
        # # element = wait.until(EC.text_to_be_present_in_element(
        # #     (By.CLASS_NAME, "fOyUs_bGBk blnAQ_bGBk blnAQ_cVrl blnAQ_drOs"), "Tomorrow"))

        # # print the html at this point
        # element = wait.until(EC.visibility_of_all_elements_located(
        #     (By.CLASS_NAME, "ergWt_bGBk")))

        # print(element)
        # element = WebDriverWait(driver, 900).until(
        #     EC.text_to_be_present_in_element(
        #         (By.CLASS_NAME, "enRcg_bGBk enRcg_cMDj enRcg_bdMA enRcg_eQnG"), "Today")
        # )

        # print(element)

        # time.sleep(8)

        # wait until something with this class shows up
        # element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located(
        #         (By.CLASS_NAME, "styles__secondary"))
        # )
        # print("elem", element)


login_SSO()

# now I will need to webscrape the html page
# br = RoboBrowser()
# br.open("https://flsouthern.instructure.com/?login_success=1", verify=True)

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
