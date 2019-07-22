##### Laura Elliott
##### Web scraping project


from selenium import webdriver
import csv
import re 

driver = webdriver.Chrome()

driver.get("https://www.airbnb.com/s/Hawaii--United-States/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJBeB5Twbb_3sRKIbMdNKCd0s&query=Hawaii%2C%20United%20States&search_type=pagination&s_tag=iX5g1dsA&section_offset=8&items_offset=0")


#writing the csv file 'airbnb_1'
csv_file = open('airbnb_2.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)

#column names
writer.writerow(['title', 'neighborhood', 'rental_type', 'agg_star_rev', 'total_review_num', 'host_location'])

#number of pages 
number_pages = int(driver.find_elements_by_xpath('//ul[@data-id="SearchResultsPagination"]/li/a')[-2].text)
print("Total of pages: {}".format(number_pages))
print('=' * 50)

#urls of pages we will scrape
page_urls = ['https://airbnb.com/s/Hawaii--United-States/homes?refinement_paths%5B%5D=%2Fhomes&query=Hawaii%2C%20United%20States&place_id=ChIJBeB5Twbb_3sRKIbMdNKCd0s&search_type=pagination&s_tag=xG2i-o9D&_set_bev_on_new_domain=1563565303_iFR3lTys363oxr8W&section_offset=7&items_offset={}&adults=1'.format(18 * x) 
for x in range(0, number_pages + 1)]


all_page_urls = []
index = 1

for url in page_urls:
    # output which page is been scraping
    print("Scraping page number " + str(index))

    #find the urls of the separate properties to scrape
    a = driver.find_elements_by_xpath('//div[@class="_8ssblpx"]/div/div/div/div/div/div[2]/div/span/a')
    detail_urls = [x.get_attribute("href") for x in a]

    #number of urls for specific properties to scrape
    driver.get(url)
    print(str(len(detail_urls)) + " links is going to be scraped in this page")
    print('=' * 50)
    

    all_page_urls.extend(detail_urls)
    index += 1

# total rentals available to scrape
index = 1
print("Total of rentals: {}".format(len(all_page_urls)))
print('=' * 50)
# Scraping each rental's page
for url in all_page_urls:
    print("Scraping rental number {} - {:0.2f}% completed".format(index, (index / len(all_page_urls) * 100)))
    driver.get(url)
    result = {}
    

    ### rental data for properties

    ## regular properties, excluding plus properties
    try:
        result['title'] = driver.find_element_by_xpath('//div[@itemprop="name"]/span/h1').text
  
    except:
        result['title'] = None

     #neighborhood rental is found in   
    try:
        result['neighborhood'] = driver.find_element_by_xpath('//div[@class="_czm8crp"]').text
    except:
        result['neighborhood'] = None
        
    # the type of rental offered, i.e. entire house, room in the house, cottage....   
    try:
        result['rental_type'] = driver.find_element_by_xpath('//div[@class="_1p3joamp"]').text
    except:
        result['neighborhood'] = None
        
    # aggregated star review on the rental 
    try:
        result['agg_star_rev'] = driver.find_element_by_xpath('//div[@class="_l0ao8q"]/div/div').get_attribute("content")
    except:
        result['agg_star_rev'] = None
        
    # number of reviews given
    try:
        result['total_review_num'] = driver.find_element_by_xpath('//span[@class="_s1tlw0m"]').text
    except:
        result['total_review_num'] = None
        
    # where the host is located
    try:
        result['host_location'] =  driver.find_element_by_xpath('//div[@class="_czm8crp"]/span').text
    except:
        result['host_location'] = None



    index += 1
    writer.writerow(result.values())

csv_file.close()
driver.close()
    
    