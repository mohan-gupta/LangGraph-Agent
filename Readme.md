# LangGraph Agent

This agent, helps you with weather related queries, and it also helps you with queries related to technical topics like Transformers, BERT, GPT and T5 models.<br><br>

This agent is desigend using LangGraph, Qdrant and Google Gemini models.<br>

To run this agent in your local machine, follow these steps:
1. <b>Set-up the .env file</b>
   ```bash
    GEMINI_API_KEY=<your google gemini api key>

    WEATHER_API_KEY=<your open weather map api key>

    QDRANT_API_KEY=<qdrant api key>
    QDRANT_CLUSTER_URL=<qdrant cluster url>
   ```
2. <b>Set-up the environment,</b> for environment setup I have used [uv](https://docs.astral.sh/uv/guides/install-python/)
   ```bash
    # langgraph supports python>=3.11
    uv venv --python 3.12

    # for windows:
    .venv\Scripts\activate

    # for mac:
    source .venv/bin/activate

    # install dependencies
    uv pip install -r requirements.txt
   ```
3. <b>load your env variables:</b>
   In the ```cfg.py``` file, I have loaded the environment variables.

4. <b>llm_stack.py:</b> In this file, I have instantiated the llm and embedding model.

5. <b>weather_api.py:</b> In this file, I have defined the function to fetch weather details for a location.

6. <b>set-up the VectorDB:</b>
   - In the documents folder, add the pdf files on which you want to perform RAG.
   - I have added Transformers, BERT, GPT, and T5 paper pdfs.
   - I have used RecursiveCharacterTextSplitter for creating document chunks.
   - and "models/gemini-embedding-001" model for creating the embeddings.
  
    ```bash
    # First run db_ops.py file to set up the VectorDB
    db_ops.py

    #Then, run the pdf_pipeline.py file to create chunks, chunk embeddings, and this file will upload the embeddings to our vectordb.
    pdf_pipeline.py
    ```
7. <b>agent.py</b>: This file contains the LangGraph Agent<br>
   <img src="assets/graph.png"><br><br>
   - First the user query goes through ```classify node```, this node will send the query into any one of the next 3 nodes based on the query classification.
   - for e.g., a query like: "What is the weather in Finland?", will go through the ```weather node```.
   - and a query like: "What is the embedding size of BERT model?", will go through the ```rag node```.