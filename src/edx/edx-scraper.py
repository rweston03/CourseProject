from selenium import webdriver

# Edx catalog URL: https://www.edx.org/search?learning_type=Course&tab=course
# Pages after first: https://www.edx.org/search?learning_type=Course&tab=course&page=2
# Edx pagination: nav.pagination-secondary.pagination-small > ul.pagination[6th child].page-item > button[aria label or text content]