#-*- coding: utf-8 -*-

import urllib3
from bs4 import BeautifulSoup

def split_text(url, no, subject_name):
    connection_pool = urllib3.PoolManager()

    resp = connection_pool.request('GET',url )

    soup = BeautifulSoup(resp.data, 'html.parser')
    #print(title)

    text = soup.find(id = 'articleBodyContents')

    string = text.get_text()
    string = string.replace('\n', '')
    string.strip()
    string_temp = string

    children = text.findChildren()

    for child in children:
        temp_text = child.text
        if temp_text != '' and string.count(temp_text) >= 1:
                string = string.replace(temp_text, '')
    if len(string) == 0:
        string = string_temp


    file_name = soup.title.get_text().replace(': 네이버 뉴스', '')
    file_name = file_name.replace("\"", '')
    file_name = file_name.replace("\'", '')
    file_name = file_name.replace("[", '')
    file_name = file_name.replace("]", '')
    file_name = file_name.replace("<", '')
    file_name = file_name.replace(">", '')
    file_name = file_name.replace("?", '')
    file_name.strip()
    number = str(no)
    file_name = '/home/alimiuser/sns_alimi/'+ subject_name + '/' + number + "_" + file_name +'.txt'
    f = open(file_name, 'w', encoding='utf-8')
    f.write(string)
    f.close

    return string

#print(text)
#print (text.get_text())
#print (str)
#f = open('test_soup.txt', 'w')
#f.write(str(soup))
#f.close()
#soup = BeautifulSoup(urllib3.(target_url).read())
#print (soup)
