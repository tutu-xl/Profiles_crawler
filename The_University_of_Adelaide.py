from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import argparse

# 创建一个解析器
parser = argparse.ArgumentParser(description="Process some integers.")

# 添加命令行参数 --start 和 --end
parser.add_argument('--start', type=int, default=100, required=True, help="The starting number.")
parser.add_argument('--end', type=int, default=150, required=True, help="The ending number.")
parser.add_argument('--port', type=str, default='9222', required=True, help="The port number.")

# 解析命令行参数
args = parser.parse_args()

options = webdriver.ChromeOptions()
chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
chrome_options.debugger_address = "127.0.0.1:" + args.port

driver = webdriver.Chrome(options=chrome_options)

final_data = []

# 获取每个页面的info
def get_info(href):
    driver.get(href)
    time.sleep(1)
    # print(driver.title)
    all_data = {}
    all_data['website'] = href
    profile = driver.find_elements(By.XPATH, r'//*[@id="homepage-contact"]/div/a')
    
    if len(profile) != 0:
        try:
            name = driver.find_element(By.XPATH, r'//*[@id="ua-main-content"]/div[2]/div/h1')
            # all_data.append(name.text)
            all_data['name'] = name.text
            # print(name.text)
        except Exception as e:
            pass
        try: 
            position = driver.find_element(By.XPATH, r'//*[@id="homepage-contact"]/table/tbody/tr[1]/td')
            # all_data.append(position.text)
            all_data['position'] = position.text
            # print(position.text)
        except Exception as e:
            pass
        try:
            org_unit = driver.find_element(By.XPATH, r'//*[@id="homepage-contact"]/table/tbody/tr[2]/td/a')
            # all_data.append(org_unit.text)
            all_data['org_unit'] = org_unit.text
            # print(org_unit.text)
        except Exception as e:
            pass
        try:
            email = driver.find_element(By.XPATH, r'//*[@id="homepage-contact"]/table/tbody/tr[3]/td/a')
            # all_data.append(email.text)
            all_data['email'] = email.text
            # print(email.text)
        except Exception as e:
            pass
        try:
            telephone = driver.find_element(By.XPATH, r'//*[@id="homepage-contact"]/table/tbody/tr[4]/td/a')
            all_data['telephone'] = telephone.get_attribute('href')
            # all_data.append(telephone.get_attribute('href'))
            # print(telephone.get_attribute('href'))
        except Exception as e:
            pass
        
        driver.get(profile[0].get_attribute('href'))
        time.sleep(1)
        
        all_info = ""
        intro = driver.find_elements(By.XPATH, r'//*[@id="block-mainpagecontent"]/div/div/div/div[2]/div[1]/div[2]/div/div/div/p')
        if(len(intro) != 0):
            all_info += intro[0].text
        try:
            intro = driver.find_element(By.XPATH, r'//*[@id="my-research"]')
            text_list = [p.text for p in intro.find_elements('xpath', './/p')]
            all_info += '\n'.join(text_list)
        except NoSuchElementException as e:
            pass
        try:
            intro = driver.find_element(By.XPATH, r'//*[@id="block-mainpagecontent"]/div/div/div/div[2]/div[1]/div[1]/div/div/div/p')
            all_info += intro.text   
        except  NoSuchElementException as e:
            pass

        all_data['all_info'] = all_info
        # all_data.append(all_info)
        # print(intro.text)
    return all_data


#  从第一页开始读取
for num in range(args.start, args.end):
    driver.get('https://www.adelaide.edu.au/directory/atoz?dsn=directory.phonebook;orderby=last%2Cfirst%2Cposition_n;m=atoz;page=' + str(num))
    print(driver.title)
    time.sleep(2)

    # # 获取页面完整的 HTML 内容
    # html_content = driver.page_source
    # print(html_content)
    list_items0 = driver.find_elements(By.TAG_NAME, r"tr")

    teacher_list = []
    for num0, list0 in enumerate(list_items0):
        if num0 == len(list_items0)-1:
            break
        # print(list0)
        link = driver.find_element(By.XPATH, r'//*[@id="bztable1"]/tbody/tr[' + str(num0+1) + ']/td[2]/a')
        
        href = link.get_attribute('href')
        # print(href)
        teacher_list.append(href)

    for href in teacher_list:
        try:
            all_data = get_info(href)
        except:
            continue
        print(all_data)
        if len(all_data) != 1:
            final_data.append(all_data)

        # print(final_data)
        time.sleep(1)
   
print(final_data)
with open('Adelaide ' + str(args.start) + ' ' + str(args.end) + ' .json', 'w') as json_file:
    json.dump(final_data, json_file)
