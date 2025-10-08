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

#  从第一页开始读取
for num in range(args.start, args.end):
    print(driver.title)
    driver.get(r'https://findanexpert.unimelb.edu.au/searchresults?category=profile&pageNumber=' + str(num) + '&q=&sorting=mostRecent')
    time.sleep(5)
    

    # # 获取页面完整的 HTML 内容
    # html_content = driver.page_source
    # print(html_content)                           
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="app"]/main/div/div/div[2]/div/div/div[2]/div/div[*]/div/div/div[2]/div/a')

    teacher_list = []
    for num0, list0 in enumerate(list_items0): 
        href = list0.get_attribute('href')
        print(href)
        teacher_list.append(href)

    for href in teacher_list[:2]:
        all_data = {}
        
        try:
            driver.get(href)
            time.sleep(3)
            print(driver.current_url)
            all_data['website'] = driver.current_url
        except:
            continue

    time.sleep(100000)








