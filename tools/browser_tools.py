import json
import os

import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html

from newspaper import Article

#from langchain.llms import Ollama

class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(website):
    """Useful to scrape and summarize a website content, just pass a string with
    only the full url, no need for a final slash `/`, eg: https://google.com or https://clearbit.com/about-us"""
    
    summaries = []


    #USE ARTICLE FOR SCRAPPING
    title = []
    text = []
    url=website
    # We scrape the news site to collect the content over there
    if url:
        article = Article(url)
        article.download()
        article.parse()
        title.append(article.title)
        text.append(article.text)
        content_new = [text[i:i + 8000] for i in range(0, len(text), 8000)]

    #print(f'\nScrapped Content raw: {content_new}\n')





    for chunk in content_new:
      agent = Agent(
          role='Principal Researcher',
          goal=
          'Do amazing researches and summaries based on the content you are working with',
          backstory=
          "You're a Principal Researcher at a big company and you need to do a research about a given topic.",
          #llm=Ollama(model=os.environ['MODEL']),
          allow_delegation=False)
      task = Task(
          agent=agent,
          description=
          f'Analyze and make a LONG summary the content bellow, make sure to include the ALL relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
      )
      summary = task.execute()
      summaries.append(summary)
      content_new = "\n\n".join(summaries)
      print(f'\nScrapped Content formatted: {content_new}\n')
    return f'\nScrapped Content: {content_new}\n'

