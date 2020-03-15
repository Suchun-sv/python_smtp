from flask import Flask,request
import yaml
import smtplib
import json
from email.mime.text import MIMEText
from email.header import Header

app = Flask(__name__)
def parseconfig():
    """
    Read the config file
    mail_addr = xxx@126.com
    password = xxxxxx
    Note: the password should be specified in the web site like qq or 126(Authorization code)
    """
    with open('config.yaml') as f:
        config = yaml.load(f)
        return config



def check(message):
    config = parseconfig()
    if config.has_key('mail_addr') and config.has_key('password') and config.has_key('server_addr'):
        pass
    else:
        print('Cannot get the config, Please check the .yaml file')
        return False
    if message.has_key('to') and message.has_key('text'):
        pass
    else:
        print('Cannot parse the form dict, check the form')
        return False
    return True

def send(message):
  if not check(message):
    return False
  config = parseconfig()
  from_addr = config['mail_addr']
  password = config['password']
 
  to_addr = message['to']

  smtp_server = config['server_addr']
 

  msg = MIMEText(message['text'],'plain','utf-8')
 

  msg['From'] = Header(from_addr)
  msg['To'] = Header(to_addr)
  if message.has_key('subject'):
    msg['Subject'] = Header(message['subject'])
  else:
    msg['Subject'] = Header('Defalut Subject')
    
  try:  
    # Start the transmission with SSL
    server = smtplib.SMTP_SSL(smtp_server, 465)
    #server.ehlo()
    
    #server.connect(smtp_server)
    # login
    #server.starttls()
    server.login(from_addr, password)
    # send mail
    server.sendmail(from_addr, to_addr, msg.as_string())
    # quit
    server.quit()
  except Exception as e:
    print(e)
    print("Find error when tring to login and send mail!")
    return True



@app.route('/', methods=['GET', 'POST']) 
def parse():
    if request.method == 'POST':
        print(request.form)
        _return = send(request.form.to_dict())
        if _return:
          return "200"
        else:
          return "500"


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 25)
