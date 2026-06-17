from main import(plan_searches,perform_Searches,write_report)
import gradio as gr



css = """
.prose{
    font-size:20px !important;
}
"""

async def research(topic):
    yield "Planning the Research..."
    searchPlan = await plan_searches(topic)

    yield "Searching the web..."
    search_results = await perform_Searches(searchPlan)

    yield " Writing the report..."
    report = await write_report(
        topic,
        search_results
    )
    yield report.markdown_report

with gr.Blocks(theme=gr.themes.Default()) as demo:
    gr.HTML("<h1 style='font-size:24px; margin:0 0 12px;'>Deep Research Agent</h1>")

    topic = gr.Textbox(
        label="Which topic do you want to research about",
        placeholder="Enter a topic.."
    )
    research_btn = gr.Button("Research")

    output= gr.Markdown()
    research_btn.click(
        fn=research,
        inputs=topic,
        outputs=output
    )
demo.launch(inbrowser=True)