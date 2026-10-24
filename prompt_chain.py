from langgraph.graph import StateGraph , START,END
from langchain_ollama import ChatOllama


from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()
model = ChatOllama(model="qwen2.5:3b", temperature=0.7, num_predict=256)

class BlogState(TypedDict):
    content : str
    outline : str
    title : str

def create_outline(state : BlogState) -> BlogState:
    title = state['title']

    prompt = f'generate a detail blog on this {title}'
    outline = model.invoke(prompt).content
    state ['outline'] = outline
    return state

def create_blog(state : BlogState) -> BlogState:
    title = state['title']
    outline = state['outline']

    prompt = f'write a detail blog on the {title} using the following outline\n {outline} '
    content = model.invoke(prompt).content
    state['content'] = content
    return state

graph = StateGraph(BlogState)

graph.add_node('create_outline' ,create_outline )
graph.add_node('create_blog' ,create_blog )

graph.add_edge(START,'create_outline')
graph.add_edge('create_outline','create_blog')
graph.add_edge('create_blog',END)

workflow = graph.compile()

inital_state = {'title' :'rise of ai in india'}
final_state = workflow.invoke(inital_state)

print(final_state)
