#!/usr/bin/env node
/**
 * @file server.js
 * @description Backend server for AI-Assisted Content Publisher
 * @encoding utf-8
 * @author [abkh]
 * @version 1.0
 * @date [2024]
 */


const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = 3000;

// Middleware to parse JSON clearly
app.use(bodyParser.json());

// Root route (Test)
app.get('/', (req, res) => {
  res.send('AI-Assisted Content Publisher Backend Running!');
});


// Temporary storage for articles (for initial simplicity)
let articles = [];

/**
 * POST route to upload an article.
 * Expects JSON: { "title": "My Article", "content": "Article content here." }
 */
app.post('/articles', (req, res) => {
  const { title, content } = req.body;

  if (!title || !content) {
    return res.status(400).json({ error: 'Title and content are required.' });
  }

  const newArticle = {
    id: articles.length + 1,
    title,
    content,
    date: new Date()
  };

  articles.push(newArticle);

  res.status(201).json({
    message: 'Article uploaded successfully.',
    article: newArticle
  });
});

/**
 * GET route to retrieve all articles.
 */
app.get('/articles', (req, res) => {
  res.json({ articles });
});


app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
