from selenium import webdriver

import os

osu = "C:\\Users\\matia\\AppData\\Local\\osu!\\"
downloads = "C:\\Users\matia\Downloads\\"

driver = webdriver.Chrome()
driver.get("https://osu.ppy.sh")

songList = []
import re

def updateSongs():
    global songList
    regex = re.compile('^\d+')
    l = filter(regex.match, os.listdir(osu+"Songs"))
    songList = [int(x.split(" ")[0]) for x in l]

updateSongs()

def openFiles():
    for osuFile in os.listdir(downloads):
        if osuFile.endswith(".osz"):
            os.startfile(downloads+osuFile)
    updateSongs()    

def download(x,check=False):
    if x not in songList:
        driver.get("https://osu.ppy.sh/beatmapsets?m=0&q="+str(x))
        if check:
            try:
                driver.find_element_by_class_name('beatmapsets__empty')
            except:
                driver.get("https://osu.ppy.sh/beatmapsets/"+str(x)+"/download")
        else:
            driver.get("https://osu.ppy.sh/beatmapsets/"+str(x)+"/download")
            
def topRanks(num=10):
    driver.get("https://osu.ppy.sh/beatmapsets?m=0")
    while len(driver.find_elements_by_class_name('beatmapset-panel__header'))<num:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    l = [int(x.get_attribute("href")[len("https://osu.ppy.sh/beatmapsets/"):]) for x in driver.find_elements_by_class_name('beatmapset-panel__header')]
    for x in l[:num]:
        download(x)
    openFiles()

if len(sys.argv)==2:
    topRanks(int(sys.argv[1]))
else:
    topRanks()
