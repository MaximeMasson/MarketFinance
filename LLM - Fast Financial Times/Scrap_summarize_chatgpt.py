import openai
import pandas as pd
from Connection_ft import scrap_article
import os
from dotenv import load_dotenv

def ScrapSum():
    load_dotenv()
    API = os.getenv("API")
    PROMPT = os.getenv("PROMPT")
    
    #Set OpenAI API key
    openai.api_key = API
   
    #Scrape articles from the web using a custom function
    titles = None
    while titles is None:
        try:
            # Connect to the website and scrape articles
            titles = scrap_article(5)
        except:
            pass

    #Create a Pandas DataFrame to store the scraped data
    df = pd.DataFrame(titles[0:],columns=["Nom","URL","Article"])

    # Read data from an Excel file using pandas
    #df = pd.read_excel("Financial_Times-Fast_Reading/article.xlsx")
    
    #Define a function to request text completion from OpenAI API
    def openai_request(ask, article):
        chat = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": ask},
        {"role": "user", "content": article},
    ]
)
        reply = chat.choices[0].message.content
        return reply

    #Iterate through each row of the DataFrame and request text completion from OpenAI API
    for i in range(len(df)):
        test = None
        while test is None:
            try:
                # Connect to OpenAI API and request text completion for article summarization and translation
                print("Analyse article ",i + 1)
                # Use OpenAI API to summarize the article
                df.loc[i, 'Resume'] = openai_request(PROMPT ,df.loc[i, 'Article'])
                # Use OpenAI API to rewrite the article title in French
                df.loc[i, 'Trad_title'] = openai_request("Rewrite it in French", df.loc[i, 'Nom'])
                test = True
            except Exception as e:
                print(e)
                pass

    #Save the scraped and processed data into an Excel file
    df.to_excel('Financial_Times-Fast_Reading/article.xlsx', index=False)

    #Print a message to indicate that the program has finished running
    print('Done')
    