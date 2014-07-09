import urllib
import sys
import http.cookiejar
import json

cookie = http.cookiejar.CookieJar()
cjhdr = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(cjhdr)
urllib.request.install_opener(opener)

url = "YOUR OWN MEDIAWIKI SITE/api.php"
pagetitle = "PAGENAME"
username = "USERNAME"
password = "PASSWORD"

def request(opener, postdata):
      params = urllib.parse.urlencode(postdata).encode('utf-8')
      data = opener.open(url, params)
      return data

def getToken(opener):
      postdata = {'format':'json',
                  'action':'login',
                  'lgname':username,
                  'lgpassword':password}
      data = request(opener, postdata)
      token = json.loads(data.read().decode('utf-8'))["login"]["token"]
      return token

def login(opener):
      postdata = {'format':'json',
            'action':'login',
            'lgname':username,
            'lgpassword':password,
            "lgtoken":getToken(opener)}
      data = request(opener, postdata)
      print(json.loads(data.read().decode('utf-8')))

def getEditToken(opener):
      postdata = {'format':'json',
                  'action':'query',
                  'prop':'info',
                  'intoken':'edit',
                  'titles':'Mediawiki'}
      data = request(opener, postdata)
      edittoken = json.loads(data.read().decode('utf-8'))['query']['pages']['-1']['edittoken']
      return edittoken

def addText(opener, title, text):
      postdata = {'format':'json',
                  'action':'edit',
                  'title' : pagetitle,
                  'section':"new",
                  'summary': title,
                  'text': text ,
                  'token':getEditToken(opener)}
      data = request(opener, postdata)
      print(data.read().decode('utf-8'))

def editText(opener, section, text):
      postdata = {'format':'json',
                  'action':'edit',
                  'title' : pagetitle,
                  'section': section + 1,
                  'summary': "edit",
                  'text': getText(section) + '\n' + text,
                  'token':getEditToken(opener)}
      data = request(opener, postdata)
      print(data.read().decode('utf-8'))

def getSections():
      opener = urllib.request.build_opener(cjhdr)
      postdata = {'format':'json',
                  'action':'parse',
                  'prop':'sections',
                  'page':pagetitle}
      data = request(opener, postdata)
      rawdata = json.loads(data.read().decode('utf-8'))['parse']['sections']
      return {data['line']:index for (index, data) in enumerate(rawdata)}

def getText(section):
      opener = urllib.request.build_opener(cjhdr)
      postdata = {'format':'json',
                  'action':'query',
                  'prop':'revisions',
                  'rvprop':'content',
                  'rvsection':section + 1,
                  'titles':pagetitle}
      data = request(opener, postdata)
      rawdata = json.loads(data.read().decode('utf-8'))
      return rawdata['query']['pages']['30']['revisions'][0]['*']
      

login(opener)
      
