# NLP Student Reflection Analysis System

A Python application that captures, processes, and analyzes student verbal reflections in educational settings using Natural Language Processing and AI.

## Overview

This application allows educators to:
- Collect verbal responses from students using speech recognition
- Process and analyze student reflections in real-time
- Generate comprehensive summaries of student feedback using Google's Gemini AI

## Features

- **Speech Recognition**: Captures student verbal responses and converts them to text
- **Text Preprocessing**: Normalizes text for consistent analysis (case normalization, punctuation removal)
- **AI-Powered Summarization**: Leverages Google's Gemini 2.0 Flash model to generate insights
- **User-Friendly Interface**: Simple Tkinter GUI for educators to manage the Q&A process
- **Data Persistence**: Stores historical question-reflection-summary data using NumPy arrays

## Technical Stack

- Python
- Google Gemini AI API
- SpeechRecognition library
- Tkinter GUI Framework
- NumPy

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install speech_recognition requests numpy tkinter
   ```
3. Ensure you have a working microphone for speech recognition

## Usage

1. Run the application:
   ```
   python main.py
   ```
2. Enter a question in the input field and click "Next"
3. Have students provide verbal responses using the "Record Answer" button
4. Use "Next Student" to move to the next respondent
5. Click "Finish Q&A" to generate a summary of all responses

## API Key Configuration

The application uses Google's Gemini AI API. U can get the API key from https://makersuite.google.com/app/apikey

## Data Files

The application uses the following data files:
- `questions.npy`: Stores historical questions
- `reflections.npy`: Stores student reflections
- `summary.npy`: Stores generated summaries
