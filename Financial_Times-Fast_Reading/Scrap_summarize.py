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
            titles = scrap_article(6)
        except:
            pass

    #Create a Pandas DataFrame to store the scraped data
    df = pd.DataFrame(titles[0:],columns=["Nom","URL","Article"])

    #Define a function to request text completion from OpenAI API
    def openai_request(prompt):
        # Generate completions for the prompt
        completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.6,
        )
        # Get the generated text and return it
        message = completions.choices[0].text
        return message

    #Iterate through each row of the DataFrame and request text completion from OpenAI API
    for i in range(len(df)):
        test = None
        while test is None:
            try:
                # Connect to OpenAI API and request text completion for article summarization and translation
                print("Analyse article ",i + 1)
                # Use OpenAI API to summarize the article
                df.loc[i, 'Resume'] = openai_request(df.loc[i, 'Article'] + "\nThe article: " + PROMPT)
                # Use OpenAI API to rewrite the article title in French
                df.loc[i, 'Trad_title'] = openai_request(df.loc[i, 'Nom'] + "\nRewrite this in French.\n")
                test = True
            except Exception as e:
                print(e)
                pass

    #Save the scraped and processed data into an Excel file
    df.to_excel('Financial_Times-Fast_Reading/article.xlsx', index=False)

    #Print a message to indicate that the program has finished running
    print('Done')