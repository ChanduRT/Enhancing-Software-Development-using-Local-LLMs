
import flask
from flask import request, jsonify
import google.generativeai as genai
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
    try:
        prompt = (
            f"Analyze the following Python code for security vulnerabilities.\n\n"
            f"--- Code ---\n{code}\n\n"
            "### Instructions:\n"
            "1. Provide a summary of vulnerabilities detected.\n"
            "2. List findings in a table with these columns:\n"
            "   - Vulnerability\n"
            "   - Description\n"
            "   - Severity (Critical/High/Medium/Low)\n"
            "   - Line Number(s)\n"
            "3. Explain root causes and remediation for each issue.\n"
            "4. Provide enhanced or optimized secure code for each issue.\n\n"
            "### Examples for reference:\n"
            f"{vulnerability_examples}\n"
        )

        # Debug print (optional)
        # print(prompt)

        response = model_vulnerability_checker.generate_content(
            prompt,
            safety_settings={
                'HARASSMENT': 'block_none',
                'HATE_SPEECH': 'block_none',
                'HARM_CATEGORY_HARASSMENT': 'block_none',
                'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none',
            }
        )

        return response.text

    except Exception as e:
        return f"Error during vulnerability analysis: {e}"

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

@app.route("/report", methods=["POST"])
def generate_report():
    """Generate a structured cybersecurity vulnerability report for the organization."""
    user_code = request.json.get("code")
    linting_comments = request.json.get("code_sum")

    if not user_code or not linting_comments:
        return jsonify({"error": "No code or analysis result provided"}), 400

    try:
        prompt = (
            f"Generate a detailed structured cybersecurity vulnerability report "
            f"based on the following code and vulnerability analysis:\n\n"
            f"--- Source Code ---\n{user_code}\n\n"
            f"--- Vulnerability Analysis ---\n{linting_comments}\n\n"
            "### Instructions for Report Format:\n"
            "1. Start with an **Executive Summary**:\n"
            "- General security posture overview.\n"
            "- Key issues found.\n\n"
            "2. Provide a **Security Assessment Summary (Pass/Fail Table)**:\n\n"
            "| Checkpoint                      | Status |\n"
            "|--------------------------------|--------|\n"
            "| Input Validation               | Pass/Fail |\n"
            "| Authentication & Authorization| Pass/Fail |\n"
            "| Sensitive Data Exposure        | Pass/Fail |\n"
            "| SQL Injection                  | Pass/Fail |\n"
            "| Cross-Site Scripting (XSS)     | Pass/Fail |\n"
            "| Command Injection              | Pass/Fail |\n"
            "| File Handling                  | Pass/Fail |\n"
            "| Error Handling & Logging       | Pass/Fail |\n"
            "| Secure Dependencies            | Pass/Fail |\n\n"
            "3. Create a **Detailed Vulnerability Findings Table**:\n\n"
            "| Vulnerability               | Description                                        | Severity | Line Number(s) |\n"
            "|-----------------------------|----------------------------------------------------|----------|----------------|\n"
            "| Example: SQL Injection      | Unsanitized input in query construction.           | High     | Line 15        |\n"
            "| Example: Hardcoded Password | Static password used in authentication logic.     | Critical | Line 42        |\n\n"
            "4. Add **Root Cause & Remediation Recommendations** for each issue:\n"
            "- Vulnerability\n"
            "- Root Cause\n"
            "- Remediation Steps\n\n"
            "5. Provide **Optimized and Enhanced Secure Code Examples** fixing the vulnerabilities:\n"
            "- Before and After code snippets.\n"
            "- Include explanations on improvements made.\n\n"
            "6. Finish with **Security Best Practices & Recommendations**:\n"
            "- Follow OWASP Top 10 guidelines.\n"
            "- Implement Secure SDLC practices.\n"
            "- Perform regular security assessments.\n"
            "- Secure sensitive data and use encryption.\n"
        )

        response = model_vulnerability_checker.generate_content(
            prompt,
            safety_settings={
                'HARASSMENT': 'block_none',
                'HATE_SPEECH': 'block_none',
                'HARM_CATEGORY_HARASSMENT': 'block_none',
                'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none',
            }
        )

        return jsonify({"report": response.text})

    except Exception as e:
        return jsonify({"error": f"Error generating report: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

