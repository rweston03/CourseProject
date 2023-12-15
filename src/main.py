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
    # ****************************************************
    # If you put your chromedriver.exe file somewhere other
    # than the path below, update the path before running
    # this program.
    # ****************************************************
    PATH = "C:\Program Files (x86)\chromedriver.exe"

    # Initialize Chrome options
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

    # Initialize Selenium driver
    driver = webdriver.Chrome(PATH, options=chrome_options)

    # Initialize dataset directories
    projectDirectory = os.getcwd()
    projectDirectory.replace("\\", "\\\\")
    currentDirectory = projectDirectory + "\\src\\mooc_datasets"

    courseraDirectory = projectDirectory + "\\src\\coursera\\datasets"
    edxDirectory = projectDirectory + "\\src\\edx\\datasets"
    udacityDirectory = projectDirectory + "\\src\\udacity\\datasets"
    futurelearnDirectory = projectDirectory + "\\src\\futurelearn\\datasets"

    # Initialize variables for commandline arguments
    choice = ""
    pageNum = 0

    # Set pageNum variable based on second commandline argument
    if(len(sys.argv) == 3):
        pageNum = int(sys.argv[2]) if sys.argv[2].isnumeric() else 2

    # Set directories and sub-scrape values based on first commandline argument
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
        elif(choice == "futurelearn"):
            if(pageNum > 0):
                futurelearnDirectory = futurelearnDirectory + "\\limited"
            futurelearn_scraper(driver, futurelearnDirectory, pageNum)
        elif(choice == "all"):
            if(pageNum > 0):
                udacityDirectory = udacityDirectory + "\\limited"
                edxDirectory = edxDirectory + "\\limited"
                courseraDirectory = courseraDirectory + "\\limited"
                futurelearnDirectory = futurelearnDirectory + "\\limited"
            udacity_scraper(driver, udacityDirectory, pageNum)
            edx_scraper(driver, edxDirectory, pageNum)
            coursera_scraper(driver, courseraDirectory, pageNum)
            futurelearn_scraper(driver, futurelearnDirectory, pageNum)
    # If no command line arguments are entered, run all scrapers in default directories
    else:
        choice = "all"
        udacity_scraper(driver, udacityDirectory, pageNum)
        edx_scraper(driver, edxDirectory, pageNum)
        coursera_scraper(driver, courseraDirectory, pageNum)
        futurelearn_scraper(driver, futurelearnDirectory, pageNum)

    # Open existing files to handle main mooc dataset concatenation
    courseraDATFP = os.path.join(courseraDirectory, 'coursera.dat')
    courseraCSVFP = os.path.join(courseraDirectory, 'coursera.csv')
    courseraSTATFP = os.path.join(courseraDirectory, 'stats.txt')
    cv = open(courseraCSVFP, 'r', encoding="utf-8")
    cd = open(courseraDATFP, 'r', encoding="utf-8")
    cs = open(courseraSTATFP, 'r', encoding="utf-8")

    edxDATFP = os.path.join(edxDirectory, 'edx.dat')
    edxCSVFP = os.path.join(edxDirectory, 'edx.csv')
    edxSTATFP = os.path.join(edxDirectory, 'stats.txt')
    ev = open(edxCSVFP, 'r', encoding="utf-8")
    ed = open(edxDATFP, 'r', encoding="utf-8")
    es = open(edxSTATFP, 'r', encoding="utf-8")

    udacityDATFP = os.path.join(udacityDirectory, 'udacity.dat')
    udacityCSVFP = os.path.join(udacityDirectory, 'udacity.csv')
    udacitySTATFP = os.path.join(udacityDirectory, 'stats.txt')
    uv = open(udacityCSVFP, 'r', encoding="utf-8")
    ud = open(udacityDATFP, 'r', encoding="utf-8")
    us = open(udacitySTATFP, 'r', encoding="utf-8")

    futurelearnDATFP = os.path.join(futurelearnDirectory, 'futurelearn.dat')
    futurelearnCSVFP = os.path.join(futurelearnDirectory, 'futurelearn.csv')
    futurelearnSTATFP = os.path.join(futurelearnDirectory, 'stats.txt')
    fv = open(futurelearnCSVFP, 'r', encoding="utf-8")
    fd = open(futurelearnDATFP, 'r', encoding="utf-8")
    fs = open(futurelearnSTATFP.replace("\\\\", "\\"), 'r')

    # Clear out existing mooc datasets before replacing them with new files
    if(pageNum > 0):
        currentDirectory = currentDirectory + "\\limited"

    if os.path.exists(currentDirectory + "\\mooc.dat"):
        os.remove(currentDirectory + "\\mooc.dat")
    if os.path.exists(currentDirectory + "\\mooc.csv"):
        os.remove(currentDirectory + "\\mooc.csv")
    if os.path.exists(currentDirectory + "\stats.txt"):
        os.remove(currentDirectory + "\stats.txt")

    filepathCSV = os.path.join(currentDirectory, 'mooc.csv')
    c = open(filepathCSV, "a+", encoding="utf-8")
    filepathDAT = os.path.join(currentDirectory, 'mooc.dat')
    f = open(filepathDAT, "a+", encoding="utf-8")
    filepathSTATS = os.path.join(currentDirectory, 'stats.txt')
    s = open(filepathSTATS, "a+", encoding="utf-8")

    # Write header line to mooc csv file
    c.write("id,platform,institution,title,url,class_type,description,rating,rating_max,num_reviews,difficulty,duration,skills,prereqs,cost_type\n")
    total = 0 
    if os.path.exists(courseraDATFP) and (choice == "all" or choice == "coursera"):
        lines = cv.read().splitlines(True)[1:]
        c.writelines(lines)
        cd.seek(0)
        f.write(cd.read())
        if os.path.exists(courseraSTATFP):
            csTotal = cs.read()
            if(csTotal.isnumeric()):
                total = total + int(csTotal)
            cs.close()
        cd.close()
    if os.path.exists(edxDATFP) and (choice == "all" or choice == "edx"):
        lines = ev.read().splitlines(True)[1:]
        c.writelines(lines)
        ed.seek(0)
        f.write(ed.read())
        if os.path.exists(edxSTATFP):
            esTotal = es.read()
            if(esTotal.isnumeric()):
                total = total + int(esTotal)
            es.close()
        ed.close()
    if os.path.exists(udacityDATFP) and (choice == "all" or choice == "udacity"):
        lines = uv.read().splitlines(True)[1:]
        c.writelines(lines)
        ud.seek(0)
        f.write(ud.read())
        if os.path.exists(udacitySTATFP):
            usTotal = us.read()
            if(usTotal.isnumeric()):
                total = total + int(usTotal)
            us.close()
        ud.close()
    if os.path.exists(futurelearnDATFP) and (choice == "all" or choice == "futurelearn"):
        lines = fv.read().splitlines(True)[1:]
        c.writelines(lines)
        fd.seek(0)
        f.write(fd.read())
        if os.path.exists(futurelearnSTATFP):
            fsTotal = fs.read()
            if(fsTotal.isnumeric()):
                total = total + int(fsTotal)
            fs.close()
        fd.close()

    s.write(str(total))

    f.close()
    c.close()
    s.close()

    print("Scraping complete")