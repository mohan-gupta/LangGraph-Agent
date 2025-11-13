from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from src.cfg import gemini_api_key
from src.llm_stack import llm
from src.weather_api import get_weather_data
from src.db_ops import vector_search


class Location(TypedDict):
    location: str

class QueryType(TypedDict):
    query_type: Literal["weather", "rag", "invalid"]

class State(TypedDict):
    query: str
    query_type: QueryType|None
    
    response: str

    
class Agent:
    def __init__(self):
        self.builder = StateGraph(State)
        self.create_graph()
        self.graph = self.builder.compile()
    
    def create_graph(self):
        self.builder.add_node("classify", self.classify_node)
        self.builder.add_node("weather", self.weather_node)
        self.builder.add_node("rag", self.rag_node)
        self.builder.add_node("invalid", self.check_node)

        self.builder.add_edge(START, "classify")
        self.builder.add_edge("weather", END)
        self.builder.add_edge("rag", END)
        self.builder.add_edge("invalid", END)
        self.builder.add_conditional_edges("classify", self.conditional_edge)
    
    def run(self, query: str):
        initial_state = State(query=query)
    
        response = self.graph.invoke(initial_state)
        
        return response["response"]

    def classify_node(self, state: State) -> State:
        """classify user query: weather related or rag query"""
        
        structured_llm = llm.with_structured_output(QueryType)

        classification_prompt = f"""
        Analyze the user query and classify it:
        if query is related to weather, then classify it as weather.
        if query is related to bert, gpt, transformers or t5 models/architecture details and topics, then classify it as rag
        otherwise invalid

        query: {state['query']}

        Provide classification for the user query.
        """
        
        classification = structured_llm.invoke(classification_prompt)

        # Store classification as a single dict in state
        return State(query_type=classification["query_type"])

    def weather_node(self, state: State) -> State:
        """get requested weather data"""
        structured_llm = llm.with_structured_output(Location)

        location_prompt = f"""
        Identify the location name from the user query:

        query: {state['query']}

        Provide the location name in lowercase.
        """
        
        location = structured_llm.invoke(location_prompt)
        
        weather_response = get_weather_data(location["location"])
        
        weather_prompt = f"""
        Answer the user query, using the provided location data.
        query: {state["query"]}
        
        location_data: {weather_response}
        """
        
        response = llm.invoke(weather_prompt)
        
        return State(response=response.content)

    def rag_node(self, state: State) -> State:
        """get requested context"""
        query = state["query"]
        context = vector_search(query)
        
        rag_prompt = f"""
        Answer the user query, using the provided context.
        query: {state["query"]}
        
        context: {context}
        """
        
        response = llm.invoke(rag_prompt)
        
        return State(response=response.content)

    def check_node(self, state: State) -> State:
        """send message to try weather or rag document related query"""
        prompt = f"""
        If user greets or thanks you, then greet the user, otherwise tell them that you can only help them with weather related or Transformer models related queries.
        
        user query: {state["query"]}
        """
        response = llm.invoke(prompt)
        
        return State(response=response.content)

    def conditional_edge(self, state: State) -> Literal["weather", "rag", "invalid"]:
        query_type = state["query_type"]
        
        return query_type
    


if __name__ == "__main__":
    # from PIL import Image
    # import io

    # def save_graph_image(graph: StateGraph):
    #     "Function to save graph image"
    #     graph_png = graph.get_graph().draw_mermaid_png()
    #     byte_stream = io.BytesIO(graph_png)
    #     img = Image.open(byte_stream)

    #     img.save("graph.png")
    # agent = Agent()
    # save_graph_image(agent.graph)
    
    user_query = "who is Tom cruise?"
    agent = Agent()
    response = agent.run(query=user_query)
    print(response)