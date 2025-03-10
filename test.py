
import flask
from flask import request, jsonify
import google.generativeai as genai
import asyncio
import concurrent.futures

# Configure the Gemini API
genai.configure(api_key="AIzaSyA2KeIU-XgmVeELWrC41NXHErVX4CeNeRQ")

# Initialize the vulnerability checking model
model_vulnerability_checker = genai.GenerativeModel("gemini-1.5-pro-latest")

# Examples of vulnerable and secure code
vulnerability_examples = """
### Vulnerable Code Example 1:
def login(user_input):
    query = "SELECT * FROM users WHERE username = '" + user_input + "';"
    execute_query(query)

### Secure Code Example 1:
def login(user_input):
    query = "SELECT * FROM users WHERE username = ?;"
    execute_query_with_params(query, (user_input,))

### Vulnerable Code Example 2:
import os
os.system("rm -rf /")

### Secure Code Example 2:
import os
if safe_condition:
    os.system("rm -rf /home/safe_directory")

### Vulnerable Code Example 3:
data = "<script>alert('XSS')</script>"
response.write(data)

### Secure Code Example 3:
data = "<script>alert('XSS')</script>"
safe_data = escape(data)
response.write(safe_data)

### Vulnerable Code Example 4:
def insecure_function(password):
    if password == "12345":
        return True

### Secure Code Example 4:
def secure_function(password):
    hashed_password = hash_password(password)
    if hashed_password == stored_hashed_password:
        return True

### Vulnerable Code Example 5:
file = open("data.txt", "r")
file.read()

### Secure Code Example 5:
with open("data.txt", "r") as file:
    file.read()
"""

# Create a Flask application
app = flask.Flask(__name__)

def analyze_code_vulnerabilities(code):
    """Analyze the provided code for vulnerabilities using the Gemini model."""

    try:
        prompt = (
            f"Analyze the following Python code for vulnerabilities. "
            f"Just Provide a response on whivh code the code is vulnerable exactly and what it is vulnerable to  with line numbers"
            f"and include suggestions for improvement if it's vulnerable. or give the secure code for this "
            f"Here are some examples for reference:\n{vulnerability_examples}\n\n"
            f"Code to analyze:\n{code}"
        )
        print(prompt)
        response = model_vulnerability_checker.generate_content(prompt, safety_settings={
        'HARASSMENT': 'block_none',
        'HATE_SPEECH': 'block_none',
        'HARM_CATEGORY_HARASSMENT': 'block_none',
        'HARM_CATEGORY_HATE_SPEECH': 'block_none',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none',
    })
      
        return response.text
    except Exception as e:
        return f"Error during vulnerability analysis: {e}"
@app.route("/report", methods=["POST"])
def generate_report():
    """Generate a detailed report for the organization based on the code and its vulnerability analysis."""
    user_code = request.json.get("code")
    linting_comments = request.json.get("code_sum")

    if not user_code or not linting_comments:
        return jsonify({"error": "No code or analysis result provided"}), 400

    try:
        # Prepare the prompt for Gemini to generate the report
        prompt = (
            f"Create a detailed security report for the organization based on the following code analysis:\n\n"
            f"Code:\n{user_code}\n\n"
            f"Analysis (Vulnerabilities and suggestions):\n{linting_comments}\n\n"
            "Provide a detailed report with the following sections:\n"
            "1. Overview of the code and vulnerabilities.\n"
            "2. Detailed vulnerability findings with line numbers.\n"
            "3. Suggested improvements and secure code examples.\n"
            "4. General security best practices.\n"
        )
        
        # Call Gemini to generate the report
        response = model_vulnerability_checker.generate_content(prompt, safety_settings={
            'HARASSMENT': 'block_none',
            'HATE_SPEECH': 'block_none',
            'HARM_CATEGORY_HARASSMENT': 'block_none',
            'HARM_CATEGORY_HATE_SPEECH': 'block_none',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none',
        })
        
        # Return the generated report
        return jsonify({"report": response.text})
    
    except Exception as e:
        return jsonify({"error": f"Error generating report: {e}"}), 500

@app.route("/analyze", methods=["POST"])
def analyze():
    """API endpoint to analyze posted code."""
    user_code = request.json.get("code")

    
    if not user_code:
        return jsonify({"error": "No code provided"}), 400
    
    # Asynchronously process the code vulnerability analysis
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(analyze_code_vulnerabilities, user_code)
        result = future.result()

    return jsonify({"analysis_result": result})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
