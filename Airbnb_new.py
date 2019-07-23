
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import csv
import re 

driver = webdriver.Chrome()

driver.get("https://www.airbnb.com/s/Hawaii--United-States/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJBeB5Twbb_3sRKIbMdNKCd0s&query=Hawaii%2C%20United%20States&search_type=pagination&s_tag=iX5g1dsA&section_offset=8")


#writing the csv file 'airbnb_1'
csv_file = open('airbnb_new.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)


number_pages = int(driver.find_elements_by_xpath('//ul[@data-id="SearchResultsPagination"]/li/a')[-2].text)
print("Total of pages: {}".format(number_pages))
print('=' * 50)

page_urls = ['https://www.airbnb.com/s/Hawaii--United-States/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJBeB5Twbb_3sRKIbMdNKCd0s&query=Hawaii%2C%20United%20States&search_type=pagination&s_tag=iX5g1dsA&section_offset=8&items_offset={}'.format(18 * x) 
for x in range(0, number_pages + 1)]

all_page_urls = []
index = 1



for url in page_urls:
    print("Scraping page number" + str(index))


    a = driver.find_elements_by_xpath('//div[@class="_8ssblpx"]/div/div/div/div/div/div[2]/div/span/a')
    detail_urls = [x.get_attribute("href") for x in a]

    #number of urls for specific properties to scrape
    driver.get(url)
    print(str(len(detail_urls)) + " links is going to be scraped in this page")
    print('=' * 50)
    

    all_page_urls.extend(detail_urls)
    index += 1


index = 1
print("Total of rentals: {}".format(len(all_page_urls)))
print('=' * 50)

for url in all_page_urls:
    print("Scraping rental number {} - {:0.2f}% completed".format(index, (index / len(all_page_urls) * 100)))
    driver.get(url)
    result = {}

    wait_rental = WebDriverWait(driver, 10)

    try:
        result['title'] = driver.find_element_by_xpath('//div[@class="_1hpgssa1"]/div/div/span/h1/span').text
    except: 
        result['title'] = None
            
    try:
        result['location'] = driver.find_element_by_xpath('//div[@class="_1hpgssa1"]/div[2]/div/a/div').text
    except:
        result['location'] = None
        
    try:
        result['rental_type'] = driver.find_element_by_xpath('//div[@class="_1gw6tte"]/div/div/div/div[2]/div').text
    except:
        result['rental_type'] = None    
    
    try:
        result['total_review_num'] = driver.find_element_by_xpath('//div[@class="_mwt4r90"]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/button/span[2]').text
    except:
         result['total_review_num'] = None
            
    try:
        result['feat_amenities'] = driver.find_element_by_xpath('//div[@class="_1gw6tte"]/div/div/div/div/section/div[4]/div/button').text
    except:
         result['feat_amenities'] = None
    
    try:
        result['price'] =  driver.find_element_by_xpath('//div[@class="_mwt4r90"]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/span[2]/span').text
    except:
         result['price'] = None

    try:
        result['host'] = driver.find_element_by_xpath('//div[@class="_hgs47m"]/div/div/h2/span').text
    except:
         result['host'] = None

    try:
        result['host_location'] = driver.find_element_by_xpath('//div[@class="_10ejfg4u"]/div[2]/span[1]').text
    except:
         result['host_location'] = None

    try:
        result['host_reviews'] = driver.find_element_by_xpath('//div[@class="_1gw6tte"]/div/div/section/div/div[2]/div/div/div/div[2]/div').text
    except:
         result['host_reviews'] = None

    try:
        result['rental_age'] = driver.find_element_by_xpath('//div[@style="margin-top:40px;margin-bottom:8px"]/div[1]/div/div[1]/div[2]').text
    except:
         result['rental_age'] = None



    index += 1
    writer.writerow(result.values())


csv_file.close()
driver.close()



    