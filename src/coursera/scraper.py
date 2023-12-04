from model.moocClass import moocClass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Coursera start page: https://www.coursera.org/courses?
# Subsequent pages: https://www.coursera.org/courses?page=2

def coursera_scraper(driver):
    print("scrape coursera")
    courseArray = []
    currCourseArray = []
    courseNum = 0


    driver.get("https://www.coursera.org/courses?")
    time.sleep(5)
    try:
        main = driver.find_element(By.CSS_SELECTOR, "main.css-gsohuy")
        lastPage = driver.find_element(By.XPATH, "//button[starts-with(@aria-label, 'Go to last page')]")
        pageCount = lastPage.get_attribute("innerHTML").replace('<span class="cds-button-label">', "").replace("</span>", "")
        currentPage = 1

        while(int(currentPage) <= int(pageCount)):
            try:
                if(int(currentPage) == 1):
                    pageUrl = "https://www.coursera.org/courses?"
                else:
                    pageUrl = "https://www.coursera.org/courses?page=" + str(currentPage)
                driver.get(pageUrl)
                time.sleep(5)
                main = driver.find_element(By.CSS_SELECTOR, "main.css-gsohuy")

                courses = main.find_elements(By.CSS_SELECTOR, "div.cds-ProductCard-base.cds-ProductCard-grid.css-wzhpar")
        
                for course in courses:
                    url = course.find_element(By.CSS_SELECTOR, "a.cds-119.cds-113.cds-115.cds-CommonCard-titleLink.css-si869u.cds-142")
                    currUrl = str(url.get_attribute('href'))
                    if(currUrl.startswith("https://www.coursera.org/professional-certificates/") or currUrl.startswith("https://www.coursera.org/specializations/") or currUrl.startswith("https://www.coursera.org/learn/")):
                        courseNum = courseNum + 1
                        title = url.find_element(By.CSS_SELECTOR, "h3.cds-119.cds-CommonCard-title.css-e7lgfl.cds-121")
                        title = title.text.replace(",", "")
                        try:
                            institution = course.find_element(By.CSS_SELECTOR, "div.cds-ProductCard-header > div.cds-ProductCard-partnerInfo > div.cds-CommonCard-interactiveArea > div.css-oejgx0.cds-ProductCard-partners > p.cds-119.cds-ProductCard-partnerNames.css-dmxkm1.cds-121")
                            if(institution):
                                institution = institution.text.replace(",", "")
                        except:
                            institution = "Coursera"
                        try:
                            skills = course.find_element(By.CSS_SELECTOR, "div.cds-ProductCard-body > div.cds-CommonCard-bodyContent > p.cds-119.cds-Typography-base.css-dmxkm1.cds-121")
                            if(skills):
                                skills = skills.text.replace("Skills you'll gain: ", "").replace(", ", " - ")
                        except:
                            skills = "None"
                        try:
                            costType = course.find_element(By.CSS_SELECTOR, "div.cds-ProductCard-gridPreviewContainer > div.cds-ProductCard-statusTags.cds-ProductCard-statusTagsOverlay > span.cds-119.cds-Typography-base.css-18lymna.cds-121")
                            if(costType):
                                costType = costType.tet_attribute("innerHTML")
                        except:
                            costType = "Paid"
                        try:
                            rating = course.find_element(By.CSS_SELECTOR, "div.cds-CommonCard-ratings > div.css-1vsx0as > div.product-reviews.css-pn23ng > p.cds-119.css-11uuo4b.cds-121")
                            if(rating):
                                rating = rating.text
                                rating_max = 5
                        except:
                            rating = "None"
                            rating_max = 5
                        try:
                            num_reviews = course.find_element(By.CSS_SELECTOR, "div.cds-CommonCard-ratings > div.css-1vsx0as > div.product-reviews.css-pn23ng > p.cds-119.cds-Typography-base.css-dmxkm1.cds-121")
                            if(num_reviews):
                                num_reviews = num_reviews.text.replace("(", "").replace(")", "").replace(" reviews", "")
                        except:
                            num_reviews = "None"
                        try:
                            metadata = course.find_element(By.CSS_SELECTOR, "div.cds-CommonCard-metadata > p")
                            if(metadata):
                                metadataArr = metadata.text.split(" · ")
                                difficulty = metadataArr[0]
                                classType = metadataArr[1]
                                duration = metadataArr[2]
                        except:
                            difficulty = "Beginner"
                            classType = "Course"
                            duration = "None"
                        id = "Coursera" + "-" + str(courseNum)
                        mooc = moocClass(id, "Coursera", institution, title, url.get_attribute('href'), classType, "None", rating, rating_max, num_reviews, difficulty, duration, skills, "None", costType)
                        currCourseArray.append(mooc)
                
                for course in currCourseArray:
                    driver.get(course.url)
                    time.sleep(3)
                    main = driver.find_element(By.CSS_SELECTOR, "section.css-oe48t8")
                    try:
                        description = main.find_element(By.CSS_SELECTOR, "section.css-v6hgh2 > div.css-kd6yq1 > p.cds-119.cds-Typography-base.css-80vnnb.cds-121")
                        if(description):
                            course.description = description.text.replace(",", "")
                    except:
                        course.description = "None"
                    try:
                        prereqs = driver.find_element(By.XPATH, "//div[starts-with(@class, 'cds-Modal-container')]/div/div/div/div/div/div[starts-with(@data-testid, 'cml-viewer')]")
                        if(prereqs):
                            prereqs = prereqs.get_attribute("innerHTML").replace("<p><span><span>", "").replace("</span></span></p>", "").replace('<p data-text-variant="body1"><span><span>', ""). replace("<ul><li>", "").replace("</li><li>", " ").replace("</li></ul>", "").replace("&nbsp;", "")
                            course.prereqs = prereqs.replace(",", "").strip()
                    except:
                        course.prereqs = "None"
                    
                courseArray = courseArray + currCourseArray
                currCourseArray = []
                currentPage += 1
            except:
                print("Error parsing Coursera url: " + pageUrl)

        currentDirectory = os.getcwd()
        currentDirectory = currentDirectory + "\\src\\coursera\\datasets"
        currentDirectory.replace("\\", "\\\\")
        if os.path.exists(currentDirectory + "\\coursera.dat"):
            os.remove(currentDirectory + "\\coursera.dat")
        if os.path.exists(currentDirectory + "\\coursera.csv"):
            os.remove(currentDirectory + "\\coursera.csv")
        if os.path.exists(currentDirectory + "\stats.txt"):
            os.remove(currentDirectory + "\stats.txt")
        filepathCSV = os.path.join(currentDirectory, 'coursera.csv')
        c = open(filepathCSV, "a")
        filepathDAT = os.path.join(currentDirectory, 'coursera.dat')
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
        print("Error in Coursera scraper")