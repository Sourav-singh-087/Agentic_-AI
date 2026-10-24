from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

model = ChatOllama(model="qwen2.5:3b", temperature=0.7, num_predict=256)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}


# Short-term memory (stored in RAM, lost when the program exits)
checkpointer = MemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

initial_state ={
    'messages' : [HumanMessage(content='what is capital of west bengal')]

}
response = chatbot.invoke(initial_state, config={"configurable": {"thread_id": "chat-1"}})
print(response)