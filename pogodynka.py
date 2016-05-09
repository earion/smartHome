from lxml import html
import requests
from itertools import cycle


class Pogodynka:
    pagetree = ""
    cloudCycle = cycle("")

    def __init__(self):
        self.pagetree = self.getPageTree()

    def getPageTree(self):
        try:
            page = requests.get('http://www.pogodynka.pl/polska/prognoza_synoptyczna/warszawa_warszawa')
            return html.fromstring(page.content)
        except requests.exceptions.ConnectionError:
            return html.fromstring("<html></html>")

    def updatePageTree(self):
        newPageTree = self.getPageTree()
        if self.pagetree != newPageTree:
            self.pagetree = newPageTree
            return 1
        else:
            return 0

    def getTdFromPogodynka(self):
        self.updatePageTree()
        dailyData = self.pagetree.xpath('//td/text()')
        return dailyData

    def getDailyCloudFromPogodynka(self):
        try:
            cloud = self.pagetree.xpath("//div[@id='ico_now_under']//text()")[0]
            self.cloudCycle = cycle(cloud.strip(',').split(' '))
        except IndexError:
            self.cloudCycle = cycle("")

    def getCloudElement(self):
        if self.updatePageTree() == 0:
            return self.cloudCycle.next()
        else:
            self.getDailyCloudFromPogodynka()
            return self.cloudCycle.next()


    def getDailyTemperatureFromPogdynka(self):
        try:
            return self.getTdFromPogodynka()[55][:-2] + "*C"
        except IndexError:
            return ""

    def getDailyWindFromPogodynka(self):
        try:
            wind =  self.getTdFromPogodynka()[56]
            return wind.strip()
        except IndexError:
            return ""
