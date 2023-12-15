from model.moocClass import moocClass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# FutureLearn catalog URL: https://www.futurelearn.com/courses?filter_category=open&filter_course_type=open&filter_availability=open
# Pages after first: https://www.futurelearn.com/courses?filter_category=open&filter_course_type=open&filter_availability=open&page=2
# FutureLearn pagination: nav > ul.pagination-module_wrapper__mZtrv[7th child].pagination-module_item__3XB-1 text content

# For FutureLearn, each course in the catalog is in a div with the classes "m-card Container-wrapper_7nJ95".
# The first child of the course div is a link with the class "link-wrapper_djqc+" and the URL for the course is the href.
# The institution, course title, rating, number of reviews, duration, and cost are located in the second child in a nested div/a/div 
# (div.Body-wrapper_0gskP > a.link-wrapper_djqc+ > div.Content-wrapper_k+G32).
# The institution name is in a nested div/span child (div.label-wrapper_jRU3o > span.text-module_wrapper__FfvIV).
# The course title is in a nested div/h3 child (div.Title-wrapper_5eSVQ > h3.heading-module_wrapper__2dcxt).
# The rating is in a div with the classes "ReviewStars-text_ABUtn ReviewStars-staticText_EieAn".
# The number of reviews is in a child span of the rating div.
# Both the duration and the course cost are in nested divs 'div.Options-wrapper_XHGLX div.align-module_wrapper__1Fi9D div.align-module_itemsWrapper__utBam'.
# There are three children in this options wrapper div that have the class 'align-module_item__oiojU', the first is duration and the third is course cost.
# Path to duration from options wrapper utBam first child: 'div.align-module_wrapper__1Fi9D > div.align-module_itemsWrapper__utBam[last-child].align-module_item__oioJU > 
# p.text-module_wrapper__FfvIV'
# Path to course cost from options wrapper utBam first child: 'div.stack-module_wrapper__3ZERF > div.stack-module_item__1UYFV > div.align-module_wrapper__1Fi9D > 
# div.align-module_itemsWrapper__utBam[last-child].align-module_item__oiojU p.text-module_wrapper__FfvIV'

# On the details page, the difficulty level is in a nested div/ul/li/div/p (div.PageHeader-widgetWrapper_crisD > div > 
# div.InformationWidget-widgetWrapper_6ZMLn[4th child].InformationWidget-section_9ypWv > 
# ul.list-module_list__3LUv7[last-child].listItemWithIcon-module_wrapper__q21aj[last-child].listItemWithIcon-module_text__18TIF p.text-module_wrapper__FfvIV)
# The course description is spread across several paragraphs and will need to be concatenated into a single string.
# The course description is in a series of four nested divs (div#section-overview > div.index-module_wrapper__2aztW div.spacer-module_default__3N2H9 div p)
# FutureLearn doesn't list skills or prerequisites, but there are a couple sections listing "What will you achieve?" and "Who is this course for?" and the information for 
# these properties will have to be pulled from these items. 
# The prereqs section ("Who is this course for?") fortunately has an id and can be found in a section/div/div/p (section#section-requirements > div.index-module_wrapper__2aztW >
# div > p).
# The skills section ("What will you achieve?") unfortunately does not have an id or distinguishing class, so I'll need to look for a p tag with the inner text "By the end of the
# course, you'll be able to..." and then look for it's first sibling. (Find all p tags, then iterate through them looking for the p tag whose textContent is "By the end of the course").
# The first sibling will be a ul. I'll then have to collect the last-child of every li under the ul and concatenate them into a single string for the skills.

