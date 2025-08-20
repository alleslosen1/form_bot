from functools import reduce
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


glob_page_qs = {}
glob_chrome_options = webdriver.ChromeOptions()
# glob_chrome_options.add_argument('--headless')
glob_chrome_options.add_experimental_option("detach", True)
glob_driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="139.0.7258.128").install()), options=glob_chrome_options)

def find_qs():
    global glob_page_qs
    elems = None
    hasNext = True
    while hasNext:
        try:
            titles = WebDriverWait(glob_driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, '//span[@class="M7eMe"]')))
            titles_text = reduce(lambda x, element: x + [element.get_attribute('textContent')], titles, [])
            for title in titles_text:
                if title not in glob_page_qs:
                    glob_page_qs[title] = {"id": "", "elems": [], "weights":[]}
                else:
                    break

            # question box
            parent_qs = glob_driver.find_elements(By.XPATH, '//div[@class="Qr7Oae" and not(contains(@class, "pQK2A"))]')
            for i in range(len(parent_qs)):
                # radio
                if len(parent_qs[i].find_elements(By.XPATH, './/div[contains(@class, "AB7Lab")]')) != 0:
                    elems = parent_qs[i].find_elements(By.XPATH, './/div[contains(@class, "AB7Lab")]')
                    glob_page_qs[titles_text[i]]['id'] = 'radio'
                    glob_page_qs[titles_text[i]]['elems'] = elems
                    continue
                # checkbox
                elif len(parent_qs[i].find_elements(By.XPATH, './/div[contains(@class, "uHMk6b")]')) != 0:
                    elems = parent_qs[i].find_elements(By.XPATH, './/div[contains(@class, "uHMk6b")]')
                    glob_page_qs[titles_text[i]]['id'] = 'checkbox'
                    glob_page_qs[titles_text[i]]['elems'] = elems
                    continue
                # dropdown
                elif len(parent_qs[i].find_elements(By.XPATH, './/span[@class="vRMGwf oJeWuf" and text()="Choose"]')) != 0:
                    chooses = parent_qs[i].find_elements(By.XPATH, './/span[@class="vRMGwf oJeWuf" and text()="Choose"]')
                    chooses[i].click()
                    ddbox = parent_qs[i].find_elements(By.XPATH, '//div[@class="OA0qNb ncFHed QXL7Te"]')
                    elems = ddbox[i].find_elements(By.XPATH, './/div[@class="MocG8c HZ3kWc mhLiyf OIC90c LMgvRb"]')
                    print(len(elems))
                    glob_page_qs[titles_text[i]]['id'] = 'dropdown'
                    glob_page_qs[titles_text[i]]['elems'] = elems
            
            next = find_next()
            if next.get_attribute('textContent').lower() != 'next':
                hasNext = False
            else: 
                next.click()
            time.sleep(1)

        except Exception as e:
            print(f'Failed to find title: {e}')

def find_next():
    try:
        nexts = WebDriverWait(glob_driver, 3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[class*=NPEfkd]')))
        return nexts[-2]
    except Exception as e:
        print(f'Failed to find next button: {e}')

        
def console():
    global glob_page_qs
    for key in glob_page_qs.keys():
        while True:
            try:
                w = [int(i) for i in input(f'{key}\nEnter weights: ').split()]
                prob_sum = reduce(lambda a, b: a + b, w)
                num_elems = len(glob_page_qs[key]['elems'])
                if prob_sum == 10 and len(w) == num_elems:
                    glob_page_qs[key]['weights'] = [x / 10 for x in w]  # Divide by 10 for NumPy
                    break
                else:
                    print(f'Sum {prob_sum} != 10 or {len(w)} weights != {num_elems} elements')
            except ValueError:
                print('Invalid input. Enter integers separated by spaces.')
                continue
    
    glob_driver.get(form_url)
    glob_chrome_options.headless = False

def main(form_url):
    glob_driver.get(form_url)
    find_qs()
    glob_driver.quit()
    console()


if __name__ == '__main__':
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdYTZb8v-wVrk5GU2QDCmG-t8EGSAyDHRiLTduYxGlwxmCBcQ/viewform"
    main(form_url)