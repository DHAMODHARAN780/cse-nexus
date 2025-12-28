# AI Doubt Clearing System - Setup Guide

## 🚀 Quick Setup

### 1. Install Required Packages
```bash
pip install google-generativeai PyPDF2
```

### 2. Get Your Gemini API Key
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

### 3. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 4. Restart Your Flask Server
Stop the current server (Ctrl+C) and restart:
```bash
python nexus.py
```

## ✨ How It Works

The AI system will:
1. **Search PDFs**: Look for relevant course materials based on keywords
2. **Extract Content**: Read text from matching PDFs
3. **AI Analysis**: Use Gemini AI to understand and answer the question
4. **Cite Sources**: Show which PDFs were used to generate the answer
5. **Fallback**: If no PDFs match, use general CS knowledge

## 📝 Example Questions

- "Explain process scheduling algorithms"
- "What is a microprocessor?"
- "How does binary search work?"
- "Difference between stack and queue"

## 🔧 Troubleshooting

**Error: "GEMINI_API_KEY not set"**
- Make sure you've set the environment variable
- Restart your terminal/server after setting it

**Error: "No module named 'google.generativeai'"**
```bash
pip install google-generativeai
```

**Error: "No module named 'PyPDF2'"**
```bash
pip install PyPDF2
```

## 🎯 Features

✅ Answers from uploaded PDF course materials
✅ General Computer Science knowledge fallback  
✅ Source citation with direct PDF links
✅ Chat-like interface
✅ Real-time AI responses

Enjoy your AI-powered study assistant! 🤖✨
