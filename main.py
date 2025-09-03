
from functools import reduce
import random as rand
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

weights = []
k = int
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdYTZb8v-wVrk5GU2QDCmG-t8EGSAyDHRiLTduYxGlwxmCBcQ/viewform?usp=header"


def prompt_weights():
    rand.seed(333666999)
    q_counter = 1
    try:
        responses = int(input('Enter number of responses: '))
    except Exception as e:
        print(f'Error - {e}')

    while True:
        weight = input(f'Enter weights for question {q_counter}: ')
        if weight == 'x':
            break
        weight = weight.split(' ')
        if weight[0] == 'd':
            weight = [int(i) for i in weight[1:]]
            weight = [bool(rand.randint(1, 100) <= i) for i in weight]
            weights.append(weight)
        else:
            try:
                weight = [int(i) for i in weight]
                weights.append(rand.choices(range(len(weight)), weight, k=responses))
            except Exception as e:
                print(f'Error - {e}')
        q_counter += 1
    print(weights)


def open():
    global glob_chrome_options
    global glob_driver
    
    glob_chrome_options = webdriver.ChromeOptions()
    # glob_chrome_options.add_argument('--headless')
    glob_chrome_options.add_experimental_option("detach", True)
    glob_driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="139.0.7258.128").install()), options=glob_chrome_options)
    glob_driver.get(form_url)


def find_next():
    try:
        nexts = WebDriverWait(glob_driver, 3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[class*=NPEfkd]')))
        return nexts[-2]
    except Exception as e:
        print(f'Failed to find next button: {e}')



def fill_qs():
    for iter in range(len(weights[0])):
        open()
        hasNext = True
        total_q_counter = 0
        while hasNext:
            try:
                parent_qs = glob_driver.find_elements(By.XPATH, '//div[@class="Qr7Oae" and not(contains(@class, "pQK2A"))]')
                for i in range(len(parent_qs)):
                    if len(parent_qs[i].find_elements(By.XPATH, './/div[contains(@class, "AB7Lab")]')) != 0:    # radio
                        elems = parent_qs[i].find_elements(By.XPATH, './/div[contains(@class, "AB7Lab")]')
                        elems[weights[total_q_counter][iter]].click()

                    elif len(parent_qs[i].find_elements(By.XPATH, './/div[contains(@class, "uHMk6b")]')) != 0:  # checkbox
                        elems = parent_qs[i].find_elements(By.XPATH, './/div[contains(@class, "uHMk6b")]')
                        for j in range(len(elems)):
                            if weights[total_q_counter][j]:
                                elems[j].click()
                                
                    elif len(glob_driver.find_elements(By.XPATH, './/span[@class="vRMGwf oJeWuf" and text()="Choose"]')) != 0:  # dropdown
                        chooses = glob_driver.find_elements(By.XPATH, './/span[@class="vRMGwf oJeWuf" and text()="Choose"]')
                        chooses[i].click()
                        time.sleep(0.7)
                        ddbox = parent_qs[i].find_element(By.XPATH, '//div[@class="OA0qNb ncFHed QXL7Te"]')
                        elems = ddbox.find_elements(By.XPATH, './/div[@class="MocG8c HZ3kWc mhLiyf OIC90c LMgvRb"]')
                        elems[weights[total_q_counter][iter]].click()
                        time.sleep(0.5)
                    total_q_counter += 1

                next = find_next()
                if next.get_attribute('textContent').lower() != 'next':
                    hasNext = False
                else: 
                    next.click()
                time.sleep(1)
                
            except Exception as e:
                print(f'Error - {e}')
                glob_driver.quit()
                break
        
        submit = glob_driver.find_elements(By.CSS_SELECTOR, 'span[class*=NPEfkd]')
        submit[-2].click()
        time.sleep(0.5)
        glob_driver.quit()
    


prompt_weights()


fill_qs()


glob_driver.quit()