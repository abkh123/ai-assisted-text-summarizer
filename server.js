#!/usr/bin/env node
/**
 * @file server.js
 * @description This server handles article uploads and generates summaries using AI.
 * @encoding utf-8
 * @author [abkh]
 * @version 1.2.0
 * @license MIT
 * @date [2024]
 */

const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');

const app = express();
const PORT = 3000;

// Middleware to parse JSON
app.use(bodyParser.json());

// Temporary storage for articles
let articles = [];

/**
 * Helper function to generate summary via Python script
 */
function generateAISummary(content) {
  return new Promise((resolve, reject) => {
    const sanitizedContent = content.replace(/"/g, '\\"'); // Prevent quotation issues

    exec(`python ai_helper.py "${sanitizedContent}"`, (error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        reject(error);
        return;
      }
      if (stderr) {
        console.error(`stderr: ${stderr}`);
        reject(stderr);
        return;
      }
      resolve(stdout.trim());
    });
  });
}

/**
 * POST route to upload an article and generate AI summary
 */
app.post('/articles', async (req, res) => {
  const { title, content } = req.body;

  if (!title || !content) {
    return res.status(400).json({ error: 'Title and content are required.' });
  }

  try {
    const summary = await generateAISummary(content);

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
      article: newArticle
    });

  } catch (err) {
    res.status(500).json({ error: 'Failed to generate summary.' });
  }
});

/**
 * GET route to retrieve all articles.
 */
app.get('/articles', (req, res) => {
  res.json({ articles });
});

// Root route (for quick testing)
app.get('/', (req, res) => {
  res.send('AI-Assisted Content Publisher Backend Running!');
});

// Server start
app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
