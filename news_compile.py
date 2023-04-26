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

# class to simplify process
class KompasScraper:
    # set init
    def __init__(self):
        self.headlines = []
        self.head_urls = []
        self.authors = []
        self.publish = []
        self.article_raw  = []
        self.article_semi = []
        self.driver = None

    # function to run the url scraper
    def run_url(self, page_max):
        # set web options
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("detach", True)
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")

        # set driver
        self.driver = Chrome(executable_path='/chromedriver.exe', options=options)
        self.page_max = page_max

        # start loop
        print('Process started... \n')
        bar = Bar('Processing', max=self.page_max)  # add progress bar        
        for page in range(1, self.page_max + 1):
            try:
                # define page url
                site_url = 'https://indeks.kompas.com/?site=global'
                page_no = f'&page={page}'
                self.driver.get(site_url + page_no)
                self.driver.implicitly_wait(8)

                # click popup
                self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[5]/a').click()
                self.driver.implicitly_wait(3)

                # data collection (headline and url)
                headline = []
                head_url = []
                for i in range(1, 16):
                    head = self.driver.find_element(by=By.XPATH, value=f'/html/body/div[1]/div[2]/div[4]/div[1]/div[3]/div[{i}]/div[2]/h3/a').text
                    urls = self.driver.find_element(by=By.XPATH, value=f'/html/body/div[1]/div[2]/div[4]/div[1]/div[3]/div[{i}]/div[2]/h3/a').get_attribute('href')
                    headline.append(head)
                    head_url.append(urls)
                    self.driver.implicitly_wait(3)

                bar.next()
                print(f" Scraping page {page} of {self.page_max} \n")

                # put to main list
                self.headlines.extend(headline)
                self.head_urls.extend(head_url)

            except:
                pass

        # end loop
        bar.finish()
        print('Finished! \n')

        # close driver
        self.driver.quit()

        # transform to dataframe
        df = pd.DataFrame({'headlines': self.headlines,
                           'headline_url': self.head_urls})

        # pass to csv file
        df.to_csv("data\kompas_news_url.csv", index=0)
        print("Data successfully written to csv file")

    # function to run the news article scraper
    def run_article(self):
        # set options
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("detach", True)
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")

        # set driver
        self.driver = Chrome(executable_path='/chromedriver.exe', options=options)

        # import data
        df = pd.read_csv("data/kompas_news_url.csv")

        # start loop
        print('Process started... \n')

        # set url list
        urls = df["headline_url"][:]
        bar = Bar('Processing', max=len(urls)) # add progress bar

        # data collection
        for idx, url in enumerate(urls):
            try:
                # define url
                self.driver.get(url)
                self.driver.implicitly_wait(5)

                # close popup
                self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[6]/a').click()
                self.driver.implicitly_wait(3)

                # get data (author, published date, news content)
                auth = self.driver.find_element(by=By.XPATH, value='//*[@id="penulis"]/a').text
                pubs = self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[5]/div[1]/div[1]/div[1]/div').text
                news = self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[5]/div[1]/div[4]/div[2]/div[2]').text

                # get the page source and parse it using bs4
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                news_text = soup.find("div", class_="read__content").find_all("p")

                # append all data
                self.authors.append(auth)
                self.publish.append(pubs)
                self.article_raw.append(news_text)
                self.article_semi.append(news)
                
                self.driver.implicitly_wait(3)
                bar.next()
                print(f" - Scraping news article number {idx} of {len(urls)} \n")

            except:
                pass

        # end loop
        bar.finish()
        print('Finished! \n')

        # close driver
        self.driver.quit()

        # transform to dataframe
        df = pd.DataFrame({'author' : self.authors, 
                           'publish_date': self.publish,
                           'news_article_raw': self.article_raw,
                           'news_article_semi': self.article_semi})

        # pass to csv file
        df.to_csv("data\kompas_news_article.csv", index=0)
        print("Data successfully written to csv file")

#run init program
if __name__ == "__main__":
    print("set max page to scrape:")
    max_page = int(input())
    scraper = KompasScraper()
    scraper.run_url(page_max=max_page)
    scraper.run_article()