from model.moocClass import moocClass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Coursera start page: https://www.coursera.org/courses?
# Subsequent pages: https://www.coursera.org/courses?page=2

def coursera_scraper(driver, currentDirectory, pageNum):
    print("Scrape coursera")

    #Initialize variables
    currCourseArray = []
    courseNum = 0
    totalCourses = 0

    # Clear out existing files if they exist and prepare new files for writing
    if os.path.exists(currentDirectory + "\\coursera.dat"):
        os.remove(currentDirectory + "\\coursera.dat")
    if os.path.exists(currentDirectory + "\\coursera.csv"):
        os.remove(currentDirectory + "\\coursera.csv")
    if os.path.exists(currentDirectory + "\stats.txt"):
        os.remove(currentDirectory + "\stats.txt")
    if os.path.exists(currentDirectory + "\errors.txt"):
        os.remove(currentDirectory + "\errors.txt")
    filepathCSV = os.path.join(currentDirectory, 'coursera.csv')
    c = open(filepathCSV, "a", encoding="utf-8")
    filepathDAT = os.path.join(currentDirectory, 'coursera.dat')
    f = open(filepathDAT, "a", encoding="utf-8")
    filepathERR = os.path.join(currentDirectory, 'errors.txt')
    e = open(filepathERR, "a", encoding="utf-8")
    filepathSTATS = os.path.join(currentDirectory, 'stats.txt')
    c.write("id,platform,institution,title,url,class_type,description,rating,rating_max,num_reviews,difficulty,duration,skills,prereqs,cost_type\n")

    # Fetch the first course page
    driver.get("https://www.coursera.org/courses?")

    # Add sleep setting to allow page to fully load
    time.sleep(5)
    try:
        # Get total number of course catalog pages
        main = driver.find_element(By.CSS_SELECTOR, "main")
        lastPage = driver.find_element(By.XPATH, "//button[starts-with(@aria-label, 'Go to last page')]")
        pageCount = lastPage.get_attribute("innerHTML").replace('<span class="cds-button-label">', "").replace("</span>", "")
        pageCount = int(pageCount)

        # Set current page to 1
        currentPage = 1

        # If a desired number of pages has been passed in, use it if it is under the total number of course catalog pages
        # Otherwise, use the total
        if(pageNum != 0 and pageNum <= pageCount):
            pageCount = pageNum

        # Scrape course catalog pages until the last page is reached
        while(int(currentPage) <= pageCount):
            try:
                # Get the current course catalog page
                if(int(currentPage) == 1):
                    pageUrl = "https://www.coursera.org/courses?"
                else:
                    pageUrl = "https://www.coursera.org/courses?page=" + str(currentPage)
                driver.get(pageUrl)
                # Wait for it to load
                time.sleep(5)
                try:
                    # Wait for main element and courses to be displayed
                    main = driver.find_element(By.CSS_SELECTOR, "main")
                    courses = main.find_elements(By.CSS_SELECTOR, "div.cds-ProductCard-base.cds-ProductCard-grid.css-wzhpar")
                except:
                    # If the necessary elements aren't displayed, get the page again and wait a little longer for the elements to be displayed
                    if(int(currentPage) == 1):
                        pageUrl = "https://www.coursera.org/courses?"
                    else:
                        pageUrl = "https://www.coursera.org/courses?page=" + str(currentPage)
                    driver.get(pageUrl)
                    time.sleep(10)
                    main = driver.find_element(By.CSS_SELECTOR, "main")
                    courses = main.find_elements(By.CSS_SELECTOR, "div.cds-ProductCard-base.cds-ProductCard-grid.css-wzhpar")

                # Iterate through the courses on the course catalog page and scrape the available information for each course
                for course in courses:
                    url = course.find_element(By.CSS_SELECTOR, "a.cds-119.cds-113.cds-115.cds-CommonCard-titleLink.css-si869u.cds-142")
                    currUrl = str(url.get_attribute('href'))

                    # Check to make sure that the course element in the course catalog points to a course detail page instead of an advertisement or some other page
                    if(currUrl.startswith("https://www.coursera.org/professional-certificates/") or currUrl.startswith("https://www.coursera.org/specializations/") or currUrl.startswith("https://www.coursera.org/learn/")):
                        courseNum = courseNum + 1
                        title = url.find_element(By.CSS_SELECTOR, "h3.cds-119.cds-CommonCard-title.css-e7lgfl.cds-121")
                        title = title.text.replace(",", "").replace("\n","")
                        try:
                            institution = course.find_element(By.CSS_SELECTOR, "div.cds-ProductCard-header > div.cds-ProductCard-partnerInfo > div.cds-CommonCard-interactiveArea > div.css-oejgx0.cds-ProductCard-partners > p.cds-119.cds-ProductCard-partnerNames.css-dmxkm1.cds-121")
                            if(institution):
                                institution = institution.text.replace(",", "").replace("\n","")
                        except:
                            institution = "Coursera"
                        try:
                            skills = course.find_element(By.CSS_SELECTOR, "div.cds-ProductCard-body > div.cds-CommonCard-bodyContent > p.cds-119.cds-Typography-base.css-dmxkm1.cds-121")
                            if(skills):
                                skills = skills.text.replace("Skills you'll gain: ", "").replace(", ", " - ").replace("\n","")
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

                # After scraping the course catalog page, iterate through the courses found and scrape their detail pages
                for course in currCourseArray:
                    driver.get(course.url)
                    liveUrl = driver.current_url
                    time.sleep(3)
                    if(liveUrl == course.url):
                        main = driver.find_element(By.CSS_SELECTOR, "section.css-oe48t8")
                        try:
                            description = main.find_element(By.CSS_SELECTOR, "section.css-v6hgh2 > div.css-kd6yq1 > p.cds-119.cds-Typography-base.css-80vnnb.cds-121")
                            if(description):
                                course.description = description.text.replace(",", "").replace("• ", "").replace("\n", " ").strip()
                        except:
                            course.description = "None"
                        try:
                            prereqs = driver.find_element(By.XPATH, "//div[starts-with(@class, 'cds-Modal-container')]/div/div/div/div/div/div[starts-with(@data-testid, 'cml-viewer')]")
                            if(prereqs):
                                prereqs = prereqs.get_attribute("innerHTML").replace("<p><span><span>", "").replace("</span></span></p>", "").replace('<p data-text-variant="body1"><span><span>', ""). replace("<ul><li>", "").replace("</li><li>", " ").replace("</li></ul>", "").replace("&nbsp;", "")
                                course.prereqs = prereqs.replace(",", "").replace("• ", "").replace("\n", " ").strip()
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
                print("Error parsing Coursera url: " + pageUrl)

        c.close()
        e.close()
        f.close()
 
        # Write the total number of courses scraped to the stats file
        s = open(filepathSTATS, "w")
        s.write(str(totalCourses))
        s.close()

    except:
        print("Error in Coursera scraper")