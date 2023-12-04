from model.moocClass import moocClass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Udacity catalog URL: https://www.udacity.com/catalog/all/any-price/any-school/any-skill/any-difficulty/any-duration/any-type/recently-updated/page-1
# Udacity pagination: div#react-select-select-instance-pageSelect-placeholder holds Page x of X, will need to grab as string and parse out last page #

# For Udacity, each course listed in the catalog is in an article element with class 'css-1gj5mr6'.
# The second div child (we'll call this the content div div.css-15q7znr) of each article element contains url (href) for the course in an a tag with class 'css-752atj'.
# The Title of the course is in a nested div child (div.css-c5zt4b > div.css1rsg1aw) of the a tag
# The Rating of the course is in a nested div child (div.css1a1nbps > div.css-171.onha > div.css-nbgxi6[aria-label]) of the content div.
# The Number of Ratings of the course is in a nested p child (div.css1a1nbps > div.css-171.onha > p.css-rxdhdu) of the content div.
# The Duration of the course is in a nested p child (div.css1a1nbps > div.css-k008qs > p.css-1osqk4n) of the content div.
# The Difficulty of the course is in a nested p child (div.css1a1nbps > div.css-k008qs > p.css-5ucqax) of the content div.

# For the detail page of each course, the basic information for the course is in a div with the class 'css-13a007i'
# If the course is free, there will be a span with the classes 'chakra-badge css-voosbm' on the page
# The class type is in a p child with the class 'css-rxdhdu'
# The class description is in a nested div/p child (div.css-ozv6cb > p.css-s4w4a4)
# The skills and prerequisite info for the course is in a div with the class 'css-8ptr35'
# The prerequisites for the course are in a nested figure/div/p child (figure.css-1wk2m2i > div.css-0 > p.css-o3oz8b)
# The skills learned in the course are partially on the page (figure.css-amj7dw > div.css-0) and are fully rendered in a modal
# The modal is activated by clicking a button with classes "chakra-link css-3fo2pp". 
# The skills in the modal are in "div.chakra-modal__body > div.css-fm4r4t > figure.css-1821gv5 p.css-030z8b"
# The modal is closed by clicking on the modal button with the classes "chakra-modal__close-btn css-aek9sk".

