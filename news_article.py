# import libraries
import pandas as pd
import warnings
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from progress.bar import Bar

# filter warning
warnings.filterwarnings(action='ignore')

# set options
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")

# set driver
driver = Chrome(executable_path='/chromedriver.exe', options=options)

# import data
df = pd.read_csv("data/kompas_news_url.csv")

# start loop
print('Process started... \n')

# set url list
urls = df["headline_url"][:]
bar = Bar('Processing', max=len(urls)) # add progress bar

# data collection
authors = []
publish = []
article_raw  = []
article_semi = []
for idx, url in enumerate(urls):
    try:
        # define url
        driver.get(url)
        driver.implicitly_wait(5)

        # close popup
        driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[6]/a').click()
        driver.implicitly_wait(3)

        # get data (author, published date, news content)
        auth = driver.find_element(by=By.XPATH, value='//*[@id="penulis"]/a').text
        pubs = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[5]/div[1]/div[1]/div[1]/div').text
        news = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[5]/div[1]/div[4]/div[2]/div[2]').text

        # get the page source and parse it using bs4
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        news_text = soup.find("div", class_="read__content").find_all("p")

        # append all data
        authors.append(auth)
        publish.append(pubs)
        article_raw.append(news_text)
        article_semi.append(news)
        
        driver.implicitly_wait(3)
        bar.next()
        print(f" - Scraping news article number {idx} of {len(urls)} \n")

    except:
        pass

# end loop
bar.finish()
print('Finished! \n')

# close driver
driver.quit()

# transform to dataframe
df = pd.DataFrame({'author' : authors, 
                   'publish_date': publish,
                   'news_article_raw': article_raw,
                   'news_article_semi': article_semi})

# pass to csv file
df.to_csv("data\kompas_news_article.csv", index=0)
print("Data successfully written to csv file")