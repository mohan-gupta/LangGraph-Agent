import streamlit as st

from src.agent import Agent

agent = Agent()
    

st.title('LangGraph Agent')
st.write("This Agent will assist with weather related query.")
st.write("It will also assist you with Transformer based models like BERT, GPT and T5 related doubts.")

prompt = st.chat_input("Hi, how can I assist you")
if prompt:
    st.write(f"User: {prompt}")
    agent_response = agent.run(prompt)
    st.write(f"Agent: {agent_response}")