def udacity_scraper(driver):
    print("scrape udacity")
    courseArray = []
    currCourseArray = []
    courseNum = 0


    driver.get("https://www.udacity.com/catalog/all/any-price/any-school/any-skill/any-difficulty/any-duration/any-type/recently-updated/page-1")
    time.sleep(3)
    try:
        pagination = driver.find_element(By.ID, "react-select-select-instance-pageSelect-placeholder")
        wait = WebDriverWait(driver, timeout=10)
        wait.until(lambda d : pagination.text != "Page 0 of 0")
        main = driver.find_element(By.CLASS_NAME, "css-mrqgt1")
        pageCount = pagination.text
        pageCount = pageCount.split(" ")
        pageCount = pageCount[len(pageCount) - 1]
        currentPage = 1
        while(int(currentPage) <= int(pageCount)):
            try:
                pageUrl = "https://www.udacity.com/catalog/all/any-price/any-school/any-skill/any-difficulty/any-duration/any-type/recently-updated/page-" + str(currentPage)
                driver.get(pageUrl)
                time.sleep(5)
                pagination = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.ID, "react-select-select-instance-pageSelect-placeholder"))
                main = driver.find_element(By.CLASS_NAME, "css-mrqgt1")

                courses = main.find_elements(By.CLASS_NAME, "css-1gj5mr6")
                for course in courses:
                    url = course.find_element(By.CLASS_NAME, "css-752atj") 
                    currUrl = str(url.get_attribute('href'))
                    if(currUrl.startswith("https://www.udacity.com/course/")):
                        courseNum = courseNum + 1
                        title = course.find_element(By.CSS_SELECTOR, "div.css-15q7znr > a.css-752atj > div.css-c5zt4b > div.chakra-heading.css-1rsglaw")
                        try:
                            rating = course.find_element(By.CLASS_NAME, "css-nbgxi6")
                            if(rating):
                                ratingString = rating.get_attribute('aria-label')
                                ratingString = ratingString.split(" ")
                                rating = ratingString[1]
                                rating_max = ratingString[4]
                                numReviewString = course.find_element(By.CLASS_NAME, "css-rxdhdu")
                                num_reviews = numReviewString.text.replace("(", "")
                                num_reviews = num_reviews.replace(")", "")
                        except:
                            rating = "None"
                            rating_max = "None"
                            num_reviews = "None"  
                        try:
                            duration = course.find_element(By.CLASS_NAME, "css-1osqk4n")
                            if(duration):
                                duration = duration.text
                        except:
                            duration = "None"
                        try:
                            difficulty = course.find_element(By.CLASS_NAME, "css-5ucqax")
                            if(difficulty):
                                difficulty = difficulty.text.replace(",", "")
                        except:
                            difficulty = "None"
                        id = "Udacity" + "-" + str(courseNum)
                        mooc = moocClass(id, "Udacity", "Udacity", title.text, url.get_attribute('href'), "None", "None", rating, rating_max, num_reviews, difficulty, duration, "None", "None", "Paid")
                        currCourseArray.append(mooc)
                
                for course in currCourseArray:
                    driver.get(course.url)
                    main = driver.find_element(By.CLASS_NAME, "css-1bok1n8")
                    enrollButton = main.find_element(By.CLASS_NAME, "css-i5wyu9")
                    wait = WebDriverWait(driver, timeout=10)
                    wait.until(lambda d : enrollButton.text == "Enroll Now")
                    classType = driver.find_element(By.CLASS_NAME, "css-rxdhdu")
                    course.class_type = classType.text
                    try:
                        costTypeString = main.find_element(By.CSS_SELECTOR, "span.chakra-badge.css-voosbm")
                        if(costTypeString):
                            course.cost_type = "Free"
                    except:
                        course.cost_type = "Paid"
                    try:
                        description = main.find_element(By.CSS_SELECTOR, "p.css-s4w4a4")
                        if(description):
                            course.description = description.text.replace(",", "")
                    except:
                        course.description = "None"
                    try:
                        skills = main.find_element(By.CSS_SELECTOR, "figure.css-amj7dw")
                        if(skills):
                            try:
                                skillsButton = skills.find_element(By.CSS_SELECTOR, "button.chakra-link.css-1771ffa")
                                if(skillsButton):
                                    skillsButton.click()
                                    body = driver.find_element(By.CLASS_NAME, "chakra-ui-light")
                                    skillsModal = body.find_element(By.CSS_SELECTOR, "section.chakra-modal__content.css-fjdl7f")
                                    wait = WebDriverWait(driver, timeout=20)
                                    wait.until(lambda d : skillsModal.is_displayed())
                                    if(skillsModal):
                                        skillParagraphs = skillsModal.find_elements(By.CSS_SELECTOR, "p.chakra-text.css-o3oz8b")
                                        if(skillParagraphs):
                                            course.skills = ""
                                            for idx, paragraph in enumerate(skillParagraphs):
                                                paragraphText = paragraph.text.replace(" •", " - ")
                                                course.skills += paragraphText
                                                if(idx < len(skillParagraphs) - 1):
                                                    course.skills += " - "
                                        skillsClose = skillsModal.find_element(By.CSS_SELECTOR, "button.chakra-modal__close-btn.css-aek9sk")
                                        skillsClose.click()
                                                
                            except:
                                try:
                                    skillsText = skills.find_element(By.CSS_SELECTOR, "div.css-0")
                                    if(skillsText):
                                        course.skills = skillsText.text.replace(" •", " - ")
                                except:
                                    course.skills = "None"
                    except:
                        course.skills = "None"
                    
                    try:
                        prereqs = main.find_element(By.CSS_SELECTOR, "figure.css-1wk2m2i")
                        if(prereqs):
                            try:
                                prereqsButton = prereqs.find_element(By.CSS_SELECTOR, "button.chakra-link.css-1771ffa")
                                if(prereqsButton):
                                    prereqsButton.click()
                                    body = driver.find_element(By.CLASS_NAME, "chakra-ui-light")
                                    prereqsModal = body.find_element(By.CSS_SELECTOR, "section.chakra-modal__content.css-fjdl7f")
                                    wait = WebDriverWait(driver, timeout=20)
                                    wait.until(lambda d : prereqsModal.is_displayed())
                                    if(prereqsModal):
                                        prereqList = prereqsModal.find_elements(By.CSS_SELECTOR, "li.css-0")
                                        if(prereqList):
                                            course.prereqs = ""
                                            for idx, listItem in enumerate(prereqList):
                                                course.prereqs += listItem.text
                                                if(idx < len(prereqList) - 1):
                                                    course.prereqs += "- "
                                        prereqsClose = prereqsModal.find_element(By.CSS_SELECTOR, "button.chakra-modal__close-btn.css-aek9sk")
                                        prereqsClose.click()
                                                
                            except:
                                try:
                                    prereqsText = prereqs.find_element(By.CSS_SELECTOR, "div.css-0")
                                    if(prereqsText):
                                        course.prereqs = prereqsText.text.replace(" •", " - ")
                                except:
                                    course.prereqs = "None"
                    except:
                        course.prereqs = "None"          

                courseArray = courseArray + currCourseArray
                currCourseArray = []
                currentPage += 1
            except:
                print("Error parsing Udacity url: " + pageUrl)

        currentDirectory = os.getcwd()
        currentDirectory = currentDirectory + "\\src\\udacity\\datasets"
        currentDirectory.replace("\\", "\\\\")
        if os.path.exists(currentDirectory + "\\udacity.dat"):
            os.remove(currentDirectory + "\\udacity.dat")
        if os.path.exists(currentDirectory + "\\udacity.csv"):
            os.remove(currentDirectory + "\\udacity.csv")
        if os.path.exists(currentDirectory + "\stats.txt"):
            os.remove(currentDirectory + "\stats.txt")
        filepathCSV = os.path.join(currentDirectory, 'udacity.csv')
        c = open(filepathCSV, "a")
        filepathDAT = os.path.join(currentDirectory, 'udacity.dat')
        f = open(filepathDAT, "a")
        filepathSTATS = os.path.join(currentDirectory, 'stats.txt')
        s = open(filepathSTATS, "a")
        s.write(str(len(courseArray)))
        c.write("id,platform,institution,title,url,class_type,description,rating,rating_max,num_reviews,difficulty,duration,skills,prereqs,cost_type\n")
        for course in courseArray:
            c.write(course.toFileString().lower())
            f.write(course.toFileString().lower())
        f.close()
        c.close()
        s.close()

    except:
        print("Error in Udacity scraper")