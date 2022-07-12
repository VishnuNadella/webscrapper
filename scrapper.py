from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from datetime import datetime
import json

def save_data(data):
    file = open(f"data/{dt.strftime('%d-%m')}.json", "wt")
    data = data
    json.dump(data, file)
    file.close()
    print("\n\n\n\n                                                    ---Scrapping Successful---")


options = ChromeOptions()
chrome_driver_path = "C:/Users/vishn/Desktop/proj/chromedriver_win32_103/chromedriver.exe"
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options.binary_location = brave_path
options.headless = True


# comp_page_full_det_vld = "https://dare2compete.com/all-opportunities?filters=,all,all,open&types=teamsize,payment,eligible,oppstatus&keyword=entrepreneur" # paid events
comp_page_full_det_vld = "https://dare2compete.com/all-opportunities?filters=,all,open,unpaid&types=teamsize,eligible,oppstatus,payment&keyword=entrepreneur"

driver = Chrome(executable_path = chrome_driver_path, chrome_options = options)

driver.get(comp_page_full_det_vld)


soup = BeautifulSoup(driver.page_source, "html.parser")

event_page = soup.find_all("h2", class_ = "double-wrap")
event_organized_by = soup.find_all("h3", class_ = "double-wrap ng-star-inserted")
# event_status = soup.find_all("div", class_ = "closed_icons ng-star-inserted") # not required
# event_cash_prz = soup.find_all("div", class_ = "inr ng-star-inserted") # in future
event_dys_lft = soup.find_all("strong", class_ = "ml-5")
if_no_comp = soup.find_all("div", class_ = "no_opportunity ng-star-inserted")
print("No live competitions:", [i.text for i in if_no_comp])
all_addr = []
event_list = driver.find_element_by_tag_name("a")

elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    req = elem.get_attribute("href")
    if ("https://dare2compete.com/competition/" in req or "https://dare2compete.com/workshop/" in req or "https://dare2compete.com/quiz/" in req) and "d2c" not in req:
        all_addr.append(req)


all_events = [i.text for i in event_page]
all_organi = [i.text for i in event_organized_by]
all_vld_dt = [i.text for i in event_dys_lft]
print(all_events, all_organi, all_vld_dt)
# all_przs = [i.text for i in event_cash_prz]

dt = datetime.now()
data = False
try:
    data = [i.text for i in if_no_comp][0]
    save_data(data)
except:
# data = data.replace("No opportunities with the entered keywords", "No live contests going on")
    if data:
        save_data(data)
        # print("DATA IS______________:", data[0])

    else:
        for i in range(len(all_events)):
            try:
                save_data({"Event" : all_events[i], "Organizer" : all_organi[i], "link" : all_addr[i], "Register" : all_vld_dt[i]})
            except Exception as e:
                print("Error:", e)


driver.quit()