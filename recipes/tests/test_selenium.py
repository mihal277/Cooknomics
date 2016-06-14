from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://localhost:8000/recipes/")
assert "Recipes" in driver.title
elem = driver.find_element_by_class_name("app_title")
assert "RECIPES" in elem.text
elem = driver.find_element_by_id("search_button")
assert "Wyszukaj" in elem.text
elem = driver.find_element_by_id("downvote_count_banan")
before = elem.text
upvote_button = driver.find_element_by_id("dwnbtn_banan").click()
after = elem.text
assert after == before+1
driver.close()
