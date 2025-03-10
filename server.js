import express from 'express';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import bodyParser from 'body-parser';
import axios from 'axios';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const port = 3000;

// Set EJS as templating engine
app.set('view engine', 'ejs');
app.set('views', join(__dirname, 'views'));

// Middleware
app.use(express.static('public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
  res.render('editor');
});

// Language Mapping for Piston API
const languageVersions = {
  javascript: "node",
  python: "python",
  c: "c",
  cpp: "cpp",
  java: "java",
};

// Execute Code using Piston API
app.post('/execute', async (req, res) => {
  const { code, language } = req.body;
  const runtime = languageVersions[language.toLowerCase()];

  if (!runtime) {
    return res.status(400).json({ error: "Unsupported language" });
  }

  try {
    const response = await axios.post('https://emkc.org/api/v2/piston/execute', {
      language: runtime,
      version: "*",
      files: [{ content: code }],
    });

    res.json({
      output: response.data.run.output || "No output",
      error: response.data.run.stderr || null,
    });
  } catch (error) {
    res.status(500).json({ error: "Error communicating with Piston API", details: error.message });
  }
});

// Linting Endpoint
app.post('/checklint', async (req, res) => {
  const { code, language } = req.body;

  try {
    const flaskResponse = await axios.post('http://localhost:5000/analyze', { code });
    const lintingComments = flaskResponse.data.analysis_result || [];

    res.json({ comments: lintingComments });
  } catch (error) {
    res.status(500).json({ comments: [], error: "Failed to check code on Flask server" });
  }
});

// Generate Report Endpoint
app.post('/crerep', async (req, res) => {
  const { code, language } = req.body;

  try {
    const flaskResponse = await axios.post('http://localhost:5000/analyze', { code, language });
    const lintingComments = flaskResponse.data.analysis_result || [];

    const reportResponse = await axios.post('http://localhost:5000/report', {
      code: code,
      code_sum: lintingComments,
    });

    res.json({ output: reportResponse.data.report });
  } catch (error) {
    res.status(500).json({ comments: [], error: "Failed to check code on Flask server" });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
