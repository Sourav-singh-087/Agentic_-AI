from langgraph.graph import StateGraph , START,END
from langchain_huggingface import ChatHuggingFace , HuggingFaceEmbeddings  , HuggingFaceEndpoint
from pydantic import BaseModel,Field

from dotenv import load_dotenv
from typing import TypedDict,Annotated
import operator

load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-8B",
    task="text-generation",
    max_new_tokens=256,
    temperature=0.7
)
model = ChatHuggingFace(llm = llm)

class evalutionsechma(BaseModel):
    feedback : str = Field(description='detailed feedback for the essay')
    score : int = Field(description='score out of 10', ge=0,le=10)

structured_model = model.with_structured_output(
    evalutionsechma,
    method="json_mode"
)

essay = """"
# The Role of India in the AI Revolution

Artificial Intelligence (AI) is transforming the modern world by changing how people work, learn, communicate, and solve problems. Its applications range from healthcare and agriculture to finance, education, transportation, and governance. As AI becomes increasingly important to economic and social development, India is emerging as a significant participant in this global technological shift.

One of India's greatest strengths is its large pool of skilled professionals and students in engineering, computer science, mathematics, and related fields. The country's established IT industry provides a strong foundation for developing and adopting AI technologies. Major technology companies are using AI to improve software development, data analysis, cybersecurity, customer support, and business operations. At the same time, startups are creating solutions designed for India's unique economic and social needs.

The Indian government has also taken steps to encourage AI development. Initiatives such as the IndiaAI Mission focus on areas including computing infrastructure, innovation, skill development, and responsible AI adoption. These efforts can help create an environment where researchers, businesses, and entrepreneurs can develop practical AI applications.

AI has consider
"""
prompt = f'Evaluate the language quality of the following essay and provide a feedback and assign a score out of 10 \n {essay}'
response = structured_model.invoke(prompt)
print(response)
class UPSCState(TypedDict):

    essay: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_scores: Annotated[list[int], operator.add]
    avg_score: float

def evalute_language(state : UPSCState):
    prompt = f'Evaluate the language quality of the following essay and provide a feedback and assign a score out of 10 \n {state ["essay"]}'
    output = structured_model.invoke(prompt)

    return{'language_feedback' : output.feedback , 'individual_scores' : [output.score]}

def evalute_analysis(state : UPSCState):
    prompt = f'Evaluate the depth of analysis of the following essay and provide a feedback and assign a score out of 10 \n {state ["essay"]}'
    output = structured_model.invoke(prompt)

    return{'analysis_feedback' : output.feedback , 'individual_scores' : [output.score]}

def evalute_clarity(state : UPSCState):
    prompt = f'Evaluate the clarity of though of the following essay and provide a feedback and assign a score out of 10 \n {state ["essay"]}'
    output = structured_model.invoke(prompt)

    return{'clarity_feedback' : output.feedback , 'individual_scores' : [output.score]}

def final_evaluation(state: UPSCState):

    # summary feedback
    prompt = f'Based on the following feedbacks create a summarized feedback \n language feedback - {state["language_feedback"]} \n depth of analysis feedback - {state["analysis_feedback"]} \n clarity of thought feedback - {state["clarity_feedback"]}'
    overall_feedback = model.invoke(prompt).content

    # avg calculate
    avg_score = sum(state['individual_scores'])/len(state['individual_scores'])

    return {'overall_feedback': overall_feedback, 'avg_score': avg_score}
    

graph = StateGraph(UPSCState)

graph.add_node('evalute_analysis',evalute_analysis)
graph.add_node('evalute_language',evalute_language)
graph.add_node('evalute_clarity',evalute_clarity)
graph.add_node('final_evaluation',final_evaluation)

graph.add_edge(START,'evalute_analysis')
graph.add_edge(START,'evalute_language')
graph.add_edge(START,'evalute_clarity')

graph.add_edge('evalute_analysis','final_evaluation')
graph.add_edge('evalute_language','final_evaluation')
graph.add_edge('evalute_clarity','final_evaluation')

graph.add_edge('final_evaluation',END)

workflow = graph.compile()

inital_state = {
    'essay': essay,
    'individual_scores': []
}

print(workflow.invoke(inital_state))