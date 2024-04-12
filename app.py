import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Lyzr System Designer",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Lyzr System Designer👩🏼‍💻")
st.markdown("### Welcome to the Lyzr System Designer!")
st.markdown("Upload Your Code and Tech stack.This App generating you The System Designer!!!")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

system = st.text_area("Enter Your Requirements: ")
tech = st.text_input("Enter Tech Stack: ",placeholder="Python,AWS,Docker")


def system_designer(systems,tech_stack):
    analysis_agent = Agent(
        role="System Analysis expert",
        prompt_persona=f"You are a system Analyst.your task is to implement system based on requiremnts"
    )

    prompt=f"""You are an expert system analyst.
        Your task is to create system outline for {system}.The technology stack is {tech}.
        Follow below instruction:
        1\ you have to you have to craete Infrastructure and organizational proposed system.
        2\ Think how many data schema possible and generate data schema(design table for each class)
        Design seperate table for each class show as below:
        | Attribute	| Type	  | Description                     |
        | UserID	| String  | Unique identifier for the user  |
        | Name	    | String  |	Name of the user                |
        3\ A function hierarchy diagram or web page map that graphically describes the program structure in given tech and language
        [!important] don't show nothing apart from above details
    """

    Analysis_task = Task(
        name="System Design Task",
        model=open_ai_text_completion_model,
        agent=analysis_agent,
        log_output=True,
        instructions=prompt
    )

    output = LinearSyncPipeline(
        name="System Design Pipeline",
        completion_message="System Created!!",
        tasks=[
            Analysis_task
        ],
    ).run()

    answer = output[0]['task_output']

    return answer


if st.button("Design"):
    solution = system_designer(system,tech)
    st.markdown(solution)

with st.expander("ℹ️ - About this App"):
    st.markdown("""
    This app uses Lyzr Automata For System Design.Enter your system requirements and tech stack.it can generate you system design for your requiremnets.

    """)
    st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width=True)
    st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width=True)
    st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width=True)
    st.link_button("Slack",
                   url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw',
                   use_container_width=True)