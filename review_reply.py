from langgraph.graph import StateGraph , START,END
from langchain_huggingface import ChatHuggingFace , HuggingFaceEmbeddings  , HuggingFaceEndpoint


from dotenv import load_dotenv
from typing import TypedDict,Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    max_new_tokens=256,
    temperature=0.7
)
model = ChatHuggingFace(llm = llm)

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


chain = prompt | model

result = chain.invoke({
    "text": "The product is too bad"
})

class reviewstate(TypedDict):
    review : str
    sentiment : Literal["positive" , "negative"]
    diagnosis : dict
    response : str

def find_sentimant(state : reviewstate):
    prompt = f''
    sentiment = chain.invoke(prompt).sentiment

graph = StateGraph(reviewstate)

graph.add_node('find_sentimant',find_sentimant)

print(result.content)