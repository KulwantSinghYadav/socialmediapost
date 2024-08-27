from flask import Flask, render_template, request
from dotenv import load_dotenv
from crewai import Agent, Crew
from markdown_it import MarkdownIt
from tasks import MarketingAnalysisTasks
from agents import MarketingAnalysisAgents

load_dotenv()

app = Flask(__name__)

tasks = MarketingAnalysisTasks()
agents = MarketingAnalysisAgents()

# Initialize MarkdownIt
md = MarkdownIt()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # product_description = f"""\
        # The content discusses the transformation of the mortgage finance industry to provide tailored solutions for consumers rather than one-size-fits-all approaches. It emphasizes that each individual's situation is unique and the financing options should reflect this diversity.

        # The company offers distinct services such as home purchase mortgages, refinances, commercials, investments, and assistance for newcomers 
        # to Canada.

        # For home purchase mortgages, the company simplifies the complex process for consumers by doing all the heavy lifting, ensuring that they 
        # secure the best mortgage for their unique needs both in the present and for the future.

        # For refinances, the company offers aid to save money and maximize the refinance or renewal strategy, be it through an equity take out, prepayment plan, or cost saving opportunity.

        # In terms of commercials, the company asserts that the right investment opportunity can alter one's financial future. Regardless of the scenario, they guarantee solutions and take responsibility for finding the right one for the client.

        # For investments, the company assists clients to put their equity to work, allowing them to stay in their home longer. It promises seamless, personalized service that helps clients enjoy their retirement in their own way.

        # Lastly, for those who are new to Canada, the company's brokers  offer assistance in understanding the Canadian real estate environment. This includes information about various risks, the importance of maintaining a stable income, and all the essential details that one needs 
        # to know."""

        product_description = request.form['product_description']
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
        # Convert Markdown to HTML
        ad_copy_html = md.render(ad_copy)

        # Create Crew responsible for Image
        senior_photographer = agents.senior_photographer_agent()
        chief_creative_diretor = agents.chief_creative_diretor_agent()
        # Create Tasks for Image
        take_photo = tasks.take_photograph_task(senior_photographer, ad_copy, topic, product_description)
        approve_photo = tasks.review_photo(chief_creative_diretor, topic, product_description)

        image_crew = Crew(
            agents=[
                senior_photographer
            ],
            tasks=[
                take_photo
            ],
            verbose=True
        )

        images = image_crew.kickoff()
        images_html = md.render(images)

        return render_template('index.html', ad_copy=ad_copy_html, images=images_html)

    return render_template('index.html', ad_copy=None, images=None)

if __name__ == '__main__':
    app.run(debug=True)
