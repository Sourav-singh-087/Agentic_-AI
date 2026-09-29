from langgraph.graph import StateGraph,START,END
from typing import Literal, TypedDict


class quadstate(TypedDict):
    a : int
    b : int
    c : int

    equation : str
    discriminant : float
    result : str

def show_equation(state : quadstate) :
    equation = f'{state["a"]}x2{state["b"]}x{state["c"]}'

    return{'equation': equation}

def calculate_discriminant(state : quadstate):
    discriminant = state["b"]**2 - (4*state["a"]*state["c"])

    return {'discriminant': discriminant}

def real_root(state : quadstate):
    root1 = (-state["b"] + state["discriminant"]**0.5) /(2*state["a"])
    root2 = (-state["b"] - state["discriminant"]**0.5) /(2*state["a"])

    result = f'the two roots are {root1} and {root2}'

    return{'result': result}

def repeated_root(state : quadstate):
    root = (-state["b"]) /(2*state["a"])
    
    result = f'the repeated_roots are {root} '

    return{'result': result}

def no_root(state : quadstate):
    
    result = f'there are no real roots '

    return{'result': result}

def check_condition(state : quadstate) -> Literal["real_root","repeated_root","no_root"]:
    if(state['discriminant'] > 0) :
        return "real_root"
    elif(state['discriminant'] == 0):
        return"repeated_root"
    else :
        return"no_root"
    


graph = StateGraph(quadstate) 

graph.add_node('show_equation',show_equation)
graph.add_node('calculate_discriminant',calculate_discriminant)
graph.add_node('real_root',real_root)
graph.add_node('repeated_root',repeated_root)
graph.add_node('no_root',no_root)


graph.add_edge(START,'show_equation')
graph.add_edge('show_equation','calculate_discriminant')
graph.add_conditional_edges('calculate_discriminant' ,check_condition)
graph.add_edge('real_root',END)
graph.add_edge('repeated_root',END)
graph.add_edge('no_root',END)


workflow = graph.compile()

initial_state = {
    'a' : +4,
    'b' : +5,
    'c' : 0
}
print(workflow.invoke(initial_state))
