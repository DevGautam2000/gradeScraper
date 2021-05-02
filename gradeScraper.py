import json

import requests
from bs4 import BeautifulSoup

url = ''  # add required url
cardUrl = []
joinUrl = "https://result.smuexam.in/grade.php?subid="
headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
                  'Version/11.0 Mobile/15A5341f Safari/604.1'}
fileName = ""


def readFile(infoDict, line, name, readTextFile):
    subCode = "CODE"
    credit = 0.0
    while line:
        # print(f"line1: {line}")
        line = line.strip().split()
        # print(f"line2: {line}")

        if (len(line) > 0 and line[0] == "File") or (len(line) > 0 and (
                line[0] == "P>35" or line[2] == "F<35" or line[0] == "Last" or line[0] == "/UNIVERSAL")):
            break
        elif (len(line) == 0 or line[0][0:3] == "REG" or line[0][0:3] == "SIK" or line[0][0:3] == "GRA" or line[0][
                                                                                                           0:3] == "Abb" or
              line[0][0:3] == "Abs" or line[0][0:3] == "S>=" or line[0][0:3] == "P>=" or line[0][0:3] == "Sto" or
              line[0][0:3] == "Gra"):
            line = readTextFile.readline()
            continue
        elif line[0] == "Subject":
            if line[1] == "Code":
                subCode = line[3]
            elif line[1] == "Title":
                i = 3
                while i < len(line):
                    name += line[i] + " "
                    i += 1
            elif line[1] == "Credit":
                if len(line) >= 4:
                    credit = float(line[3][0:3])
        else:
            # print(f"reg: {reg}")
            detailDict = {}
            if line[0] == "S>89," or line[0] == "Lower":
                break

            reg = int(line[0])

            infoDict[reg] = infoDict.get(reg, {})
            detailDict['sub'] = name
            detailDict['int'] = line[1]
            detailDict['ext'] = line[2]
            detailDict['tot'] = line[3]
            detailDict['grade'] = line[4]
            detailDict['credit'] = credit
            infoDict[reg][subCode] = detailDict
        line = readTextFile.readline()


def getCardUrl(soup):
    for div in soup.find_all("div", {"class": "card-body"}):
        for para in div.select("p"):
            for link in para.select("a"):
                href = link['href']
                subCode = href[href.index('=') + 1:]
                cardUrl.append(joinUrl + subCode)


def readFromFile(infoDict, name):
    read = open(f"{fileName}.txt")
    line = read.readline()
    readFile(infoDict, line, name, read)
    read.close()


def writeToFile(soup):
    write = open(f"{fileName}.txt", "w")
    write.write(soup.find('pre').getText())
    write.close()


def dumpJson(infoDict):
    jsonFinal = open(f"{fileName}.json", "w")
    jsonFinal.write(json.dumps(infoDict))
    jsonFinal.close()


def main():
    infoDict = {}  # will contain the final data
    session = requests.Session()  # create session
    body = session.get(url.strip(), headers=headers)
    soup = BeautifulSoup(body.content, 'lxml')

    getCardUrl(soup)

    for linkUrl in cardUrl:
        name = ""
        body = session.get(linkUrl.strip(), headers=headers)
        soup = BeautifulSoup(body.content, 'lxml')

        writeToFile(soup)
        readFromFile(infoDict, name)

    dumpJson(infoDict)


if __name__ == "__main__":
    main()
