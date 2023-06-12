# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 19:39:54 2023

@author: Mahir Navid
"""

"""
Created on Mon Jun  5 21:40:42 2023

@author: Mahir Navid
"""
import openai
import os
import argparse

parser = argparse.ArgumentParser(description='Import API KEY')
parser.add_argument('api_key_file', type=str, help='Path to the API key file')
parser.add_argument('--enable_api', action='store_true', help='Enable the OpenAI API call')

args = parser.parse_args()

api_key_file = os.path.abspath(args.api_key_file)

with open(api_key_file, 'r') as f:
    api_key = f.read().strip()

print('API Key read from file:', api_key)  # Debug print

openai.api_key = api_key  # Set the API key

print('API Key set for OpenAI')  # Debug print

# Prepare prompt
prompt = "I love you, say it back."

# Check if the OpenAI API should be called
if args.enable_api:
    print('Calling OpenAI API...')  # Debug print
    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=50
    )

    print('API call completed.')  # Debug print
    print(response['choices'][0]['text'])
else:
    print("OpenAI API call disabled by default. Use the '--enable_api' flag to enable.")
    








