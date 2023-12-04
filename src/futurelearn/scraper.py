from selenium import webdriver

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

def futurelearn_scraper(driver):
    print("scrape furturelearn")