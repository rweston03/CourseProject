# CourseProject

This course project scrapes course information from Coursera, Edx, and Udacity.

## Setup
You will need to install the following:
1. Google Chrome (if you don't already have it) - https://www.google.com/chrome/
2. ChromeDriver - https://chromedriver.chromium.org/
    - NOTE: if you are on Chrome version 115 or higher, you will need to find the correct ChromeDriver in the chrome-for-testing 
            area of the website: https://googlechromelabs.github.io/chrome-for-testing/
    - This download is just an executable. I put the chromedriver.exe files in the following location: "C:\Program Files (x86)\chromedriver.exe". If you put yours elsewhere, you
      will need to update this path in the places marked in the python web scraper files.
3. Selenium - install via pip in virtual environment with command "pip install Selenium"

## Running the Program

You can run all the scrapers for all available pages by just running:
```
python.exe src/main.py
```

However, if you want to run a smaller subset of the scrapers or capture a smaller number of pages, you can run one of these commands:

```
# Replace {subset} with your desired subset: coursera, edx, udacity, or all
# Replace {number of pages} with an integer value for your desired number of pages (i.e. 1, 20, etc.)

python.exe src/main.py {subset} {number of pages}
```

Subset datasets will show up in the nested "limited" folders within the datasets folders.