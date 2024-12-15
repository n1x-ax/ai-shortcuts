import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from collections.abc import MutableMapping
from enum import Enum

# Load environment variables from a local .env file
load_dotenv('.env.local')

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Function to flatten nested JSON structures into a single level dictionary
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, MutableMapping):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '_')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Define a list of input prompts for user data collection
input_prompts = [
    "Project Name",
    "Project Manager",
    "Number of Team Members",
    "Project Duration (days)",
    "List of Key Milestones"
]

# Define the subject of the project management document
subject = "Development Project Management and Schedule"

# Collect user inputs based on the defined prompts
user_inputs = {}
for i, prompt in enumerate(input_prompts, start=1):
    user_input = input(f"{i}. {prompt}: ")
    user_inputs[f"input_{i}"] = user_input

# System prompt to guide the AI in generating a CSV structure
system_prompt = f"""
You are a utility that generates a creatively designed CSV for "{subject}" using user inputs.
- Ensure the CSV is structured, accessible, and easy to read.
- Use creative layout with headers, subheaders, and ASCII symbols.
- Group related information logically, using spacing for readability.
- Keep the CSV compact in width, utilizing height for design.
- For tasks like project management, calendar generation, or invoices, make sure to format information properly, to avoid single column CSVs or complet ASCII within one cell.
- Make sure to avoid separating sentences or numbers between cells, keep it consistent.
- Provide CSV structure only, without '```csv'.
"""

# Construct the user prompt for generating the CSV
prompt = f"""Generate a CSV schedule for the project "{user_inputs['input_1']}" managed by {user_inputs['input_2']}. The project involves {user_inputs['input_3']} team member(s), spans {user_inputs['input_4']} days, and includes the following key milestones: {user_inputs['input_5']}."""

# Request the AI to generate the CSV structure
structure_completion = client.beta.chat.completions.parse(
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt},
    ],
    response_format={ "type": "text" },  # Specify the response format as text
)

# Extract the generated CSV content from the AI's response
csv_content = structure_completion.choices[0].message.content

# Write the CSV content to a file
csv_file_path = 'output.csv'
with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_file.write(csv_content)

# Notify the user that the CSV file has been created
print(f"CSV file has been written to {csv_file_path}")