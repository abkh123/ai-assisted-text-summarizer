#!/usr/bin/env node
/**
 * @file server.js
 * @description Backend server for AI-Assisted Content Publisher
 * @encoding utf-8
 * @author [abkh]
 * @version 1.0
 * @date [2024]
 */

// Required Libraries
const express = require('express');
const app = express();
const PORT = 3000;

// Basic route for testing server
app.get('/', (req, res) => {
  res.send('AI-Assisted Content Publisher Backend!');
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
