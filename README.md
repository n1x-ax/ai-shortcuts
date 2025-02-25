Since the latest public releases of SOTA language models, we've seen an exponential growth of new human-machine interactions - prompt engineering. And yet, not everyone is ready to learn how to talk to AI models, instruct them to complete simple tasks, and even more - try to replace work processes using LLMs. This thought became a foundation for AI Shortcuts.

## Introduction

AI Shortcuts empower users to bypass the complexities of prompt engineering by offering pre-designed tools for fast task execution and content generation. These customizable shortcuts simplify interactions with language models, enabling efficiency without mastering AI instructions. Leveraging zero-shot capabilities, users can achieve accurate results without prior examples or extensive input.

When integrated into software, they provide a seamless and intuitive way to execute tasks with minimal input, making AI-driven productivity effortless. This simplicity is a crucial aspect of UX in software development, ensuring users can harness AI capabilities without friction, transforming complex processes into intuitive experiences.

## Getting Started

### Install `openai` and `python-dotenv` Libraries

```
pip install openai python-dotenv
```

### Create a `.env` file:

This file should contain your OpenAI API key:

`OPENAI_API_KEY=your_openai_api_key_here`

## 1. Simple Shortcut Execution Using User Input

### Technical Overview:

Here is a straightforward application that leverages OpenAI's API to generate content based on user inputs. It demonstrates how to collect user data and construct a prompt dynamically, which is then used to generate a TikTok video script. This script highlights the ease of integrating AI into various software workflows without bypassing user's prompt engineering need while collecting personal input.

### Key Components:

- **User Input Collection:** Prompts the user for aesthetic style and video topic.

- **Dynamic Prompt Construction:** Uses the collected inputs to create a detailed prompt for the AI model.

- **API Interaction:** Sends the prompt to OpenAI's API and retrieves the generated script.

```python
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
```

```
shortcut.py

1. Aesthetic Style: J-Pop         
2. Video Topic: Style in Japan

**[TikTok Video Script: "Style in Japan: A Journey Through J-Pop Aesthetics"]**

**[INTRO]**  
**[Visuals: A fast-paced montage of vibrant Tokyo streets, bustling Harajuku fashion scenes, and artists performing pop music. The screen flashes colorful text: "Style in Japan: J-Pop Aesthetic!"]**  
**Voiceover:**  
"Hey, TikTok! Today, we’re diving into the vibrant world of J-Pop fashion! 🇯🇵✨ Join me as we explore the colorful styles that make Japan a fashion powerhouse!"
–––
**[Segment 1: History of J-Pop Fashion]**  
**[Visuals: Clips of iconic J-Pop artists from the past decades, such as Namie Amuro, Kyari Pamu Pamu, and Arashi, performing on stage.]**  
**Voiceover:**  
"First, let’s take a quick look back. J-Pop emerged in the late 1980s and exploded in the 90s, blending Western pop influences with unique Japanese culture. Artists like Namie Amuro and Hikaru Utada set the stage for what we now call J-Pop fashion!"

...
```

This method can be applied in various software applications within proper pipelines.

## 2. Shortcut Generator

### Technical Overview:

The shortcut generator automates the creation of prompts by analyzing user needs and generating a structured JSON object. This script is ideal for applications where custom AI functions needed to be created on user's side without a need in prompt-engineering or any other efforts, except providing an information about task needed to be complete.

### Key Components:
- **Initial User Input:** Collects a description of the desired shortcut.

- **JSON Object Generation:** Uses OpenAI's API to generate a JSON object containing input hints, subject, and a prompt template.

- **Dynamic Prompt Execution:** Collects user inputs based on generated hints and constructs the final prompt for execution.

```python
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
```

```
shortcut_gen.py

Please describe your shortcut: Poem

Subject:
Creating a poem

Prompt:
Compose a poem that explores the theme of '{input_1}', using a '{input_2}' style, maintaining a length of '{input_3}' lines, evoking '{input_4}' emotions, suitable for an '{input_5}' audience.

Inputs:
['theme', 'style', 'length', 'emotion', 'audience']

1. theme: Rainy Season
2. style: Any
3. length: 3 blocks
4. emotion: High
5. audience: Me

**Rainy Season**

In the hush of dawn, the world exhales,  
Silver droplets weave like whispered tales,  
Each beat a promise, a lover's refrain.  

Clouds gather close, a shroud of gray,  
They drench the earth in a tender ballet,  
Every splash, a memory, igniting the pain.  

We dance in puddles, heartbeats collide,  
Nature's embrace, where sorrows subside,  
In the storm's wild rhythm, we find our gain.
```

After we started `shortcut_gen.py` and provided information about our shortcut - in our case it was "Poem", we can see that it's generated a subject, prompt, and inputs, that was used for future questions' collection to generate poem.

## 3. Shortcut to CSV Process
### Technical Overview:

