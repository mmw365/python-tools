import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename
from configparser import ConfigParser

def get_newbooks_koto():
    print('start getting koto data')
    filename = './data/koto-' + date.today().strftime('%Y%m%d') + '.txt'
    f = open(filename, mode='w')
    page = 1
    checkNext = True
    while checkNext:
        print('getting page #{} ...'.format(str(page)))
        resp = requests.get('https://www.koto-lib.tokyo.jp/opw/OPW/OPWNEWBOOK.CSP?DB=LIB&WRTCOUNT=100&PAGE=' + str(page))
        bs = BeautifulSoup(resp.content, 'html.parser')
        elems = bs.find_all('div', class_='container')
        for elem in elems:
            trs = elem.find_all('tr')
            if(len(trs) < 101):
                checkNext = False
            for tr in trs:
                tds = tr.find_all('td')
                if len(tds) < 7 or tds[0].text.strip() == '受入日':
                    continue
                f.write(tds[2].text.strip() + ' ' 
                        + tds[3].text.strip() + ' '
                        + tds[4].text.strip() + '('
                        + tds[5].text.strip() + ')\n')
        page += 1
    f.close()
    print('finish getting koto data')

def get_newbooks_sumida():
    print('start getting sumida data')
    filename = './data/sumida-' + date.today().strftime('%Y%m%d') + '.txt'
    f = open(filename, mode='w')
    page = 1
    checkNext = True
    while checkNext:
        print('getting page #{} ...'.format(str(page)))
        resp = requests.get('https://www.library.sumida.tokyo.jp/newarrivalresult?14&ctg=01&code=000&sort=5&mv=100&pcnt={}&marcuse=0&lib'.format(str(page)))
        bs = BeautifulSoup(resp.content, 'html.parser')
        elems = bs.find_all('div', id='result')
        for elem in elems:
            secs = elem.find_all('section', class_='infotable')
            if(len(secs) < 100):
                checkNext = False
            for sec in secs:
                lnk = sec.find_all('a')
                items = sec.find_all('div', class_='item')
                dd = items[0].find_all('dd')
                f.write(lnk[0].text.strip() + ' ' 
                      + dd[2].text.strip() + ' (' 
                      + dd[0].text.strip() + ' '
                      + dd[1].text.strip() + ')\n')
        page += 1
    f.close()
    print('finish getting sumida data')

def check_new_arrivails():
    print('compare with yesterday''s data')
    todayDt = date.today().strftime('%Y%m%d')
    prevDt = (date.today() - timedelta(days=1)).strftime('%Y%m%d')

    with open('./data/koto-' + prevDt + '.txt') as f:
        prevbooks = [s.strip() for s in f.readlines()]
    with open('./data/koto-' + todayDt + '.txt') as f:
        newbooks = [s.strip() for s in f.readlines() if s.strip() not in prevbooks]
    with open('./data/koto-new-' + todayDt + '.txt', mode='w') as f:
        for b in newbooks:
            f.write(b + '\n')

    with open('./data/sumida-' + prevDt + '.txt') as f:
        prevbooks = [s.strip() for s in f.readlines()]
    with open('./data/sumida-' + todayDt + '.txt') as f:
        newbooks = [s.strip() for s in f.readlines() if s.strip() not in prevbooks]
    with open('./data/sumida-new-' + todayDt + '.txt', mode='w') as f:
        for b in newbooks:
            f.write(b + '\n')

def send_result_mail():
    print('send result mail')
    todayDt = date.today().strftime('%Y%m%d')
    config = ConfigParser()
    config.read("check_new_book_info.ini")

    msg = MIMEMultipart()
    msg['Subject'] = '江東区・墨田区の新着図書 ' + todayDt
    msg['To'] = config['mail']['to']
    msg['From'] = config['mail']['from']
    msg.attach(MIMEText('本日新着の資料です。'))

    path = './data/koto-new-' + todayDt + '.txt'
    with open(path, 'rb') as f:
        part = MIMEApplication(f.read(), Name=basename(path))
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(path))
    msg.attach(part)

    path = './data/sumida-new-' + todayDt + '.txt'
    with open(path, 'rb') as f:
        part = MIMEApplication(f.read(), Name=basename(path))
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(path))
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(config['mail']['from'], config['mail']['password'])
    server.send_message(msg)
    server.quit()

get_newbooks_koto()
get_newbooks_sumida()
check_new_arrivails()
send_result_mail()



 
 

