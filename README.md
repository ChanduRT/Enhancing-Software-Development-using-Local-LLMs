

---
# 💻 Dev_IDE (Enhancing software development using AI ) —
**Dev_IDE*, is a cutting-edge, browser-based Integrated Development Environment (IDE) focused on **developer productivity**, **AI-assisted coding**, and **security-first development**. It combines the power of real-time code execution, **local LLMs** via Ollama, and advanced vulnerability scanning to ensure your code is clean, optimized, and secure.

---

## 🚀 Key Features

### 🧠 AI-Powered Development
- **Ollama LLM Integration**: Interact with local large language models (like CodeLLaMA, Mistral) for real-time code suggestions, bug detection, and readability improvements.
- **Offline & Private**: No cloud processing. AI inference runs locally through Ollama — perfect for secure, offline development.
![image](https://github.com/user-attachments/assets/bfb09371-260b-44f2-b1ca-7eee12770737)

### 🔐 Secure Coding
- **Vulnerability Detection**: Real-time scans for OWASP Top 10, insecure code patterns, and logical flaws.
- **AI-Powered Review**: Generate AI-based reasoning for code vulnerabilities with remediation suggestions.

### ✨ Code Enhancement
- **Optimization Recommendations**: Receive suggestions to improve performance, reduce redundancy, and clean up memory usage.
- **Readability Improvements**: Refactor for better naming, formatting, and modularity.

### 🧪 Live Code Execution
- **Judge0 / Piston API Integration**: Compile and run code in over 40+ programming languages.
- **Custom Inputs & Outputs**: Execute code with runtime input and receive output in real-time.

![image](https://github.com/user-attachments/assets/be11eae1-b7c7-49de-b0c6-66678aeea96b)

### 📄 Professional Reporting
- **PDF Generation**: Export AI-reviewed, security-verified code with vulnerability reports, optimization tips, and code metadata using `html2pdf`.

---
![image](https://github.com/user-attachments/assets/32e6a083-3c46-4867-8afa-f1e8d0d15b05)

## ⚙️ Tech Stack

| Component       | Technology                         |
|-----------------|------------------------------------|
| Frontend        | HTML, CSS, JavaScript,   |
| Backend         | Node.js, electron.js , python      |
| AI Engine       | Ollama (running local LLMs)        |
| Compiler APIs   | Piston API / Judge0                |
| PDF Reports     | html2pdf.js                        |
| Vulnerability   |  AI-driven detection  |

---
![image](https://github.com/user-attachments/assets/c02a3c18-b890-4565-909e-37763e30436e)

## 📦 Installation & Setup

### 🔧 Requirements
- Node.js (v16+)
- NPM
- Ollama installed locally → [https://ollama.com](https://ollama.com)
- Git
![image](https://github.com/user-attachments/assets/d074fa54-7b4e-4772-ab1d-6f2f0f09f2b4)

### 🚀 Steps to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/your-username/dev_ide.git
cd dev_ide

# 2. Install backend dependencies
npm install

# 3. Start the Ollama LLM (use any model like codellama, mistral, etc.)
ollama run codellama

# 4. Start the Dev_IDE server
npm start
App runs at: http://localhost:3000

🎮 How to Use
Write code in the editor with syntax highlighting.

Click Run to compile via Judge0 or Piston.

Click Scan for vulnerability checks.

Ask AI Suggestions for optimizations or explanations (powered by Ollama).

Click Generate Report to export your code review as a PDF.

🔒 Security Features
✅ OWASP Top 10 Scanning

✅ AI Reasoning on Vulnerabilities

✅ Secure Code Patterns Suggestions

✅ Injection Detection (SQLi, XSS)

✅ Input Validation Checks

📄 Report Contents
Each PDF Report Includes:

🧩 Code Snapshot

🔐 Vulnerability Overview

⚙ Optimization Tips

🧠 AI Feedback (via LLM)

🕒 Timestamp & Language Metadata

🧠 AI Capabilities via Ollama
Models Supported:

codellama
Capabilities:

Explain functions line-by-line

Suggest cleaner code structure

Identify redundant logic

Summarize code functionality

Recommend security best practices

Ollama allows all inference to be local, giving you complete privacy and security.
![image](https://github.com/user-attachments/assets/5704fedb-7f99-48be-82fc-2df1c37ed71a)
📈 Roadmap
Feature	Status
AI-powered Bug Fixing	✅ Completed
Plugin-based Vulnerability Modules	🚧 In Progress
Docker Deployment	🚧 Planned
OAuth Integration	🚧 Planned
Syntax Error Auto-fix via AI	✅ Completed
Real-time Collaboration	🕓 On Hold

# Push and submit PR
git push origin feature/my-feature
🧪 Deployment (Optional Docker)
dockerfile
Copy
Edit
# Dockerfile (coming soon)
Containerized builds with Ollama GPU support & backend isolation  along with voice assisted coding are in progress.
