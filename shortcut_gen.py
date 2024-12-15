import os
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('.env.local')

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Collect initial user input
initial_input = input("Please describe your shortcut: ")

example = r"""Develop an output that centers around '{input_2}', using a '{input_1}', approach, while incorporating '{input_3}', and '{input_4}'."""

# Generate JSON object with input prompts, subject, and prompt
initial_prompt = f"""
As a professional prompt engineer, your task is to generate detailed instructions for provided task.
First, analyze user's needs, subject, and identify main inputs for task, that should be used uppon completion.
This subjects will be a foundation for prompt inputs, that will be answered by user.
You need to define this inputs within a prompt that way, so user can answer questions about them using generated hints.
This hints should be provided within "input_hints", 5 hints maximum. It's a short input titles up to 3 words.
Subject is main description of current task based on user's input.
Prompt example: {example}. 
Use the following structure:
{{
    "input_hints": ["prompt1", "prompt2", ...],
    "subject": "subject of CSV",
    "prompt": "prompt for chat completion with placeholders like {{input_1}}"
}}
Your respinse should be a JSON format only.
"""

# First ChatCompletion request to generate JSON object
initial_response = client.beta.chat.completions.parse(
    model='gpt-4o-mini',
    messages=[
        {'role': 'assistant', 'content': initial_prompt},
        {'role': 'user', 'content': initial_input}
    ],
    temperature=0.8,
    response_format={ "type": "json_object" }
)

# Parse the generated JSON object
generated_json = json.loads(initial_response.choices[0].message.content)

# Extract input prompts and subject from the JSON object
input_hints = generated_json['input_hints']
subject = generated_json['subject']
prompt_template = generated_json['prompt']

print("Subject:")
print(subject)
print("Prompt:")
print(prompt_template)
print("Inputs:")
print(input_hints)
print("Please provide information:")

# Collect user inputs based on generated prompts
user_inputs = {}
for i, prompt in enumerate(input_hints, start=1):
    user_input = input(f"{i}. {prompt}: ")
    user_inputs[f"input_{i}"] = user_input

# Ensure user_inputs is populated before using it
if not user_inputs:
    raise ValueError("User inputs were not collected properly.")

# Check if all expected keys are in user_inputs
expected_keys = [f"input_{i}" for i in range(1, 6)]  # Expecting 5 inputs
missing_keys = [key for key in expected_keys if key not in user_inputs]

if missing_keys:
    raise KeyError(f"Missing user inputs for keys: {missing_keys}")

# Construct the final prompt using the template and user inputs
try:
    final_prompt = prompt_template.format(**user_inputs)
except KeyError as e:
    raise KeyError(f"Missing key in user_inputs: {e}")

# a ChatCompletion request
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'user', 'content': final_prompt}
    ],
    temperature=0.8
)

print(response.choices[0].message.content)