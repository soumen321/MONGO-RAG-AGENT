# Main Module
# Entry point for the RAG application with MongoDB and LangGraph
#
# Flow:
# 1. Load configuration and initialize MongoDB connections.
# 2. Register tools for vector search and documentation summarization.
# 3. Build a prompt template that describes the agent's responsibilities.
# 4. Bind the tools to the LLM and compile the LangGraph workflow.
# 5. Execute the graph with a user query and route model outputs to tools when needed.
#
# Tool connections:
# - get_information_for_question_answering: performs vector search over chunked documents.
# - get_page_content_for_summarization: retrieves full page content from the documentation collection.
#
# This file orchestrates the high-level RAG flow while delegating database,
# embedding, graph, and tool logic to separate modules.

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from database import init_mongodb
from graph import init_graph, execute_graph
from tools import get_information_for_question_answering, get_page_content_for_summarization
from config import get_openai_api_key

def main():
    """
    Main function to initialize and execute the graph.
    """

    mongodb_client, vs_collection, full_collection = init_mongodb()

    tools = [
        get_information_for_question_answering,
        get_page_content_for_summarization
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

    # tool_call_check = llm_with_tools.invoke(["What are some best practices for data backups in MongoDB?"]).tool_calls
    # print("Tool call check:")
    # print(tool_call_check)

    tools_by_name = {tool.name: tool for tool in tools}

    app = init_graph(llm_with_tools, tools_by_name, mongodb_client)

    execute_graph(app, "thread_1", "What are some best practices for data backups in MongoDB?")

    execute_graph(app, "thread_2", "Give me a summary of the page titled Create a MongoDB Deployment")

# Execute main function when script is run directly
if __name__ == "__main__":
    main()