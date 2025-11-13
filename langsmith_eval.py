from dotenv import load_dotenv

import json

from pydantic import BaseModel, Field

from langsmith import Client
from langsmith import evaluate

from src.llm_stack import llm
from src.agent import Agent

load_dotenv()

client = Client()

dataset_name = "agent-eval-dataset"

def create_dataset(dataset_name):
    if client.has_dataset(dataset_name=dataset_name):
        return
    
    dataset = client.create_dataset(dataset_name=dataset_name)
    
    with open("eval_dataset.json") as f:
        examples = json.load(f)
    
    client.create_examples(dataset_id=dataset.id, examples=examples)


# Define a scoring schema that our LLM must adhere to
class CorrectnessScore(BaseModel):
    """Correctness score of the answer when compared to the reference answer."""
    score: int = Field(description="The score of the correctness of the answer, from 0 to 1")


def correctness(inputs: dict, outputs: dict, reference_outputs: dict) -> bool:
    prompt = f"""
    You are an expert data labeler evaluating model outputs for correctness. Your task is to assign a score based on the following rubric:

    <Rubric>
        A correct answer:
        - Provides accurate information
        - Uses suitable analogies and examples
        - Contains no factual errors
        - Is logically consistent

        When scoring, you should penalize:
        - Factual errors
        - Incoherent analogies and examples
        - Logical inconsistencies
    </Rubric>

    <Instructions>
        - Carefully read the input and output
        - Use the reference output to determine if the model output contains errors
        - Focus whether the model output uses accurate analogies and is logically consistent
    </Instructions>

    <Reminder>
        The analogies in the output do not need to match the reference output exactly. Focus on logical consistency.
    </Reminder>

    <input>
        {inputs["query"]}
    </input>

    <output>
        {outputs["output"]}
    </output>

    Use the reference outputs below to help you evaluate the correctness of the response:
    <reference_outputs>
        {reference_outputs["response"]}
    </reference_outputs>
    """
    
    structured_llm = llm.with_structured_output(CorrectnessScore)
    generation = structured_llm.invoke(prompt)
    return generation.score == 1

def run(inputs: dict):
    agent = Agent()
    response = agent.run(inputs["query"])
    return response


evaluate(
    run,
    data=dataset_name,
    evaluators=[correctness],
    experiment_prefix="weather-tech-agent"
)