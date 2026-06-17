from agents import Agent , Runner, OpenAIChatCompletionsModel,function_tool,model_settings
from agents.model_settings import ModelSettings
from openai import AsyncOpenAI
import asyncio
from pydantic import BaseModel
from ddgs import DDGS
import os 
from dotenv import load_dotenv
import resend

load_dotenv(override=True)


groq_client = AsyncOpenAI(base_url=os.getenv("GROQ_BASE_URL"), api_key=os.getenv("GROQ_API_KEY"))
gemini_client= AsyncOpenAI(base_url=os.getenv("GEMINI_BASE_URL"),api_key=os.getenv("GEMINI_API_KEY"))
ollama_client = AsyncOpenAI(base_url=os.getenv("OLLAMA_BASE_URL"), api_key=os.getenv("OLLAMA_API_KEY"))
openrouter_client = AsyncOpenAI(base_urL=os.getenv("OPENROUTER_BASE_URL"),api_key=os.getenv("OPENROUTER_API_KEY"))
model1 = OpenAIChatCompletionsModel(model="meta-llama/llama-4-scout-17b-16e-instruct" , openai_client=groq_client)
writer_model = OpenAIChatCompletionsModel(model="meta-llama/llama-4-scout-17b-16e-instruct",openai_client=groq_client)

Instructions = """You are a research assistant. Given a search term, you search the web for that term and \
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 \
words. Capture the main points. Write succintly, no need to have complete sentences or good \
grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the \
essence and ignore any fluff. Do not include any additional commentary other than the summary itself.
"""

@function_tool
def websearchtool(query:str):

    """use this tool to search the web for the given query using duck duck go """
    result = DDGS().text(
        query,
        max_results = 1
    )
    return result

search_agent= Agent(
    name="search agent",
    instructions=Instructions,
    tools=[websearchtool],
    model_settings=ModelSettings(tool_choice="required"),
    model=model1
)

NUMBER_OF_SEARCHES = 3

class WebSearchTerm(BaseModel):
    reason:str 
    """your reasoning for choosing the search term you chose"""
    searchTerm:str
    """The search term that will be used """


class WebSearchPlan(BaseModel):
    searchplan : list[WebSearchTerm]
    """A list of search terms"""


Planner_agent = Agent(
    name="planner agent",
    instructions=f"You are a helpful research assistant. Given a query, come up with a set of web searches\
to perform to best answer the query. Output {NUMBER_OF_SEARCHES} terms to query for.\
",
model=model1,
output_type=WebSearchPlan
)


INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)

class reportSchema(BaseModel):
    summary: str
    """A short summary of the search results given to you"""
    markdown_report: str
    """the final report"""

    follow_up_questions:str
    """suggested topic to research further"""




writer_agent = Agent(
    name="write agent",
    instructions=INSTRUCTIONS,
    model=writer_model,
    output_type=reportSchema
)


@function_tool
def send_email(subject:str , html_body:str):
    """
    Sends an email using the Resend API.
    
    Parameters:
    - subject: The subject of the email.
    - body: The body content of the email.
    
    Returns:
    - A confirmation message indicating the email was sent.
    """
    print("Sending email")
    print(f"Subject: {subject}")
    try:
            resend.api_key = os.getenv("RESEND_APIKEY")
            
            result = resend.Emails.send({
                "from": os.environ.get("EMAIL_FROM", "Acme <onboarding@resend.dev>"),
                "to": ["Youremail@gmail.com"],
                "subject": subject,
                "html": html_body,
                "text": "Welcome! This email was sent using Resend's Python SDK",
            })
            print("Email sent successfully to: demo@gmail.com")
            return "Email sent successfully"
    except Exception as e:
            print(f"Error sending email: {str(e)}")
            raise


emailer_agent= Agent(
     name="Email sender",
     instructions="you are a help full assisstant and your task is to send emails using the tools that are provided to you\
        generate a suitable subject line and write the email in html body and do not use the tool more than one time!!! and once you're done writing the email send it using the send_email tool provided to you ",
    model=model1,
    tools=[send_email]

)