def futurelearn_scraper(driver, currentDirectory, pageNum):
    print("Scrape futurelearn")

    #Initialize variables
    currCourseArray = []
    courseNum = 0
    totalCourses = 0

    # Clear out existing files if they exist and prepare new files for writing
    if os.path.exists(currentDirectory + "\\futurelearn.dat"):
        os.remove(currentDirectory + "\\futurelearn.dat")
    if os.path.exists(currentDirectory + "\\futurelearn.csv"):
        os.remove(currentDirectory + "\\futurelearn.csv")
    if os.path.exists(currentDirectory + "\stats.txt"):
        os.remove(currentDirectory + "\stats.txt")
    if os.path.exists(currentDirectory + "\errors.txt"):
        os.remove(currentDirectory + "\errors.txt")
    filepathCSV = os.path.join(currentDirectory, 'futurelearn.csv')
    c = open(filepathCSV, "a", encoding="utf-8")
    filepathDAT = os.path.join(currentDirectory, 'futurelearn.dat')
    f = open(filepathDAT, "a", encoding="utf-8")
    filepathERR = os.path.join(currentDirectory, 'errors.txt')
    e = open(filepathERR, "a", encoding="utf-8")
    filepathSTATS = os.path.join(currentDirectory, 'stats.txt')
    c.write("id,platform,institution,title,url,class_type,description,rating,rating_max,num_reviews,difficulty,duration,skills,prereqs,cost_type\n")
    
    # Fetch the first course page
    driver.get("https://www.futurelearn.com/courses?filter_category=open&filter_course_type=open&filter_availability=open")
    
    # Add sleep setting to allow page to fully load
    time.sleep(3)
    try:
        # Get total number of course catalog pages
        paginationWrapper = driver.find_elements(By.CSS_SELECTOR, "li.pagination-module_item__k7cxD > a")
        pagination = paginationWrapper[len(paginationWrapper) - 1]
        pageCount = int(pagination.text)
        main = WebDriverWait(driver, timeout=100).until(lambda d: d.find_element(By.ID, "main-content"))
        pageCount = pagination.text
        pageCount = pageCount.split(" ")
        pageCount = pageCount[len(pageCount) - 1]
        pageCount = int(pageCount)

        # Set current page to 1
        currentPage = 1

        # If a desired number of pages has been passed in, use it if it is under the total number of course catalog pages
        # Otherwise, use the total
        if(pageNum != 0 and pageNum <= pageCount):
            pageCount = pageNum

        # Scrape course catalog pages until the last page is reached
        while(currentPage <= pageCount):
            try:
                # Get the current course catalog page
                if(int(currentPage) == 1):
                    pageUrl = "https://www.futurelearn.com/courses?filter_category=open&filter_course_type=open&filter_availability=open"
                else:
                    pageUrl = "https://www.futurelearn.com/courses?filter_category=open&filter_course_type=open&filter_availability=open&page=" + str(currentPage)
                driver.get(pageUrl)
                # Wait for it to load
                time.sleep(5)
                try:
                    # Wait for main element and courses to be displayed
                    main = WebDriverWait(driver, timeout=100).until(lambda d: d.find_element(By.ID, "main-content"))
                    courses = WebDriverWait(driver, timeout=10000).until(lambda d: d.find_elements(By.CSS_SELECTOR, "div.m-filter__content div.m-card.Container-wrapper_7nJ95"))
                except:
                    # If the necessary elements aren't displayed, get the page again and wait a little longer for the elements to be displayed
                    if(int(currentPage) == 1):
                        pageUrl = "https://www.futurelearn.com/courses?filter_category=open&filter_course_type=open&filter_availability=open"
                    else:
                        pageUrl = "https://www.futurelearn.com/courses?filter_category=open&filter_course_type=open&filter_availability=open&page=" + str(currentPage)
                    driver.get(pageUrl)
                    time.sleep(10)
                    main = WebDriverWait(driver, timeout=100).until(lambda d: d.find_element(By.ID, "main-content"))
                    courses = WebDriverWait(driver, timeout=10000).until(lambda d: d.find_elements(By.CSS_SELECTOR, "div.m-filter__content div.m-card.Container-wrapper_7nJ95"))
                
                # Iterate through the courses on the course catalog page and scrape the available information for each course
                for course in courses:
                    url = course.find_element(By.CSS_SELECTOR, "div.Body-wrapper_0gskP > a") 
                    currUrl = str(url.get_attribute('href'))

                    # Check to make sure that the course element in the course catalog points to a course detail page instead of an advertisement or some other page
                    if(currUrl.startswith("https://www.futurelearn.com/courses/")):
                        courseNum = courseNum + 1
                        title = course.find_element(By.CSS_SELECTOR, "div.Body-wrapper_0gskP > a > div > div.Title-wrapper_5eSVQ > h3")
                        title = str(title.get_attribute('innerHTML')).replace(",", "").replace("\n","").strip()
                        try:
                            institution = course.find_element(By.CSS_SELECTOR, "div.Body-wrapper_0gskP > a > div > div.label-wrapper_jRU3o > span")
                            if(institution):
                                institution = str(institution.get_attribute('innerHTML')).replace(",", "").replace("\n","").strip()
                        except:
                            institution = "FutureLearn"
                        try:
                            rating = course.find_element(By.CSS_SELECTOR, "div.Body-wrapper_0gskP > a > div > div.spacer-module_default__LTC4S div.ReviewStars-text_ABUtn")
                            if(rating):
                                ratingString = str(rating.get_attribute('innerHTML')).replace("<span>(<!-- -->", "").replace("<!-- -->", "").replace(")</span>", "")
                                ratingString = ratingString.split(" ")
                                rating = ratingString[0]
                                rating_max = 5
                                num_reviews = ratingString[1]
                        except:
                            rating = "None"
                            rating_max = "None"
                            num_reviews = "None"  
                        try:
                            subDivs = course.find_elements(By.CSS_SELECTOR, "div.Body-wrapper_0gskP > a > div > div.Options-wrapper_XHGLX > div.align-module_wrapper__RpD0z > div.align-module_itemsWrapper__VqrgE > div.align-module_item__YwH46")
                            if(subDivs):
                                durationDiv = subDivs[0]
                                duration = durationDiv.find_element(By.CSS_SELECTOR, "p.text-module_wrapper__Dg6SG.text-module_coolGrey__azvPI")
                                duration = duration.text
                                costDiv = subDivs[2]
                                cost = costDiv.find_element(By.CSS_SELECTOR, "p.text-module_wrapper__Dg6SG.text-module_coolGrey__azvPI")
                                cost = "Free" if "Free" in cost.text else "Paid"
                        except:
                            duration = "None"
                            cost = "Paid"
                        id = "FutureLearn" + "-" + str(courseNum)
                        mooc = moocClass(id, "FutureLearn", institution, title, url.get_attribute('href'), "Course", "None", rating, rating_max, num_reviews, "None", duration, "None", "None", cost)
                        currCourseArray.append(mooc)

                # After scraping the course catalog page, iterate through the courses found and scrape their detail pages
                for course in currCourseArray:
                    driver.get(course.url)
                    liveUrl = driver.current_url
                    time.sleep(3)
                    if(liveUrl == course.url):
                        main = WebDriverWait(driver, timeout=100).until(lambda d: d.find_element(By.ID, "main-content"))

                        try:
                            description = main.find_element(By.CSS_SELECTOR, "#section-page-header div.PageHeader-introduction_vthti > p")
                            if(description):
                                course.description = description.text.replace(",", "").replace("\n","").strip()
                        except:
                            try:
                                descriptionDivs = main.find_elements(By.CSS_SELECTOR, "#section-page-header > div.PageHeader-contentWrapper_zNpvN > div.PageHeader-content_iKK59 > div.stack-module_wrapper__aPV9V > div.stack-module_item__6l6uZ")
                                if(descriptionDivs):
                                    descriptionDivs = descriptionDivs[2]
                                    description = descriptionDivs.find_element(By.CSS_SELECTOR, "p.text-module_wrapper__Dg6SG")
                                    course.description = description.text.replace(",", "").replace("\n","").strip()
                            except:
                                course.description = "None"
                        try:
                            difficultyDivs = main.find_elements(By.CSS_SELECTOR, ".PageHeader-widgetWrapper_crisD > div > div.InformationWidget-widgetWrapper_6ZMLn > div.InformationWidget-section_9ypWv")
                            if(difficultyDivs):
                                difficultyDivs = difficultyDivs[2]
                                difficultyLists = difficultyDivs.find_elements(By.CSS_SELECTOR, "ul.list-module_list__GCpaz > li.listItemWithIcon-module_wrapper__3rRoW")
                                difficultyLists = difficultyLists[len(difficultyLists) - 1]
                                difficulty = difficultyLists.find_element(By.CSS_SELECTOR, "div.listItemWithIcon-module_text__TyyZd > p.text-module_wrapper__Dg6SG")
                                difficulty = difficulty.text
                                difficulty = difficulty.split(" ")[0].strip()
                                course.difficulty = difficulty if difficulty != "Open" else "None"
                        except:
                            course.difficulty = "None"
                        
                        try:
                            skillsParagraph = driver.find_element(By.XPATH, "//p[contains(text(),'By the end of the course, you‘ll be able to...')]")
                            if(skillsParagraph):
                                skillsDiv = skillsParagraph.find_element(By.XPATH, "./..")
                                skillsList = skillsDiv.find_elements(By.CSS_SELECTOR, "ul.Grid-module_grid__c8F99 > li.listItemWithIcon-module_wrapper__3rRoW > div.listItemWithIcon-module_text__TyyZd")
                                skills = ""
                                for idx, s in enumerate(skillsList):
                                    s = s.get_attribute('innerHTML')
                                    s = s.replace(",", "").replace("\n","").strip()
                                    skills = skills + s
                                    if(idx != len(skillsList) - 1):
                                        skills = skills + " - "
                                course.skills = skills
                        except:
                            course.skills = "None"
                        
                        try:
                            prereqsParagraph = driver.find_element(By.XPATH, "//h2[contains(text(),'Who is the course for?')]")
                            if(prereqsParagraph):
                                prereqsDiv = prereqsParagraph.find_element(By.XPATH, "./..")
                                prereqs = prereqsDiv.find_element(By.CSS_SELECTOR, "div > p")
                                prereqs = prereqs.text.replace(",", "").replace("\n","").strip()
                                course.prereqs = prereqs

                        except:
                            course.prereqs = "None"   

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
                print("Error parsing FutureLearn url: " + pageUrl)

        c.close()
        e.close()
        f.close()
 
        # Write the total number of courses scraped to the stats file
        s = open(filepathSTATS, "a")
        s.write(str(totalCourses))
        s.close()

    except:
        print("Error in FutureLearn scraper")