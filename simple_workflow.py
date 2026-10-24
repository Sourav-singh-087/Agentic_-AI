from langgraph.graph import StateGraph , START,END
from langchain_ollama import ChatOllama


from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()
model = ChatOllama(model="qwen2.5:3b", temperature=0.7, num_predict=256)

#create a state 

class LLMstate(TypedDict):
    question:str
    answer:str

def llm_qr(state : LLMstate) -> LLMstate:
    question = state['question']
    prompt = f'Answer the following {question}'
    answer = model.invoke(prompt).content
    state ['answer'] = answer
    return state


graph = StateGraph(LLMstate)
graph.add_node('llm_qr', llm_qr)
graph.add_edge(START,'llm_qr')
graph.add_edge('llm_qr' ,END)

workflow = graph.compile()

inital_state = {'question' : 'how far is moon from earth'}

final_state = workflow.invoke(inital_state)

print(final_state)
