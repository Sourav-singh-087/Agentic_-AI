from langgraph.graph import StateGraph,START,END
from typing import TypedDict

class cricketBlog(TypedDict):
    runs : int
    balls : int 
    fours : int
    sixes : int

    sr : float
    bpb : float
    bp : float
    summary:str

def calculate_sr(state : cricketBlog):
    sr = (state['runs'] / state['balls'] )*100
    
    return {'sr' : sr}
def calculate_bpb(state : cricketBlog):
    bpb = (state['balls'] / state['fours']+state['sixes'] )
    
    return {'bpb' : bpb}
def calculate_bp(state : cricketBlog):
    bp = ((state['fours']*4)+(state['sixes']*6) / state['runs'])
    
    return {'bp' : bp}
def summary(state : cricketBlog):
    summary = f""""
    Strike rate - {state['sr']}\n
    balls per boundary - {state['bpb']}\n
    boundary percentage - {state['bp']}

    """
    
    return {'summary' : summary}


graph = StateGraph(cricketBlog)

graph.add_node("calculate_sr",calculate_sr)
graph.add_node("calculate_bpb",calculate_bpb)
graph.add_node("calculate_bp",calculate_bp)
graph.add_node("summary",summary)

graph.add_edge(START,"calculate_sr")
graph.add_edge(START,"calculate_bpb")
graph.add_edge(START,"calculate_bp")

graph.add_edge("calculate_sr","summary")
graph.add_edge("calculate_bpb","summary")
graph.add_edge("calculate_bp","summary")

graph.add_edge("summary",END)

workflow = graph.compile()

print(workflow)

inital_state = {
    'runs' : 100,
    'balls' : 50,
    'sixes' : 6,
    'fours' : 4
}
print(workflow.invoke(inital_state))