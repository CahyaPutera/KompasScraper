# Project Name: News Scraper - A Web Scraper for News Articles

This is an experimental Sentiment Analysis mini project based on web scraped news article data from the [kompas.com](https://www.kompas.com/) website.

## Table of Contents

1. Installation Requirements
2. Usage
3. Disclaimer

## Installation Requirements

To set up this program on your local machine, you will need to follow these steps:

1. Clone the repository from Github.
2. Setup virtualenv: 
```bash
python -m venv [envname]
```
3. Activate the virtual env: 
```bash
.\venv\Scripts\activate
```
4. Install the requirements using pip method:
```bash
pip install -r requirements.txt
```

## Usage

There are 3 separate Python programs (.py) and 2 Python notebooks (.ipynb) included in the 'notebook' folder for this project.

The Python programs are:

1. `news_url.py`: This script will only scrape the news headline and URL and can be run independently.
2. `news_article.py`: This script will get the URL stored from news_url.py process and will scrape information regarding the news article, such as author name, published date, and the main article itself.
3. `news_compile.py`: This script is the combination of the two previous scripts using a class method to simplify and ease the process. To run this, you will need to enter the maximum page that you want to scrape (as of 25/03/2023, the maximum page limit is about 666 pages).

To run the program, you can use standard python syntax `python [program_name]`.

The Python notebooks are:
1. `news_scraper_prep.ipynb`: This notebook focuses solely on preparing scraped news article data for the Sentiment Analysis project requirements.
2. `news_scraper_model.ipynb`: This notebook is to create and compare between 2 models (SVM and XGB) to determine which is better to predict the the scraped news article data.

The result of experimentation showed that both SVM and XGB models perform relatively well in classifying the articles into positive and negative sentiment categories. 
Interestingly, the lexicon methods are the one who actually affected the results instead of the model algorithm itself. 
However, further experimentation may be necessary to prove this.

## Disclaimer

This project is a non-profit and is for educational purposes only. 
The code and information provided here is not intended for commercial purposes or for use in any commercial products. 
The authors of this project are not responsible for any damages or losses that may result from the use of this project.
