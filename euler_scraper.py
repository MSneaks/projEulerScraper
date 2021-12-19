import requests
from bs4 import BeautifulSoup
import time
import re


problem_dict = []
def getText(count,skip):
    print("page",count)
    if count == 1:
        url = 'https://projecteuler.net/archives'
    else:
        url = url = 'https://projecteuler.net/archives;page=' + str(count)
    try: 
        page = requests.get(url)
        html_code = page.content
    except Exception as e:
        print(e)
        print("Would not connect")

    try:
        soup = BeautifulSoup(html_code, 'html.parser')  #Parse html code
        for link in soup.find_all('tr'):
            text = str(link)
            #print(text)
            if skip < 1:
                skip+=1
                pass
            else:
                sanitizeText(text,problem_dict)
           # print(problem_dict)
        #print(problem_dict)
    except Exception as e:
        print(e)

def sortOnKey(d):
    d = sorted(d, key=lambda x: x[3], reverse=True)
    return d

def sanitizeText(text,d):
        s = text
        startProblemNumber = 'tr><td class="id_column">'
        endProblemNumber = '</td><td><a href='
        problemNumber = ( s[s.find(startProblemNumber)+len(startProblemNumber):s.rfind(endProblemNumber)])
        #print(problemNumber)

        startProblemLink ='<a href="'
        endProblemLink = '" title="Published'
        problemLink = ( s[s.find(startProblemLink)+len(startProblemLink):s.rfind(endProblemLink)])
        #print(problemLink)

        startName = re.search('([1-9]|0[1-9]|1[0-2]):[0-5][0-9] ([ap][m])">', text)
        #06:00 pm">
        if not startName:
            startProblemName = 0
        else:
            startProblemName = startName.end()
        endProblemName = '</a></td><td><div class='
        if not endProblemName:
            end = len(text)
        else:
            end = s.rfind(endProblemName)
        problemName = text[startProblemName:end]
        #print(problemName)

        startSolved = '<div class="center">'
        endSolved = '</div></td></tr>'
        numberSolved = ( s[s.find(startSolved)+len(startSolved):s.rfind(endSolved)])
        #print(numberSolved)
        arr = [problemNumber,problemLink,problemName,int(numberSolved)]
        d.append(arr)

def giveOutput(d,file):
    
    for i in d:
        s = ''
        s ="\n" + i[0] + " " + 'https://projecteuler.net/' + i[1] + " " + i[2] + " " + str(i[3]) + "\n"
        file.write(s)





skip = 0
for i in range(1,17):
  getText(i,skip)
  time.sleep(30)
problem_dict = sortOnKey(problem_dict)
file1 = open("euler_res.txt", "w", encoding="utf-8")
giveOutput(problem_dict,file1)
file1.close()