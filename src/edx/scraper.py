from model.moocClass import moocClass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Edx catalog URL: https://www.edx.org/search?learning_type=Course&tab=course
# Pages after first: https://www.edx.org/search?learning_type=Course&tab=course&page=2
# Edx pagination: nav.pagination-secondary.pagination-small > ul.pagination[6th child].page-item > button[aria label or text content]

def edx_scraper(driver, currentDirectory, pageNum):
    # learningTypes = ["Bachelors", "Boot+Camp", "Certificate", "Course", "Doctorate", "Executive+Education", "License", "Masters", "MicroBachelors", "MicroMasters", "Professional+Certificate", "XSeries"]
    # tabs = ["course", "program", "degree-program", "boot-camp", "executive-education"]

    # Edx has an oddly designed website. I was originally going to do each learning type available (i.e. "Bachelors", "Boot+Camp", "Certificate", "Course", 
    # "Doctorate", "Executive+Education", etc.), however, there isn't a lot of consistency between urls for programs (i.e. bachelors, masters, etc) and regular courses. For instance, 
    # regular course urls start with "https://www.edx.org/learn/" but microbachelors urls start with "https://www.edx.org/bachelors/microbachelors/"
    # and a license url I found links to an outside website "https://educationonline.udayton.edu/principal-licensure-preparation-program". So, I'm going to limit my scraping on Edx to
    # courses only.

    print("Scrape edx")

    #Initialize variables
    currCourseArray = []
    courseNum = 0
    totalCourses = 0

    # Clear out existing files if they exist and prepare new files for writing
    if os.path.exists(currentDirectory + "\edx.dat"):
        os.remove(currentDirectory + "\edx.dat")
    if os.path.exists(currentDirectory + "\edx.csv"):
        os.remove(currentDirectory + "\edx.csv")
    if os.path.exists(currentDirectory + "\stats.txt"):
        os.remove(currentDirectory + "\stats.txt")
    if os.path.exists(currentDirectory + "\errors.txt"):
        os.remove(currentDirectory + "\errors.txt")
    filepathCSV = os.path.join(currentDirectory, 'edx.csv')
    c = open(filepathCSV, "a", encoding="utf-8")
    filepathDAT = os.path.join(currentDirectory, 'edx.dat')
    f = open(filepathDAT, "a", encoding="utf-8")
    filepathERR = os.path.join(currentDirectory, 'errors.txt')
    e = open(filepathERR, "a", encoding="utf-8")
    filepathSTATS = os.path.join(currentDirectory, 'stats.txt')
    c.write("id,platform,institution,title,url,class_type,description,rating,rating_max,num_reviews,difficulty,duration,skills,prereqs,cost_type\n")

    # Fetch the first course page
    driver.get("https://www.edx.org/search?tab=course&learning_type=Course")

    # Add sleep setting to allow page to fully load
    time.sleep(3)

    try:
        # Get total number of course catalog pages and set current page to 1
        main = driver.find_element(By.ID, "main-content")
        wait = WebDriverWait(driver, timeout=20)
        wait.until(lambda d : main.is_displayed())

        pagination = WebDriverWait(driver, timeout=10000).until(lambda d : d.find_element(By.CSS_SELECTOR, "ul.pagination"))

        currentPage = 1

        pages = driver.find_elements(By.XPATH, "//button[starts-with(@aria-label, 'Page ')]")
        wait = WebDriverWait(driver, timeout=2000)
        wait.until(lambda d : len(pages) >= 1)

        idx = len(pages)
        idx = int((idx/2) - 1)
        pageCount = pages[idx]
        pageCount = pageCount.get_attribute('innerHTML')
        pageCount = int(pageCount)

        # If a desired number of pages has been passed in, use it if it is under the total number of course catalog pages
        # Otherwise, use the total
        if(pageNum != 0 and pageNum <= pageCount):
            pageCount = pageNum

        # Scrape course catalog pages until the last page is reached
        while(int(currentPage) <= pageCount):
            try:
                # Get the current course catalog page
                if(int(currentPage) == 1):
                    pageUrl = "https://www.edx.org/search?tab=course&learning_type=Course"
                else:
                    pageUrl = "https://www.edx.org/search?learning_type=Course&tab=course&page=" + str(currentPage)
                driver.get(pageUrl)
                # Wait for it to load
                time.sleep(5)
                try:
                    # Wait for pagination, main element, and courses to be displayed
                    main = driver.find_element(By.ID, "main-content")
                    wait = WebDriverWait(driver, timeout=20)
                    wait.until(lambda d : main.is_displayed())

                    courses = main.find_elements(By.CSS_SELECTOR, "div.card-container div.base-card-wrapper") 
                except:
                    # If the necessary elements aren't displayed, get the page again and wait a little longer for the elements to be displayed
                    if(int(currentPage) == 1):
                        pageUrl = "https://www.edx.org/search?tab=course&learning_type=Course"
                    else:
                        pageUrl = "https://www.edx.org/search?learning_type=Course&tab=course&page=" + str(currentPage)
                    driver.get(pageUrl)
                    time.sleep(10)
                    main = driver.find_element(By.ID, "main-content")
                    wait = WebDriverWait(driver, timeout=20)
                    wait.until(lambda d : main.is_displayed())

                    courses = main.find_elements(By.CSS_SELECTOR, "div.card-container div.base-card-wrapper") 

                # Iterate through the courses on the course catalog page and scrape the available information for each course
                for course in courses:
                    url = course.find_element(By.CLASS_NAME, "base-card-link") 
                    currUrl = str(url.get_attribute('href'))

                    # Check to make sure that the course element in the course catalog points to a course detail page instead of an advertisement or some other page
                    if(currUrl.startswith("https://www.edx.org/learn/")):
                        courseNum = courseNum + 1
                        title = ""
                        titleSpans = course.find_elements(By.CSS_SELECTOR, "div.pgn__card-header-content > div.pgn__card-header-title-md > span > span > span")
                        for idx, span in enumerate(titleSpans):
                            title += span.text.replace(",", "").replace("\n","")
                            if(idx != len(titleSpans) - 1):
                                title += " "
                        try:
                            institution = course.find_element(By.CSS_SELECTOR, "div.pgn__card-header-content > div.pgn__card-header-subtitle-md > span > span > span")
                            institution = institution.text.replace(",", "").replace("\n","")
                        except:
                            institution = "None"
                        try:
                            classType = course.find_element(By.CSS_SELECTOR, "div.pgn__card-section > div > span.badge")
                            classType = classType.get_attribute("innerHTML")
                        except:
                            classType = "Course"
                        id = "Edx" + "-" + str(courseNum)
                        mooc = moocClass(id, "Edx", institution, title, url.get_attribute('href'), classType, "None", "None", "None", "None", "None", "None", "None", "None", "Paid")
                        currCourseArray.append(mooc)
                
                # After scraping the course catalog page, iterate through the courses found and scrape their detail pages
                for course in currCourseArray:
                    if(str(course.url).startswith("https://www.edx.org/learn/")):
                        driver.get(course.url)
                        liveUrl = driver.current_url
                        time.sleep(3)
                        if(liveUrl == course.url):
                            main = driver.find_element(By.ID, "main-content")
                            wait = WebDriverWait(driver, timeout=10)
                            wait.until(lambda d : main.is_displayed())
                            header = WebDriverWait(driver, timeout=10).until(lambda d : d.find_element(By.CSS_SELECTOR, "div.col-md-7.pr-4 > h1"))
                            try:
                                rating = driver.find_element(By.CSS_SELECTOR, "div.course-header > div.position-relative.container-mw-lg.container-fluid > div.row.no-gutters > div.col-md-7.pr-4 > div.d-flex.align-items-center > div.h5.ml-1.mr-3.mb-0")
                                if(rating):
                                    rating = rating.get_attribute("innerHTML")
                                    course.rating = rating.split(" ")[0].replace("<!--", "")
                                course.rating_max = "5"
                            except:
                                course.rating = "None"
                                course.rating_max = "None"
                            try:
                                description = driver.find_element(By.CSS_SELECTOR, "div.course-header > div.position-relative.container-mw-lg.container-fluid > div.row.no-gutters > div.col-md-7.pr-4 > div.p > p")
                                if(description):
                                    course.description = description.text.replace(",", "").replace("\n","")
                            except:
                                course.description = "None"

                            try:
                                num_reviews = driver.find_element(By.CSS_SELECTOR, "div.course-header > div.position-relative.container-mw-lg.container-fluid > div.row.no-gutters > div.col-md-7.pr-4 > div.d-flex.align-items-center > div.micro")
                                if(num_reviews):
                                    num_reviews = num_reviews.get_attribute("innerHTML")
                                    course.num_reviews = num_reviews.split(" ")[0].replace("<!--", "")
                            except:
                                course.num_reviews = "None"

                            
                            try:
                                duration = driver.find_element(By.CSS_SELECTOR, "div.course-snapshot-content.py-2.text-primary-500 > div.row.pl-1.pl-sm-0.my-1 > div.d-flex.align-items-start.col-12.pb-4.pb-md-0.col-md-4 > div.ml-3 > div.h4.mb-0")
                                if(duration):
                                    course.duration = duration.get_attribute("innerHTML")
                            except:
                                course.duration = "None"
                            try:
                                costType = driver.find_element(By.CSS_SELECTOR, "div.course-snapshot-content.py-2.text-primary-500 > div.row.pl-1.pl-sm-0.my-1 > div.d-flex.align-items-start.col-12.pt-4.pt-md-0.col-md-4 > div.ml-3 > div.h4.mb-0")
                                if(costType):
                                    course.cost_type = costType.get_attribute("innerHTML")
                            except:
                                course.cost_type = "Paid"
                            

                            try:
                                difficultySpan = driver.find_element(By.XPATH, "//span[contains(text(),'Level: ')]")
                                difficulty = difficultySpan.find_element_by_xpath('..')
                                if(difficulty):
                                    difficulty = difficulty.get_attribute("innerHTML").split(" ")
                                    course.difficulty = difficulty[len(difficulty) - 1].replace("-->", "")
                            except:
                                course.difficulty = "Introductory"

                            try:
                                prereqsSpan = driver.find_element(By.XPATH, "//span[contains(text(),'Prerequisites: ')]")
                                prereqs = prereqsSpan.find_element_by_xpath('..')
                                if(prereqs):
                                    prereqs = prereqs.get_attribute("innerHTML").split(" ")
                                    course.prereqs = prereqs.replace('<span class="font-weight-bold">Prerequisites: </span> ', "").replace("<div>", "").replace("</div>", "").replace("<p>", "").replace("</p>", "").replace(", ", " - ").replace("\n","")
                            except:
                                course.prereqs = "None"
                            
                            try:
                                skillsSpan = driver.find_element(By.XPATH, "//span[contains(text(),'Associated skills: ')]")
                                skills = skillsSpan.find_element_by_xpath('..')
                                if(skills):
                                    skills = skills.get_attribute("innerHTML")
                                    course.skills = skills.replace('<span class="font-weight-bold">Associated skills: ', "").replace("<span>", "").replace("</span>", "").replace(", ", " - ").replace("\n","")
                            except:
                                course.skills = "None"

                # After scraping the current round of courses on the course catalog page, write the courses to the csv and dat files
                # Write any errors to the error file
                # Add the currCourseArray length to the totalCourses count for the stat file            
                for course in currCourseArray:
                    try:
                        c.write(course.toFileString().lower())
                    except:
                        print("Could not write " + course.title + " to csv file.")
                        e.write("Could not write course to csv: " + course.url + "\n")
                    try:
                        f.write(course.toFileString().lower())
                    except:
                        print("Could not write " + course.title + " to dat file.")
                        e.write("Could not write course to dat: " + course.url + "\n")
                # Add the currCourseArray length to the totalCourses count for the stat file
                totalCourses = totalCourses + len(currCourseArray)
                # Clear out the currCourseArray in preparation for the next detail page
                currCourseArray = []
                # Advance the scraper to the next page
                currentPage = currentPage + 1
            except:
                print("Error parsing Edx url: " + pageUrl)

        c.close()
        e.close()
        f.close()
 
        # Write the total number of courses scraped to the stats file
        s = open(filepathSTATS, "w")
        s.write(str(totalCourses))
        s.close()

    except:
        print("Error in Edx Scraper")