from langgraph.graph import StateGraph , START,END
from langchain_ollama import ChatOllama


from dotenv import load_dotenv
from typing import TypedDict,Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
model = ChatOllama(model="qwen2.5:3b", temperature=0.7, num_predict=256)

class sentimentsechma (BaseModel):
    sentiment : Literal["positive" , "negative"] = Field(description='sentimant of the review')


prompt = ChatPromptTemplate.from_template("""
Analyze the sentiment of the following review.

Return ONLY valid JSON.

Format:
{{
    "sentiment": "positive"
}}

Review:
{text}
""")


structured_model = model.with_structured_output(sentimentsechma)

chain = prompt | structured_model

result = chain.invoke({
    "text": "The product is too bad"
})

class reviewstate(TypedDict):
    review : str
    sentiment : Literal["positive" , "negative"]
    diagnosis : dict
    response : str

def find_sentimant(state : reviewstate):
    sentiment = chain.invoke({"text": state["review"]}).sentiment
    return {"sentiment": sentiment}

graph = StateGraph(reviewstate)

graph.add_node('find_sentimant',find_sentimant)
graph.add_edge(START, 'find_sentimant')
graph.add_edge('find_sentimant', END)

workflow = graph.compile()

print(result.sentiment)
print(workflow.invoke({'review': 'The delivery was fast and the quality is amazing'}))