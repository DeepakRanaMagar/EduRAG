# EduRAG - Educational Retrieval-Augmented Generation System

## Project Overview
EduRAG is an intelligent educational platform that combines document management with AI-powered question answering. It allows users to upload educational content, organize it by topic and grade level, and interact with the material through a smart Q&A interface.

## Features
### Content Management
- 📁 **Upload System**: Store educational materials with metadata (topic, title, grade level)
- 🔍 **Organized Knowledge**: Categorize content for easy retrieval
- 📊 **Metrics Dashboard**: Track total topics, files, and grade levels

### Knowledge Discovery
- 🏷️ **Topic Browser**: View all available subjects
- 🎓 **Grade Filtering**: Find content by education level
- 📈 **System Analytics**: Monitor knowledge base growth

### Smart Q&A System
- ❓ **Natural Language Processing**: Answer questions in plain English
- 🧠 **Context-Aware**: Responses generated from uploaded materials
- 👥 **Personality Modes**: Choose between friendly, strict, or humorous tones

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload-content/` | POST | Upload educational content files |
| `/topics/` | GET | List available topics (filterable by grade) |
| `/grades/` | GET | List all grade levels in system |
| `/metrics/` | GET | Get system statistics |
| `/ask-question/` | POST | Get AI-generated answers to questions |

## Setup Instructions
### Build containers
docker compose build --no-cache

### Start the system
docker compose up