import json
import requests
from bs4 import BeautifulSoup

fileName = "writer"

errors = []
subSet = {}
currentSem  = "23_may_june_2023"

url = "https://erp.smu.edu.in/SMITRESULTAPP/UpFiles/RELGRADE/RL000002"

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36'
}
infoDict = {}



  

def write_text_to_file(soup):
    write = open(f"{fileName}.txt", 'w')
    write.write(soup.getText())
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
                        'int': line[1],
                        'ext': line[2],
                        'tot': line[3],
                        'credit': credit,
                        'grade': line[4]
                    }

            except Exception as e:
                errors.append(e)
        line = read.readline()

def getTxt(subjectName):
    session = requests.Session()
    outerHtml = session.get(f"{url}/{subjectName}.txt", headers=headers)
    soup = BeautifulSoup(outerHtml.content, 'lxml')

    write_text_to_file(soup)
    read_file(infoDict)

def write_to_json(js,file):
    _json = open(f"{file}.json", 'w')
    _json.write(json.dumps(js))
    _json.close()


def main():
   subSet = json.load(open("subjects.json"))
   for sub in subSet:
       getTxt(sub)
       
   write_to_json(infoDict,currentSem)

if __name__ == "__main__":
    main()
    
