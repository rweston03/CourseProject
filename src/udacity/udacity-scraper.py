from selenium import webdriver

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
