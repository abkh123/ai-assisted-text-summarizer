#!/usr/bin/env node
/**
 * @file server.js
 * @description Backend server for AI-Assisted Content Publisher
 * @encoding utf-8
 * @author abkh
 * @version 1.2
 * @date May 2024
 */

const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');

const app = express();
const PORT = 3000;

// Serve frontend
app.use(express.static('public'));

// Parse JSON
app.use(bodyParser.json());

// In-memory storage
let articles = [];

/**
 * Call Python script and parse JSON output
 */
function generateAISummary(content) {
  return new Promise((resolve, reject) => {
    const sanitizedContent = content.replace(/"/g, '\\"');

    exec(`python ai_helper_together.py "${sanitizedContent}"`, (error, stdout, stderr) => {
      if (error || stderr) {
        console.error("Python error:", error || stderr);
        return reject("Failed to summarize.");
      }

      try {
        const parsed = JSON.parse(stdout);
        resolve({
          summary: parsed.summary,
          truncated: parsed.truncated
        });
      } catch (e) {
        console.error("Failed to parse Python output:", stdout);
        reject("Invalid summary format.");
      }
    });
  });
}

/**
 * POST /articles - Save content + generate summary
 */
app.post('/articles', async (req, res) => {
  const { title = "Untitled", content } = req.body;

  if (!content) {
    return res.status(400).json({ error: "Content is required." });
  }

  try {
    const { summary, truncated } = await generateAISummary(content);

    const newArticle = {
      id: articles.length + 1,
      title,
      content,
      summary,
      date: new Date()
    };

    articles.push(newArticle);

    res.status(201).json({
      message: 'Article uploaded and summary generated successfully.',
      article: newArticle,
      truncated
    });
  } catch (err) {
    res.status(500).json({ error: err.toString() });
  }
});

/**
 * GET /articles - Return stored summaries
 */
app.get('/articles', (req, res) => {
  res.json({ articles });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
