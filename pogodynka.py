from lxml import html
import requests

def getPageTree():
    try:
	page = requests.get('http://www.pogodynka.pl/polska/prognoza_synoptyczna/warszawa_warszawa')
    	return html.fromstring(page.content)
    except requests.exceptions.ConnectionError:
	return html.fromstring("<html></html>")

def getTdFromPogodynka():
    dailyData = getPageTree().xpath('//td/text()')
    return dailyData

def getDailyCloudFromPogodynka():
    try:
    	cloud =  getPageTree().xpath("//div[@id='ico_now_under']//text()")[0]
	return cloud.strip(',').split(' ')
    except IndexError:
	return ""

def getDailyTemperatureFromPogdynka():
    try:    
	return getTdFromPogodynka()[55][:-2] + "*C"
    except IndexError:
	return ""

def getDailyWindFromPogodynka():
    try:
	return getTdFromPogodynka()[56]
    except IndexError:
	return ""
