from lxml import html
import requests
from itertools import cycle
from time import *
import unicodedata


class Pogodynka:
    pagetree = ""
    cloudCycle = cycle("")
    updateTime = ""

    def __init__(self):
        self.pagetree = self.getPageTree()
        self.updateTime = time()
        self.getDailyCloudFromPogodynka()

    def getPageTree(self):
        try:
            page = requests.get('http://www.pogodynka.pl/polska/prognoza_synoptyczna/warszawa_warszawa')
            return html.fromstring(page.content)
        except requests.exceptions.ConnectionError:
            return html.fromstring("<html></html>")

    def updatePageTree(self):
        if (time() - self.updateTime) > 10:
            self.updateTime  = time()
            print('request execution' + strftime("%H:%M %d %B %Y", localtime()))
            newPageTree = self.getPageTree()
            if self.pagetree != newPageTree:
                self.pagetree = newPageTree
                self.getDailyCloudFromPogodynka()

    def getTdFromPogodynka(self):
        self.updatePageTree()
        dailyData = self.pagetree.xpath('//td/text()')
        return dailyData

    def getDailyCloudFromPogodynka(self):
        try:
            cloud = self.pagetree.xpath("//div[@id='ico_now_under']//text()")[0]
            cloudArray =  cloud.strip(',').split(' ')
            self.cloudCycle = cycle(cloudArray)
        except IndexError:
            self.cloudCycle = cycle("")

    def getCloudElement(self):
        returnData = self.cloudCycle.next()
        encoded= unicodedata.normalize('NFKD',returnData)
	return encoded.encode('ASCII','ignore')

    def getDailyTemperatureFromPogdynka(self):
        try:
            return self.getTdFromPogodynka()[55][:-2] + "*C"
        except IndexError:
            return ""

    def getDailyWindFromPogodynka(self):
        try:
            wind = self.getTdFromPogodynka()[56]
            return wind.strip()
        except IndexError:
            return ""
