from selenium import webdriver
from bs4 import BeautifulSoup

start_date = "2023-02-11"
end_date = "2023-02-13"

driver = webdriver.Chrome()
url = f"https://www.royalcaribbean.com/cruises?search=ship:WN|startDate:{start_date}~{end_date}"
driver.get(url)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()
cruise_results = soup.find(id="cruise-results-wrapper")

if len(list(cruise_results.children)) > 0:
    print("Yay")
else:
    print("Fuck")