The `shortcut-to-csv.py` script facilitates the generation of CSV files by transforming user inputs into a structured format. This script is particularly useful for creating data outputs like invoices, leveraging AI to format and organize information without manual prompt engineering.

### Key Components:

- **User Input Collection:** Gathers necessary data for the CSV, such as company and client names, item details, and payment terms.

- **CSV Structure Generation:** Uses OpenAI's API to create a creatively designed CSV layout based on the inputs.

- **File Output:** Writes the generated CSV content to a file for easy access and use.

```python
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
    "Company Name",
    "Client Name",
    "Number of Items",
    "Payment Days",
    "Total Amount",
    "List of Items/Services/Products"
]

# Define the subject of the invoice
subject = "Professional invoice"

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
- For tasks like project management, calendar generation, or invoices, make sure to put information as one per cell, to avoid single column CSVs.
- Make sure to avoid separating sentences or numbers between cells, keep it consistent.
- Provide CSV structure only, without '```csv'.
"""

# Construct the user prompt for generating the CSV
prompt = f"""Generate a CSV invoice for {user_inputs['input_1']} billed to {user_inputs['input_2']}. The invoice should include {user_inputs['input_3']} item(s), payment terms of Net {user_inputs['input_4']} days, a total amount of {user_inputs['input_5']}, and the following items/services/products: {user_inputs['input_6']}."""

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
print(f"Dynamic CSV file has been written to {csv_file_path}")
```

<img width="645" alt="Screenshot 2025-02-25 at 15 49 28" src="https://github.com/user-attachments/assets/13e4a989-dc56-44af-a352-9ffb42e59f8e" />

## 4. Shortcut to JSON Process
### Technical Overview:
The `shortcut_to_json.py` script is designed to convert project information into a structured JSON format, making it ideal for generating pre-made workflows. This script simplifies the process of creating JSON outputs, which can be used for various applications, such as project management or data analysis.

### Key Components:
- **User Input Collection:** Gathers project-related information from the user.

- **JSON Structure Generation:** Uses OpenAI's API to create a JSON object with fields like title, description, objectives, and team members.

- **Output Display:** Prints the generated JSON content for easy integration into workflows.

```python
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('.env.local')

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define input prompts
input_hints = [
    "Information about the Project"
]

# Collect user inputs
user_inputs = {}
for i, prompt in enumerate(input_hints, start=1):
    user_input = input(f"{i}. {prompt}: ")
    user_inputs[f"input_{i}"] = user_input

# Construct the prompt to request CSV format directly
system_prompt = f"""
Review the provided project information to identify its subject, direction, key objectives, and context.
Then, generate the following:
Title: A short (2-3 words) project title.
Description: A one-sentence summary of the project's main focus.
Objectives: Up to three clear objectives.
Team Members: Up to three significant roles in the project with descriptions.
Emoji: An emoji representing the project.
Output Format: Provide a JSON array with one object containing the fields: title, description, objectives, team_members, abd emoji.
"""

prompt = f"""
Information about the Project: {user_inputs['input_1']}
"""

# a ChatCompletion request
response = client.beta.chat.completions.parse(
    model='gpt-4o-mini',
    messages=[
        {'role': 'assistant', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ],
    temperature=0.8,
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "project_summary",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "objectives": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "team_members": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {"type": "string"},
                                "description": {"type": "string"}
                            },
                            "required": ["role", "description"],
                            "additionalProperties": False
                        }
                    },
                    "emoji": {"type": "string"}
                },
                "required": ["title", "description", "objectives", "team_members", "emoji"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

print(response.choices[0].message.content)
```

```
shortcut_to_json.py

1. Information about the Project: We are building an AI shortcut library

Response:
{
  "title":"AI Shortcut Library",
  "description":"Development of a comprehensive library designed to provide AI shortcuts for enhanced productivity.",
  "objectives":[
    "Create a user-friendly interface for accessing AI shortcuts.",
    "Develop a diverse range of AI shortcuts for various applications.",
    "Ensure thorough documentation and support for users."
  ],
  "team_members":[
    {
      "role":"Project Manager",
      "description":"Oversees project development and coordination among team members."
    },
    {
      "role":"AI Developer",
      "description":"Responsible for creating and testing AI shortcuts."
    },
    {
      "role":"UI/UX Designer",
      "description":"Designs the interface to ensure ease of use and accessibility."
    }
  ],
  "emoji":"🤖"
}
```

## Conclusion
AI Shortcuts provide a powerful way to simplify interactions with language models, making advanced AI capabilities accessible to users without technical expertise. By automating prompt generation and content creation, these shortcuts enable efficient task execution and data generation, transforming complex processes into intuitive experiences. Whether generating scripts, CSVs, or JSON outputs, AI Shortcuts offer a seamless and user-friendly approach to leveraging AI in everyday applications.
