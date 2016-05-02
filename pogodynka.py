from lxml import html
import requests

def getPageTree():
    page = requests.get('http://www.pogodynka.pl/polska/prognoza_synoptyczna/warszawa_warszawa')
    return html.fromstring(page.content)


def getTdFromPogodynka():
    dailyData = getPageTree().xpath('//td/text()')
    return dailyData

def getDailyCloudFromPogodynka():
    return getPageTree().xpath("//div[@id='ico_now_under']//text()")[0]


def getDailyTemperatureFromPogdynka():
    return getTdFromPogodynka()[55]


def getDailyWindFromPogodynka():
    return getTdFromPogodynka()[56]
