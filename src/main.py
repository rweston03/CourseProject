from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from udacity.scraper import udacity_scraper
from futurelearn.scraper import futurelearn_scraper
from edx.scraper import edx_scraper
from coursera.scraper import coursera_scraper
import os

PATH = "C:\Program Files (x86)\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")  # Opens an incognito window
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument("--disable-cache")  # Disables the cache
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-application-cache")  # Disable caching of HTML5 application data
chrome_options.add_argument("--disk-cache-size=0")  # Sets the disk cache size to 0
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--start-maximized")  # Start maximized
chrome_options.add_argument("--disable-extension")  # Disable extension
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
driver = webdriver.Chrome(PATH, options=chrome_options)

udacity_scraper(driver)
edx_scraper(driver)
coursera_scraper(driver)

projectDirectory = os.getcwd()
projectDirectory.replace("\\", "\\\\")
currentDirectory = projectDirectory + "\\src\\mooc_datasets"

courseraDirectory = projectDirectory + "\\src\\coursera\\datasets"
courseraDATFP = os.path.join(courseraDirectory, 'coursera.dat')
courseraSTATFP = os.path.join(courseraDirectory, 'stats.txt')
cd = open(courseraDATFP, 'r')
cs = open(courseraSTATFP, 'r')

edxDirectory = projectDirectory + "\\src\\edx\\datasets"
edxDATFP = os.path.join(edxDirectory, 'edx.dat')
edxSTATFP = os.path.join(edxDirectory, 'stats.txt')
ed = open(edxDATFP, 'r')
es = open(edxSTATFP, 'r')

udacityDirectory = projectDirectory + "\\src\\udacity\\datasets"
udacityDATFP = os.path.join(udacityDirectory, 'udacity.dat')
udacitySTATFP = os.path.join(udacityDirectory, 'stats.txt')
ud = open(udacityDATFP, 'r')
us = open(udacitySTATFP, 'r')


if os.path.exists(currentDirectory + "\\mooc.dat"):
    os.remove(currentDirectory + "\\mooc.dat")
if os.path.exists(currentDirectory + "\\mooc.csv"):
    os.remove(currentDirectory + "\\mooc.csv")
if os.path.exists(currentDirectory + "\stats.txt"):
    os.remove(currentDirectory + "\stats.txt")

filepathCSV = os.path.join(currentDirectory, 'mooc.csv')
c = open(filepathCSV, "a+")
filepathDAT = os.path.join(currentDirectory, 'mooc.dat')
f = open(filepathDAT, "a+")
filepathSTATS = os.path.join(currentDirectory, 'stats.txt')
s = open(filepathSTATS, "a+")

c.write("id,platform,institution,title,url,class_type,description,rating,rating_max,num_reviews,difficulty,duration,skills,prereqs,cost_type\n")
c.write(cd.read())
c.write(ed.read())
c.write(ud.read())

cd.seek(0)
ed.seek(0)
ud.seek(0)

f.write(cd.read())
f.write(ed.read())
f.write(ud.read())

total = int(cs.read())
total = total + int(es.read())
total = total + int(us.read())
s.write(str(total))


f.close()
c.close()
s.close()
cd.close()
cs.close()
ed.close()
es.close()
ud.close()
us.close()