# llama3-hackathon

# Writerr 🖋

Writerr is a web application designed to assist writers by generating writing templates and providing detailed analyses of their content. It uses Google Generative AI and the Meta-Llama model for content generation and analysis.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Functions](#functions)
- [Error Handling](#error-handling)
- [License](#license)

## Features

- Generate writing templates based on the type of book.
- Analyze paragraphs for suggestions, strengths, weaknesses, and various ratings.
- Provide a summary of the previous paragraphs and detailed analysis of the last paragraph.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/writerr.git
Change into the project directory:
bash
Copy code
cd writerr
Create and activate a virtual environment:
bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Usage
Set your API keys in the environment variables or directly in the code:

bash
Copy code
export TOGETHER_API_KEY='your_together_api_key'
export GENAI_API_KEY='your_genai_api_key'
Run the Flask application:

bash
Copy code
flask run
Access the application in your web browser at http://127.0.0.1:5000.

API Endpoints
1. Generate Template
Endpoint: /generate_template
Method: POST
Description: Generates a writing template based on the type of book.

Request Body:

json
Copy code
{
  "book_type": "Novel"
}
Response:

json
Copy code
{
  "template": "Once upon a time in a land far, far away..."
}
2. Analyze Paragraph
Endpoint: /analyze_paragraph
Method: POST
Description: Analyzes the given paragraph, provides suggestions, strengths, weaknesses, and various ratings.

Request Body:

json
Copy code
{
  "book_type": "Novel",
  "book_title": "The Great Adventure",
  "novel_text": "It was a dark and stormy night..."
}
Response:

json
Copy code
{
  "Summary": "The previous paragraphs discussed the protagonist's background...",
  "Suggestions": ["Add more descriptive language", "Introduce a plot twist"],
  "Strengths": ["Strong character development", "Engaging plot"],
  "Weaknesses": ["Lacks vivid descriptions", "Pacing is slow"],
  "Overall interest": 7.5,
  "Vivid Rating": 6.0,
  "Build up": "Strong",
  "Irregularities": "None",
  "References": "On Writing by Stephen King, Bird by Bird by Anne Lamott"
}
Functions
start_template(book_type, api_key)
Description: Generates a writing template based on the provided book type.

Parameters:

book_type (string): The type of book.
api_key (string): API key for Google Generative AI.
Returns: A string containing the generated template text.

summarize_paragraphs(paragraphs, api_key)
Description: Summarizes the given paragraphs using the Google Generative AI API.

Parameters:

paragraphs (string): The text to summarize.
api_key (string): API key for Google Generative AI.
Returns: A string containing the summary of the paragraphs.

get_last_paragraph_and_summary(data)
Description: Extracts the last paragraph and generates a summary of the previous paragraphs.

Parameters:

data (string): The text content of the book.
Returns: A tuple containing the summary, last paragraph, and the paragraph number.

create_prompt(summary, last_paragraph, paragraph_number, book_type, book_title)
Description: Creates a prompt for the AI model to analyze the last paragraph.

Parameters:

summary (string): Summary of the previous paragraphs.
last_paragraph (string): The last paragraph to be analyzed.
paragraph_number (int): The paragraph number.
book_type (string): The type of book.
book_title (string): The title of the book.
Returns: A string containing the prompt.

analyze_paragraph(prompt)
Description: Requests analysis and suggestions from the AI model.

Parameters:

prompt (string): The prompt for the AI model.
Returns: A string containing the AI's response.

json_response(response, api_key)
Description: Converts the analysis response to JSON format.

Parameters:

response (string): The AI's response to be converted.
api_key (string): API key for Google Generative AI.
Returns: A string containing the JSON formatted response.

Error Handling
Common Errors
400 Bad Request: The request body is missing required fields or has invalid data.

Response:
json
Copy code
{
  "error": "Invalid request. Please provide the required fields."
}
500 Internal Server Error: An error occurred on the server.

Response:
json
Copy code
{
  "error": "An internal server error occurred. Please try again later."
}
