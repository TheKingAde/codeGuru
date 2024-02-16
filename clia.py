#!/usr/bin/python
import sys
import os
import google.generativeai as palm
import subprocess
"""
CLIA - Command Line Interface Assistant

This module provides a Python script that leverages the Google PaLM (Probabilistic and Logical Modeling) API to generate text responses based on user input or content provided in files. It offers both command-line and interactive modes for convenient use.

Usage:
    - Run the script with command-line arguments to specify input files and optional instructions.
    - Launch interactive mode to ask questions and receive text responses.

Requirements:
    - Python 3.x
    - `google.generativeai` package
    - [Google PaLM API key](https://cloud.google.com/pa-lm/docs/quickstart)

Author: Meffun Adegoke
"""

# Configure the Google PaLM API with your API key
palm.configure(api_key='AIzaSyDXNVDbOLLUKukRp5pxnzZGzX3KNk8MPtY')


def runWithCmdLineArg():
    """
    This function is designed to be run with command line arguments.
    It reads the content of the files provided as arguments,
    and uses the Google PaLM API to generate a text response.
    """
    # Initialize variables
    files = []
    Instruction = None

    # Check each argument to see if it's a file or an instruction
    for arg in sys.argv[1:]:
        try:
            with open(arg, 'r') as f:
                files.append(arg)
        except IOError:
            Instruction = str(arg)

    # Read the content of each file
    contents = ""
    for file in files:
        with open(file, 'r') as f:
            contents += str(f.read())

    # Generate the prompt
    prompt = "{} {}".format(contents, Instruction if Instruction else "")

    # Use the Google PaLM API to generate a text response
    try:
        response = palm.generate_text(
            model="models/text-bison-001",
            prompt=prompt,
            temperature=0,  # The maximum length of the response
            max_output_tokens=800,
        )

        # Print the response
        print(response.result)
    except Exception as e:
        print(f"An Error Occurred: {e}")


def interactiveMode():
    """
    This function provides an interactive mode where the user can ask questions
    and get responses generated by the Google PaLM API.
    """
    username = os.getenv("USERNAME")
    print("CLIA>>> Command Line Interface Ai Assistant")
    print("[D] Hello {}, How can i help you?".format(username))
    while True:
        user_input = input("CLIA>>> ")
        if not user_input:
            continue
        if user_input.lower() == "help":
            print("Ask about anything!")
            print("e.g. 'What is the capital of France?')")
            print("You can also ask about code")
            print("e.g. 'What is the syntax for a for loop?')")
            print("type 'exit' or 'quit' to exit")
            continue
        if user_input.lower() == 'exit':
            break
        if user_input.lower() == 'quit':
            break
        try:
            response = palm.generate_text(
                model="models/text-bison-001",
                prompt=user_input,
                temperature=0,  # The maximum length of the response
                max_output_tokens=800,
            )
            print(response.result)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        runWithCmdLineArg()
    else:
        interactiveMode()
