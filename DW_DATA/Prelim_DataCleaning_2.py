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
                return (0,"")
            else:
                return (i-1,sentence[-(i-1):])
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
    for i in range(len(test)):
        try:
            if lastCaps(test[i])[1] != "":
                test[i+1] = lastCaps(test[i])[1]+ ": " +test[i+1] 
                test[i] = test[i][:-lastCaps(test[i])[0]]
            else:
                toremove.append(i+1)
        except:
            pass
    test = np.delete(np.array(test),toremove)
    return test
        
episodes = []
for i in tqdm(range(1,38)):
    go = True
    j = 1
    while go:
        url = "http://www.chakoteya.net/DoctorWho/{}-{}.htm".format(i,j)
        response = get(url)
        if "/park.js" in str(response.text):
            go = False
        else:
            html_soup = BeautifulSoup(response.text, 'html.parser')
            episodes.append(process_txt(html_soup))
#            print("{}-{}".format(i,j))
            j += 1


import pickle

with open('D://updated//Chatty-V2//webscrap1.pkl', 'wb') as f:
   pickle.dump(episodes, f)