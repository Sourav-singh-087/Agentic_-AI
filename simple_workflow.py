from langgraph.graph import StateGraph , START,END
from langchain_huggingface import ChatHuggingFace , HuggingFaceEmbeddings  , HuggingFaceEndpoint


from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    max_new_tokens=256,
    temperature=0.7
)
model = ChatHuggingFace(llm = llm)

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
