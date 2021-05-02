"""
    AUTHOR: GAUTAM CHANDRA SAHA
    DATE & TIME: 10/05/21 AT 10:36 AM

"""
import json

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located as poel
from selenium.webdriver.support.wait import WebDriverWait

cgpa_uri = ''
grade_uri = ''
join_uri = 'https://result.smuexam.in/'
fileName = grade_uri[26:30]
errors = []

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36'
}


def main():
    cardUrl = []
    infoDict = {}
    session = requests.Session()
    outerHtml = session.get(grade_uri, headers=headers)
    soup = BeautifulSoup(outerHtml.content, 'lxml')

    get_all_card_uri(cardUrl, soup)

    for links in cardUrl:
        outerHtml = session.get(links, headers=headers)
        soup = BeautifulSoup(outerHtml.content, 'lxml')

        write_text_to_file(soup)
        read_file(infoDict)

    # print(len(infoDict))
    drive_browser(infoDict)
    write_to_json(infoDict)
    errors.clear()


def get_all_card_uri(cardUrl, soup):
    for div in soup.findAll('div', class_='card-body'):
        for para in div.select('p'):
            for links in para.select('a'):
                cardUrl.append(join_uri + links['href'])


def write_text_to_file(soup):
    write = open(f"{fileName}.txt", 'w')
    write.write(soup.find('pre').getText())
    write.close()


def read_file(infoDict):
    read = open(f"{fileName}.txt", 'r')
    read_text_from_file(infoDict, read)
    read.close()


def read_text_from_file(infoDict, read):
    code = ""
    sub = ""
    credit = 0

    line = read.readline()
    while len(line) > 0:
        line = line.split()

        if len(line) > 0 and line[0] == 'Subject':
            if line[1] == "Code":
                code = line[3]

            elif line[1] == "Title":
                sub = " ".join(line[3:])

            elif line[1] == "Credit":
                if len(line) >= 4:
                    credit = line[3]

        else:
            try:
                if len(line) > 0:
                    regId = int(line[0])
                    infoDict[regId] = infoDict.get(regId, {})
                    infoDict[regId][code] = {
                        'sub': sub,
                        'internal': line[1],
                        'external': line[2],
                        'total': line[3],
                        'credit': credit,
                        'grade': line[4]
                    }

            except Exception as e:
                errors.append(e)
        line = read.readline()


def drive_browser(infoDict):
    # count = 0

    name = "NA"
    for key in infoDict:
        try:
            driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
            wait = WebDriverWait(driver, 10)
            driver.get(cgpa_uri)

            driver.find_element_by_xpath(
                "//input[@name='search']").send_keys(key)

            driver.find_element_by_xpath(
                "//button[@class='searchButton']").click()

            generator = wait.until(
                poel((By.XPATH, "//section[@id='portfolio']/div/div/div[1]")))

            txt = generator.text.split('\n')
            if len(txt) > 1:
                joinString = txt[2]
                joinString = joinString.split(":")
                name = joinString[1].strip()
                # print(f"{count}) {name}")  # print statement here
                # count += 1
            infoDict[key]['name'] = name

            driver.close()

        except Exception as e:
            errors.append(e)
            # print(f"{key}: not found")


def write_to_json(infoDict):
    _json = open(f"{fileName}.json", 'w')
    _json.write(json.dumps(infoDict))
    _json.close()


if __name__ == "__main__":
    main()
