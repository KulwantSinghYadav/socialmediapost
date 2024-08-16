from flask import Flask, render_template, request
from dotenv import load_dotenv
from crewai import Agent, Crew
from tasks import MarketingAnalysisTasks
from agents import MarketingAnalysisAgents

load_dotenv()

app = Flask(__name__)

tasks = MarketingAnalysisTasks()
agents = MarketingAnalysisAgents()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_description = f"""\
        The content discusses the transformation of the mortgage finance industry to provide tailored solutions for consumers rather than one-size-fits-all approaches. It emphasizes that each individual's situation is unique and the financing options should reflect this diversity.

        The company offers distinct services such as home purchase mortgages, refinances, commercials, investments, and assistance for newcomers 
        to Canada.

        For home purchase mortgages, the company simplifies the complex process for consumers by doing all the heavy lifting, ensuring that they 
        secure the best mortgage for their unique needs both in the present and for the future.

        For refinances, the company offers aid to save money and maximize the refinance or renewal strategy, be it through an equity take out, prepayment plan, or cost saving opportunity.

        In terms of commercials, the company asserts that the right investment opportunity can alter one's financial future. Regardless of the scenario, they guarantee solutions and take responsibility for finding the right one for the client.

        For investments, the company assists clients to put their equity to work, allowing them to stay in their home longer. It promises seamless, personalized service that helps clients enjoy their retirement in their own way.

        Lastly, for those who are new to Canada, the company's brokers  offer assistance in understanding the Canadian real estate environment. This includes information about various risks, the importance of maintaining a stable income, and all the essential details that one needs 
        to know."""
        topic = request.form['topic']
        #product_description = request.form['product_description']

        # Create Agents
        creative_agent_from_article = agents.creative_content_creator_agent_from_article()

        # Create Tasks
        write_copy_from_news = tasks.instagram_ad_copy_from_news(creative_agent_from_article, product_description, topic)
        write_news_article_summary = tasks.find_news_articles_summary_for_topic_task(creative_agent_from_article, topic, product_description)


        # Create Crew responsible for Copy
        copy_crew = Crew(
            agents=[creative_agent_from_article],
            tasks=[write_news_article_summary, 
                   write_copy_from_news],
            verbose=True
        )

        # Get ad copy
        ad_copy = copy_crew.kickoff()

        return render_template('index.html', ad_copy=ad_copy)

    return render_template('index.html', ad_copy=None)

if __name__ == '__main__':
    app.run(debug=True)
