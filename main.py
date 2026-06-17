import asyncio
from ai_agents import WebSearchPlan,WebSearchTerm,Planner_agent,search_agent,writer_agent,reportSchema,emailer_agent
from agents import Runner

async def plan_searches(query:str):
    """use this function to create a search plan based on user query"""
    print("planning searches...")
    results = await Runner.run(Planner_agent,query)
    
    return results.final_output

async def perform_Searches(searchplan:WebSearchPlan):
    """use the search() function to search for each term"""
    print("performing the searches..")
    results = []
    for item in searchplan.searchplan:
        results.append( await search(item))
    return results
async def search(item: WebSearchTerm):
    print("calling search agent...")
    input=f"reason for search{item.reason} and search term: {item.searchTerm}"
    result =await Runner.run(search_agent,input)
    return result.final_output

async def write_report(searchTerm: str, searchResults:list[str]):
    print("writing the report")
    input = f"original searchterm:{searchTerm} and summary of searches performed:{searchResults}"
    result = await Runner.run(writer_agent,input)
    print("finished the report..")
    return result.final_output

async def emailsender(reports:reportSchema):
    print("calling email sender..")
    await Runner.run(emailer_agent,reports.markdown_report)
    print("email sent...")



async def main():
    query = "top 6 agentic ai frameworks of 2026"
    searchplan =  await plan_searches(query)
    searchresults = await perform_Searches(searchplan)
    report = await write_report(query,searchresults)
    result= await emailsender(report)
if __name__=="__main__":

    asyncio.run(main())
    
