import pytest

from src.agent import Agent, State
from src.weather_api import get_weather_data
from src.db_ops import vector_search

@pytest.fixture
def my_agent():
    return Agent()

def test_classify_node(my_agent):
    weather_query = State(query="What is the weather in Finland?")
    data_query = State(query="What is the embedding size in GPT")
    invalid_query = State(query="What is the current price of ETH")
    
    weather_response = my_agent.classify_node(weather_query)
    assert weather_response["query_type"] == "weather"
    
    data_response = my_agent.classify_node(data_query)
    assert data_response["query_type"] == "rag"
    
    invalid_response = my_agent.classify_node(invalid_query)
    assert invalid_response["query_type"] == "invalid"
    

def test_weather_api():
    location = "Norway"
    response = get_weather_data(location)
    
    assert isinstance(response, dict)
    
def test_vector_search():
    query = "What is the embedding size in GPT"
    response = vector_search(query)
    
    assert len(response) > 0


def test_weather_node(my_agent):
    weather_query = State(query="What is the weather in Finland?")
    
    weather_response = my_agent.weather_node(weather_query)
    assert isinstance(weather_response["response"], str)
    
def test_rag_node(my_agent):
    data_query = State(query="What is the embedding size in GPT")
    
    data_response = my_agent.rag_node(data_query)
    assert isinstance(data_response["response"], str)