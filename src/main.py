from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from udacity.scraper import udacity_scraper
from futurelearn.scraper import futurelearn_scraper
from edx.scraper import edx_scraper
from coursera.scraper import coursera_scraper
import os
import sys

if __name__ == '__main__':
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

    projectDirectory = os.getcwd()
    projectDirectory.replace("\\", "\\\\")
    currentDirectory = projectDirectory + "\\src\\mooc_datasets"

    courseraDirectory = projectDirectory + "\\src\\coursera\\datasets"
    edxDirectory = projectDirectory + "\\src\\edx\\datasets"
    udacityDirectory = projectDirectory + "\\src\\udacity\\datasets"

    choice = ""
    pageNum = 0

    if(len(sys.argv) == 3):
        pageNum = int(sys.argv[2]) if sys.argv[2].isnumeric() else 2

    if (len(sys.argv) >= 2):
        choice = sys.argv[1]
        if(choice == "udacity"):
            if(pageNum > 0):
                udacityDirectory = udacityDirectory + "\\limited"
            udacity_scraper(driver, udacityDirectory, pageNum)
        elif(choice == "edx"):
            if(pageNum > 0):
                edxDirectory = edxDirectory + "\\limited"
            edx_scraper(driver, edxDirectory, pageNum)
        elif(choice == "coursera"):
            if(pageNum > 0):
                courseraDirectory = courseraDirectory + "\\limited"
            coursera_scraper(driver, courseraDirectory, pageNum)
        elif(choice == "all"):
            if(pageNum > 0):
                udacityDirectory = udacityDirectory + "\\limited"
                edxDirectory = edxDirectory + "\\limited"
                courseraDirectory = courseraDirectory + "\\limited"
            udacity_scraper(driver, udacityDirectory, pageNum)
            edx_scraper(driver, edxDirectory, pageNum)
            coursera_scraper(driver, courseraDirectory, pageNum)
    else:
        choice = "all"
        udacity_scraper(driver, udacityDirectory, pageNum)
        edx_scraper(driver, edxDirectory, pageNum)
        coursera_scraper(driver, courseraDirectory, pageNum)

    courseraDATFP = os.path.join(courseraDirectory, 'coursera.dat')
    courseraCSVFP = os.path.join(courseraDirectory, 'coursera.csv')
    courseraSTATFP = os.path.join(courseraDirectory, 'stats.txt')
    cv = open(courseraCSVFP, 'r')
    cd = open(courseraDATFP, 'r')
    cs = open(courseraSTATFP, 'r')

    edxDATFP = os.path.join(edxDirectory, 'edx.dat')
    edxCSVFP = os.path.join(edxDirectory, 'edx.csv')
    edxSTATFP = os.path.join(edxDirectory, 'stats.txt')
    ev = open(edxCSVFP, 'r')
    ed = open(edxDATFP, 'r')
    es = open(edxSTATFP, 'r')

    udacityDATFP = os.path.join(udacityDirectory, 'udacity.dat')
    udacityCSVFP = os.path.join(udacityDirectory, 'udacity.csv')
    udacitySTATFP = os.path.join(udacityDirectory, 'stats.txt')
    uv = open(udacityCSVFP, 'r')
    ud = open(udacityDATFP, 'r')
    us = open(udacitySTATFP, 'r')

    if(pageNum > 0):
        currentDirectory = currentDirectory + "\\limited"

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
    total = 0
    if os.path.exists(courseraDATFP) and (choice == "all" or choice == "coursera"):
        #c.write(str(cv.read().splitlines(True)[1:]))
        lines = cv.read().splitlines(True)[1:]
        c.writelines(lines)
        cd.seek(0)
        f.write(cd.read())
        if os.path.exists(courseraSTATFP):
            total = total + int(cs.read())
            cs.close()
        cd.close()
    if os.path.exists(edxDATFP) and (choice == "all" or choice == "edx"):
        #c.write(ev.read().splitlines(True)[1:])
        lines = ev.read().splitlines(True)[1:]
        c.writelines(lines)
        ed.seek(0)
        f.write(ed.read())
        if os.path.exists(edxSTATFP):
            total = total + int(es.read())
            es.close()
        ed.close()
    if os.path.exists(udacityDATFP) and (choice == "all" or choice == "udacity"):
        #c.write(uv.read().splitlines(True)[1:])
        lines = uv.read().splitlines(True)[1:]
        c.writelines(lines)
        ud.seek(0)
        f.write(ud.read())
        if os.path.exists(courseraSTATFP):
            total = total + int(us.read())
            us.close()
        ud.close()

    s.write(str(total))

    f.close()
    c.close()
    s.close()