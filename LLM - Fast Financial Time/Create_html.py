import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import date
import os

def CreateHTML():   
    # Read data from an Excel file using pandas
    df = pd.read_excel("Financial_Times-Fast_Reading/article.xlsx")

    # Retrieve values from the first column and first row to use as title and article
    titre = df.iloc[0, 0]
    article = df.iloc[0, -1]

    # Use Jinja2 to generate HTML code
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("Financial_Times-Fast_Reading/template.html")

    # Fill the template with data from each row
    cards = []
    for i in range(len(df)):
        cards.append({"titre": df.iloc[i,0], "article": str(df.iloc[i,-2])[0:].replace("\n", "<br>"), "Trad_title": df.iloc[i,-1], "lien": df.iloc[i,1]})
        
    # Generate the HTML page
    html_output = template.render(cards=cards)

    # Save the result to an HTML file
    today = date.today()
    with open("Financial_Times-Fast_Reading/Article/ft_top_"+ today.strftime("%Y-%m-%d") +".html", "w", encoding='utf-8') as f:
        f.write(html_output)    
