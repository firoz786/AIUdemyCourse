from langchain.agents import create_agent

from model import model


agent = create_agent(
    model=model,
    tools=[]
)
