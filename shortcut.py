import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('.env.local')

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define input prompts
input_hints = [
    "Aesthetic Style",
    "Video Topic"
]

# Define the subject of CSV
subject = "Professional invoice"

# Collect user inputs
user_inputs = {}
for i, prompt in enumerate(input_hints, start=1):
    user_input = input(f"{i}. {prompt}: ")
    user_inputs[f"input_{i}"] = user_input

# Construct the prompt to request CSV format directly
prompt = f"""
Produce a script for a TikTok video that centers around {user_inputs['input_2']}, utilizing a {user_inputs['input_1']} aesthetic.

Your script should encompass an introduction, visuals, voiceovers, and a conclusion.

Additionally, offer insights or advice related to the subject matter. Your response should be thorough and detailed."""

# a ChatCompletion request
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'user', 'content': prompt}
    ],
    temperature=0.8
)

print(response.choices[0].message.content)