
import json
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

session = requests.Session()

# define the data source (Ynet)
categories_links = {
    "sport": "https://www.ynet.co.il/topics/%D7%A1%D7%A4%D7%95%D7%A8%D7%98",
    "entertainment": "https://www.ynet.co.il/topics/%D7%AA%D7%A8%D7%91%D7%95%D7%AA",
    "economy": "https://www.ynet.co.il/topics/%D7%9B%D7%9C%D7%9B%D7%9C%D7%94",
    "health": "https://www.ynet.co.il/topics/%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA",
    "car": "https://www.ynet.co.il/topics/%D7%A8%D7%9B%D7%91",
    "food": "https://www.ynet.co.il/topics/%D7%90%D7%95%D7%9B%D7%9C",
    "vacation": "https://www.ynet.co.il/topics/%D7%97%D7%95%D7%A4%D7%A9",
    "dating": "https://www.ynet.co.il/topics/%D7%99%D7%97%D7%A1%D7%99%D7%9D",
    "parents": "https://www.ynet.co.il/topics/%D7%94%D7%95%D7%A8%D7%99%D7%9D",
    "environment-science": "https://www.ynet.co.il/topics/%D7%9E%D7%93%D7%A2_%D7%91%D7%A1%D7%91%D7%99%D7%91%D7%94"
}

# define the categories we want to scrape from Ynet [sport, entertainment, economy, health, car, food, vacation, dating, parents, environment-science]
categories = list(categories_links.keys())

# create a dataframe to store the data which has the following columns: text, sport, entertainment, economy, health, car, food, vacation, dating, parents, environment-science
df = pd.DataFrame(columns=["text"] + categories)

# get 100 pages from each category and save them to df
for i in tqdm(range(100), desc="Progress"):

    for category in categories:

        rows = {col: [] for col in df.columns}

        category_link = f"{categories_links[category]}/{i}"
        categories_responses = session.get(category_link)
        categories_soups = BeautifulSoup(categories_responses.text, 'html.parser')

        # get all the articles links from the page
        articles_links = [div.find('a').attrs['href'] for div in categories_soups.findAll('div', attrs={'class':'slotTitle'}) if div.find('a').attrs['href'].startswith(f'https://www.ynet.co.il/')]

        for link in articles_links:
            response = session.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # get the title, description and the body of the article (the body is in a json format so we need to parse it to get the articleBody and the description)
            title = soup.find('title').text.strip()
            body = soup.find('script', attrs={'type':'application/ld+json'}).contents[0].replace('\t', '')

            # parse the body of the article and in case of an error in the json decode use regex to fix the json format
            try:
                parsed_body = json.loads(body)
                articleBody = parsed_body['articleBody']
                description = parsed_body['description']
            except json.JSONDecodeError:
                valid = re.sub(r'([{,]\s*?"[^"]+"\s*:)\s*,', r'\1 null,', body)
                parsed_body = json.loads(valid)
                articleBody = parsed_body['articleBody']
                description = parsed_body['description']
            except:
                continue

            # clean the text from any special characters and spaces
            description = description.strip()
            articleBody = articleBody.strip()

            text = title + " " + description + " " + articleBody
            # clean the text from any special characters and spaces
            text = ''.join(e for e in text if e.isalnum() or e.isspace())

            # append the text to the dataframe and add 1 in its matching category and 0 in the rest
            for key in rows.keys():
                rows[key].append(0)
            rows['text'][-1] = text
            rows[category][-1] = 1

        # save the data to a csv file for each category
        pd.DataFrame(rows).to_csv('texts.csv', mode='a', header=False, index=False)

