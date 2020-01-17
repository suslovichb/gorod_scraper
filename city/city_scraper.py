from bs4 import BeautifulSoup
import urllib.request
import re
import os
import time

author_id = input("Enter author id: ")
picnumber = 1 #numeration start point
url = "https://gorod.dp.ua/photo/author.php?order=1&page=1&author_id={}".format(author_id)
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'lxml')
endpage = soup.find('a', string = "конец")
link = endpage.get('href')
endnumber = int(re.search('page=(.+?)&', link).group(1))
print('*******************************************************')

for pagenumber in range(1, endnumber+1):
    url = "https://gorod.dp.ua/photo/author.php?order=1&page={}&author_id={}".format(pagenumber, author_id)
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', class_ = 'photoset')
    pictures = table.find_all('img')
    for picture in pictures:
        piclink = re.sub('_s.jpg$', '.jpg', picture.get('src'))
        if re.search('star.gif', piclink):
            continue
        picname = str(picnumber) + '. ' + picture.get('alt')
        if re.search(r'[*:/|\<>?"]', picname):
            picname = str(picnumber)
        picnumber+=1
        urllib.request.urlretrieve(piclink, os.path.basename(picname + '.jpg'))
        print(picname + " ... Downloaded")
        print(piclink)
    print('------------------------------------------------------')

