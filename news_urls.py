# import libraries
import pandas as pd
import warnings
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from progress.bar import Bar

# filter warning
warnings.filterwarnings(action='ignore')

# set web options
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")

# set driver
driver = Chrome(executable_path='/chromedriver.exe', options=options)

# start loop
print('Process started... \n')

# set max page to scrape
page_max = 20
bar = Bar('Processing', max=page_max) # add progress bar

# data collection
headlines = []
head_urls = []
for pages in range(1, int(page_max)+1):
    try:
        # define page url
        site_url = 'https://indeks.kompas.com/?site=global'
        page_no  = f'&page={pages}'
        driver.get(site_url+page_no)
        driver.implicitly_wait(8)

        # click popup
        driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[5]/a').click()
        driver.implicitly_wait(3)

        # data collection (headline and url)
        headline = []
        head_url = []
        for i in range(1, 16):
            head = driver.find_element(by=By.XPATH, value=f'/html/body/div[1]/div[2]/div[4]/div[1]/div[3]/div[{i}]/div[2]/h3/a').text
            urls = driver.find_element(by=By.XPATH, value=f'/html/body/div[1]/div[2]/div[4]/div[1]/div[3]/div[{i}]/div[2]/h3/a').get_attribute('href')
            headline.append(head)
            head_url.append(urls)
            driver.implicitly_wait(3)
        
        bar.next()
        print(f" Scraping page {pages} of {page_max} \n")

        # put to main list
        headlines.extend(headline)
        head_urls.extend(head_url)

    except:
        pass

# end loop
bar.finish()
print('Finished! \n')

# close driver
driver.quit()

# transform to dataframe
df = pd.DataFrame({'headlines' : headlines, 
                   'headline_url': head_urls})

# pass to csv file
df.to_csv("data\kompas_news_url.csv", index=0)
print("Data successfully written to csv file")