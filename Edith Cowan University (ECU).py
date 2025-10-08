from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver.support.ui import Select
import re
import argparse

# 创建一个解析器
parser = argparse.ArgumentParser(description="Process some integers.")

# 添加命令行参数 --start 和 --end
parser.add_argument('--port', type=str, default='9222', required=True, help="The port number.")

# 解析命令行参数
args = parser.parse_args()

options = webdriver.ChromeOptions()
chrome_options = Options()
# chrome_options.page_load_strategy = 'eager'
chrome_options.debugger_address = "127.0.0.1:" + args.port

driver = webdriver.Chrome(options=chrome_options)

final_data = []


# driver.get('https://www.ecu.edu.au/schools/engineering/staff')
# driver.get('https://www.ecu.edu.au/schools/business-and-law/faculty')
# driver.get('https://www.ecu.edu.au/schools/education/staff')
# driver.get('https://www.ecu.edu.au/schools/medical-and-health-sciences/our-staff')
# driver.get('https://www.ecu.edu.au/schools/nursing-and-midwifery/our-staff')
# driver.get('https://www.ecu.edu.au/schools/science/staff')
# driver.get('https://www.waapa.ecu.edu.au/about/our-staff')
driver.get('https://www.ecu.edu.au/schools/arts-and-humanities/staff')


print(driver.title)
time.sleep(5)
                                            
list_items0 = driver.find_elements(By.XPATH, r'//*[@id="content-2013"]/div[1]/div/ul[*]/li[*]/a | //div[starts-with(@id,"content_container_")]/div/div//h3/a | //*[@id="component_1094843"]/ul[*]/li[*]/a | //div[starts-with(@id,"component_")]//div/h3/a | //div[starts-with(@id,"content_container_")]/ul[*]/li[*]/a')

teacher_list = []
for num0, list0 in enumerate(list_items0): 
    href = list0.get_attribute('href')
    # print(href)
    teacher_list.append(href)

for href in teacher_list:
    all_data = {}
    
    try:
        driver.get(href)
        time.sleep(3)
        all_data['website'] = driver.current_url
        print(driver.current_url)
    except:
        continue

    try:                             
        name = driver.find_element(By.XPATH, r'//*[@id="h2-container"]/h2')
        pattern = re.compile(r'^((?:Honorary Associate )?Professor|(?:Associate )?Professor|Dr|Mr|Ms|Mrs)\s+(.+)$')
        m = pattern.match(name.text)
        all_data['title'] = m.group(1)
        all_data['full name'] = m.group(2)
    except:
        continue

    try:
        org_unit = driver.find_element(By.XPATH, r'//*[@id="content-2013"]/div/div/h3')
        # print(org_unit.text)
        all_data['org_unit'] = org_unit.text
    except:
        pass

    try:                                     
        email = driver.find_element(By.ID, "staff-details-email").find_element(By.XPATH, "following-sibling::td/a")
        # print(email.text)
        all_data['email'] = email.text
    except:
        pass

    try:
        orcid = driver.find_element(By.ID, "staff-details-orcid").find_element(By.XPATH, "following-sibling::td/a")
        # print(orcid)
        all_data['orcid'] = orcid.text
    except:
        pass

    all_info = ''
    try:                       
        researchs = driver.find_elements(By.CSS_SELECTOR, 'div[id^="component_"] p, div[id^="component_"] h3, div[id^="content_"] p, div[id^="content_"] h3')
        i = 0
        while(i < len(researchs) and researchs[i].tag_name != 'h3'):
            all_info += researchs[i].text
            all_info += '\n'

            i += 1
    except:
        pass
    all_data['brief introduction'] = all_info

    print(all_data)
    final_data.append(all_data)
    time.sleep(3)


with open('Edith Cowan University (ECU) 08.json', 'w') as json_file:
    json.dump(final_data, json_file)
