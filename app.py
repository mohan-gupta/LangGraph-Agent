import streamlit as st

from src.agent import Agent

agent = Agent()
    

st.title('LangGraph Agent')
st.html("<p>This Agent will assist with weather related query.<br>It will also assist you with Transformer based models like BERT, GPT and T5 related doubts.</p>")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# React to user input
if prompt := st.chat_input("Hi, how can I help you"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Display assistant response in chat message container
    agent_response = agent.run(prompt)
    response = f"Agent: {agent_response}"

    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})