import json

filenames = []
subSet = {}


def write_to_json(js,file):
    _json = open(f"{file}.json", 'w')
    _json.write(json.dumps(js))
    _json.close()

    
def getAllFileNames():
    import os
    path = "./json"
    dirList = os.listdir(path)

    return dirList


def serializeSubjects(sub):
    if sub != "name" :
        subSet[sub] = {'count': subSet[sub]['count']+1} if sub in subSet else {'count': 1}

def getSubjects():
    for file in filenames:
        print("operating on file: ",file)
        fp = open(f"./json/{file}")
        js = json.load(fp)

        for val in js.values():
            for sub in val.keys():
                serializeSubjects(sub)

def main():
   global filenames 
   filenames = getAllFileNames()
   getSubjects()
   write_to_json(subSet,"subjects")

if __name__ == "__main__":
    main()