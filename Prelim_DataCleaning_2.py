import re
import numpy as np
from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
def lastCaps(sentence):
    caps = True
    i = 1
    while caps and len(sentence)>1 and i < 20:
        if i == 19:
            return ""
        if sentence[-i:].isupper() and "?" not in sentence[-i:] and "." not in sentence[-i:] and "!" not in sentence[-i:]:
            i += 1
        else:
            caps = False
            if (i == 1):
                return ""
            else:
                return sentence[-(i-1):]
def process_txt(html_soup):
    diag = html_soup.find_all(size="2")
    output = ""
    for text in diag:
        text = re.sub(r'\(.*\)', '', str(text))
        text = re.sub(r'\<.*\>', '', text)
        text = re.sub(r'\[.*\]', '', text)
        text = re.sub(r'\([^)]*\)', '', text)
        output += text + ' '
    output = output.replace("\n","")
    output = output.replace("\r","")
    output = output.replace("\xa0","")
    output = output.replace("\'","")
    test = output.split(":")
    
    toremove = []
    print("here1")
    for i in range(len(test)):
        try:
            if lastCaps(test[i]) != "":
                test[i+1] = lastCaps(test[i])+ ": " +test[i+1] 
            else:
                toremove.append(i+1)
        except:
            pass
    print("here2")
    test = np.delete(np.array(test),toremove)
    print("here")
    return test
        
episodes = []
for i in tqdm(range(1,38)):
    go = True
    j = 1
    while go:
        print("while {}-{}".format(i,j))
        url = "http://www.chakoteya.net/DoctorWho/{}-{}.htm".format(i,j)
        try:
            response = get(url)
            if "/park.js" in str(response.text):
                go = False
            else:
                html_soup = BeautifulSoup(response.text, 'html.parser')
                episodes.append(process_txt(html_soup))
                print("{}-{}".format(i,j))
                j += 1
        except:
            print("Failed: {}-{}".format(i,j))