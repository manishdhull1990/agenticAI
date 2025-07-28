from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatOpenAI()

def chat_node(state: ChatState):
    #take user query from state
    messages = state['messages']

    #send it to the llm
    response = llm.invoke(messages)

    #response store state
    return {'messages': [response]}

checkpointer = MemorySaver()

graph = StateGraph(ChatState)

#add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)
chatbot = graph.compile(checkpointer=checkpointer)

# inital_state = {'messages':[HumanMessage(content='What is the capital of India')]}

# print(chatbot.invoke(inital_state))
thread_id = '1'

while True:
    user_message = input('Type here:')
    print(user_message)
    if user_message.strip().lower() in ['exit','quit','bye']:
        break
    
    config = {'configurable':{'thread_id': thread_id}}
    response = chatbot.invoke({'messages':[HumanMessage(content=user_message)]}, config=config)
    print("AI:", response['messages'][-1].content)