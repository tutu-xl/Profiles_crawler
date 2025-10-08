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
# chrome_options.page_load_strategy = 'eager'
chrome_options.debugger_address = "127.0.0.1:" + args.port

driver = webdriver.Chrome(options=chrome_options)

final_data = []

def extract_section(heading_text):
    """
    把某个 h3 标题下直到下一个 h3 之前的所有兄弟元素全部抓回来
    返回 List[str]，每个元素是 .text
    """
    # 1. 先找到这个 h3
    heading = driver.find_element('xpath', f"//h3[normalize-space()='{heading_text}']")

    # 2. 往后遍历所有兄弟节点
    content = []
    for el in heading.find_elements('xpath', 'following-sibling::*'):
        if el.tag_name == 'h3':          # 遇到下一个 h3 就停
            break
        content.append(el.text.strip())  # 去掉首尾空白
    return content

#  从第一页开始读取
for num in range(args.start, args.end):
    driver.get('https://site-search.scu.edu.au/s/search.html?f.Tabs%7Cscu%7Edep-people=People&collection=scu%7Escu-dep&sort=title&start_rank=' + str((num-1)*10+1))
    print(driver.title)
    time.sleep(5)

    # # 获取页面完整的 HTML 内容
    # html_content = driver.page_source
    # print(html_content)
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="main-content"]/div/div/div/div[2]/div[2]/div[1]/div[2]/h3/a')
                                        
    teacher_list = []
    for num0, list0 in enumerate(list_items0): 
        href = list0.get_attribute('href')
        # print(href)
        teacher_list.append(href)

    for href in teacher_list:
        all_data = {}
        all_data['website'] = href
        print(href)

        try:
            driver.get(href)
        except:
            continue
        time.sleep(3)

        try:
            full_name = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section/div/div/div[1]/h1')
            # print(full_name.text)
            all_data['full name'] = full_name.text
        except:
            continue

        try:
            title = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section/div/div/div[1]/p[2]')
            # print(title.text)
            all_data['title'] = title.text
        except:
            pass
        
        try:
            org_unit = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section/div/div/div[1]/p[3]/a')
            # print(org_unit.text)
            all_data['org_unit'] = org_unit.text
        except:
            pass
        
        try:
            telephone = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section/div/div/div[1]/dl//dt[text()="Telephone"]/following-sibling::dd[1]/a')
            # print(telephone.text)
            all_data['telephone'] = telephone.text
        except:
            pass
        
        try:
            email = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section/div/div/div[1]/dl//dt[text()="Email"]/following-sibling::dd[1]/a')
            # print(email.text)
            all_data['email'] = email.text
        except:
            pass
        
        try:
            orcid = driver.find_element(By.XPATH, r'//*[@id="main-content"]/div[1]/div/div[2]/span/a')
            # print(orcid.text)
            all_data['orcid'] = orcid.text
        except:
            pass
        
        
        # positions = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section/div/div/div[1]/p[1]/text()')
        # posotion = [degree.strip() for degree in positions.split(",")]

        all_info = ''
        # 获取所有h3标签
        try:
            all_info += '\n'.join(extract_section('Biography'))
        except:
            pass
        try:
            all_info += '\n'.join(extract_section('Research'))
        except:
            pass
        # print(all_info)
        all_data['brief introduction'] = all_info

        
        if all_info != '':
            final_data.append(all_data)
            print(all_data)
        time.sleep(2)
   
# print(final_data)
with open('Southern Cross University ' + str(args.start) + ' ' + str(args.end) + ' .json', 'w') as json_file:
    json.dump(final_data, json_file)

