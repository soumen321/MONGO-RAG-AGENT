# Application Module
# Orchestrates the RAG workflow using MongoDB, tools, and LangGraph

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from .database import init_mongodb
from .graph import init_graph, execute_graph
from .tools import get_information_for_question_answering, get_page_content_for_summarization
from .config import get_openai_api_key


def main():
    """
    Initialize the application and execute the RAG graph.
    """
    mongodb_client, _, _ = init_mongodb()

    tools = [
        get_information_for_question_answering,
        get_page_content_for_summarization,
    ]

    llm = ChatOpenAI(openai_api_key=get_openai_api_key(), temperature=0, model="gpt-4o")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "You are a helpful AI assistant."
                " You are provided with tools to answer questions and summarize technical documentation related to MongoDB."
                " Think step-by-step and use these tools to get the information required to answer the user query."
                " Do not re-run tools unless absolutely necessary."
                " If you are not able to get enough information using the tools, reply with I DON'T KNOW."
                " You have access to the following tools: {tool_names}."
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    bind_tools = llm.bind_tools(tools)
    llm_with_tools = prompt | bind_tools
    tools_by_name = {tool.name: tool for tool in tools}

    app = init_graph(llm_with_tools, tools_by_name, mongodb_client)

    #execute_graph(app, "thread_1", "What are some best practices for data backups in MongoDB?")
    execute_graph(app, "thread_2", "Give me a summary of the page titled Create a MongoDB Deployment")
