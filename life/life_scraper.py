from bs4 import BeautifulSoup
import urllib.request
import re
import os
import time

author_id = input("Enter author id: ")
picnumber = 1 #pic numeration start point
url = "https://gorod.dp.ua/myfoto/author.php?page=1&id={}".format(author_id)
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'lxml')
endpage = soup.find('a', string = "Конец")
link = endpage.get('href')
endnumber = int(re.search('page=(.+?)&', link).group(1))
print('\n*********************************************************')

for pagenumber in range(1, endnumber+1):
    url = "https://gorod.dp.ua/myfoto/author.php?page={}&id={}".format(pagenumber, author_id)
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    pictures = soup.find_all('img', {'src': re.compile(r'userfoto')})
    for picture in pictures:
        piclink = "https://gorod.dp.ua/" + re.sub('_s.jpg$', '.jpg', picture.get('src'))
        picname = str(picnumber) + '. ' + picture.get('alt')
        if re.search(r'[*:/|\<>?"]', picname):
            picname = str(picnumber)
        picnumber+=1
        urllib.request.urlretrieve(piclink, os.path.basename(picname + '.jpg'))
        print(picname + " ... Downloaded")
        print(piclink)
    print("\nPage {} parsed\n".format(pagenumber))
    print('--------------------------------------------------------')
