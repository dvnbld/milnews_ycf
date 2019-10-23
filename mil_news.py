
import urllib.request as u
from html.parser import HTMLParser
import re
import smtplib
import json
from datetime import date
import milglobal

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0 
        self.data = []
        # self.at = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'class' and value == 'mainnewstd':
                    self.recording = 1
                # if name =='href':
                #     url = value
                #     self.at.append(url)
            
                
    def handle_data(self, data):
        if self.recording:
            data = re.sub(r"\xa0","",data)
            self.data.append(data)

    def handle_endtag(self, tag):
        if tag == 'tr' and self.recording:
            self.recording -=1

def date_today():
    today = date.today()
    return str(today)

def flatten_data(lst): 
    it = iter(lst) 
    res_dct = dict(zip(it, it)) 
    return res_dct

def news_parsing():
    url = "https://www.militarynews.ru/default.asp?pid=0&rid=1&lang=RU"
    p = MyHTMLParser()
    html = u.urlopen(url).read().decode('cp1251')
    p.feed(html)

    d = flatten_data(p.data)
    # d = milglobal.testData ### sample dict for testing

    return json.dumps(d, ensure_ascii=False, indent=4)

    p.close()

def send_emails(msg):
    server = smtplib.SMTP_SSL('smtp.yandex.com:465')
    server.ehlo()
    server.login(milglobal.sender_mail, milglobal.sender_pass)
    message = 'Subject: militarynews interfax рассылка {} \n\n{}'.format(date_today(),msg).encode('cp1251')
    server.sendmail(milglobal.sender_mail, milglobal.testTarget_mail, message)
    server.quit()

def handler(event, context):

    # newsdata = news_parsing()
    send_emails(news_parsing())

    data = '''
    <body style="background-color:black;">
    <p style="font-family:roboto; text-align: left; margin-left: 10px; margin-bottom: 3px; margin-top: 0px; font-size: 18pt; color:white;">Письмо отправлено!</p>
    </body>'''

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html; charset=UTF-8'
        },
        'isBase64Encoded': False,
        'body': data
    }

if __name__ == '__main__':
    # handler('','')
    # send_emails(news_parsing())
    print(news_parsing())
