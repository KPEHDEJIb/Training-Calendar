import time
from os import path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def get_sources_html():
    url = "https://sjbody.ru/members/login"
    url_t = "https://sjbody.ru/turniki"

    data = {
        "email": "dfsrarsdf@yandex.ru",
        "password": "NHBjeGRm"
    }

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(executable_path="/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(options=options, service=service)

    try:
        print("[+] Logging in...")
        driver.get(url=url)

        time.sleep(2)

        username = driver.find_element(By.NAME, "login")
        password = driver.find_element(By.NAME, "password")
        entry = driver.find_element(By.TAG_NAME, "button")

        username.send_keys(data["email"])
        password.send_keys(data["password"])
        entry.click()

        time.sleep(2)

        print("[+] Successfully logged in!")

        print("[+] Starting parsing weeks...")
        for i in range(1, 13):
            print(f"[+] Proceed {i}...", end='')
            try:
                driver.get(url=url_t + str(i))

                timeout = 5
                try:
                    element_present = expected_conditions.presence_of_element_located((By.CLASS_NAME, 'tn-atom'))
                    WebDriverWait(driver, timeout).until(element_present)
                except TimeoutException:
                    print("Timed out waiting for page to load")
                time.sleep(0.5)

                with open(path.abspath(f"scraped_websites/index{i}.html"), 'w', encoding="utf-8") as f:
                    f.write(driver.page_source)
            except Exception as e:
                print(" Error:")
                print(e)
            print(" Done")

    except Exception as e:
        print(e)
    finally:
        print("[+] Stopping requests...")
        driver.close()
        driver.quit()
        print("[+] Requests are successfully stopped!")


get_sources_html()
