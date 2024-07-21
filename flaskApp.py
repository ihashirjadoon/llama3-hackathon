from flask import Flask, request, render_template, jsonify
import os
from together import Together
import google.generativeai as genai
import json

# Add API Keys before running
# genaiAPI = ""
# togetherApi = ""

app = Flask(__name__)
client = Together(api_key=togetherApi)

def start_template(book_type, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    prompt = f"You are a writing expert. So suggest short ways to start writing a {book_type}. Make sure it should be short and in 2 paragraphs"
    response = model.generate_content(prompt)
    return response.text.strip()

def summarize_paragraphs(paragraphs, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    prompt = f"Summarize the following text: {paragraphs}"
    response = model.generate_content(prompt)
    return response.text.split("\n")[0].strip()

def get_last_paragraph_and_summary(data):
    paragraphs = data.strip().split('\n')
    last_paragraph = paragraphs[-1] if paragraphs else ""
    previous_paragraphs = paragraphs[:-1] if len(paragraphs) > 1 else []
    summary = summarize_paragraphs(previous_paragraphs, genaiAPI)
    return summary, last_paragraph, len(paragraphs)

def create_prompt(summary, last_paragraph, paragraph_number, book_type, book_title):
    return f"""
    I am writing a {book_type} and This is paragraph {paragraph_number}. The title in my mind is {book_title}.
    Here is a summary of the previous paragraphs: {summary}
    Analyse the last paragraph and give me ways to improve: {last_paragraph}.
    After analysing, give a json output for :
    'Overall interest' [A floating value out of 10],
    Vivid Rating [A floating value out of 10],
    Build up: [Strong, Weak, Average],
    Irregularities: [if any],
    References: [Some reference book titles and authors],
    Summary : (summary of the paragraph),
    Suggestions: ,
    Strengths,
    Weaknesses.
    """

def analyze_paragraph(prompt):
    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
    return response

def json_response(response, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    prompt = f"Make this {response} as a json with keys 'Overall interest','Vivid Rating','Build up','Irregularities','References' (Dont use any special characters here but try to get the link for the mentioned book),'Summary','Suggestions','Strengths','Weaknesses'"
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_template', methods=['POST'])
def generate_template():
    data = request.json
    book_type = data.get('book_type')
    template = start_template(book_type, genaiAPI)
    return jsonify({'template': template})

@app.route('/analyze_paragraph', methods=['POST'])
def analyze():
    data = request.json
    book_type = data.get('book_type')
    book_title = data.get('book_title')
    novel_text = data.get('novel_text')
    summary, last_paragraph, paragraph_number = get_last_paragraph_and_summary(novel_text)
    prompt = create_prompt(summary, last_paragraph, paragraph_number, book_type, book_title)
    response = analyze_paragraph(prompt)
    json_raw = json_response(response, genaiAPI)
    json_data = json.loads(json_raw.replace("\n", "").replace("  ", "").replace("json", "").replace("`", ""))
    return jsonify(json_data)

if __name__ == "__main__":
    app.run(debug=True)
