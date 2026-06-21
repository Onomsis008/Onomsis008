# JARVIS - Advanced AI Assistant

JARVIS (Just A Rather Very Intelligent System) is a highly advanced personal assistant inspired by Marvel's Iron Man. It combines voice interaction, computer vision (finger and eye tracking), and Large Language Models to provide a comprehensive, companion-like experience.

## Features

- **Multilingual Companion**: Communicates in all languages with a polite and witty persona.
- **Voice Control**: Listen and respond using speech recognition and text-to-speech.
- **Vision Interaction**:
    - **Finger Tracking**: Move the mouse cursor and click using hand gestures.
    - **Eye Tracking**: Monitor gaze and iris movement for hands-free interaction.
- **System Actions**: Open websites, search the web, and execute system commands.
- **LLM Brain**: Powered by Google Gemini for sophisticated reasoning and natural conversation.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd jarvis
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment Variables**:
    Create a `.env` file in the root directory and add your Google Gemini API key:
    ```env
    GOOGLE_API_KEY=your_api_key_here
    ```

## Usage

To start JARVIS with full capabilities (requires camera and microphone):
```bash
python main.py
```

To run in text-only mode (useful for testing or headless environments):
```bash
python main.py --text
```

## Architecture

-   `main.py`: Entry point and integration hub.
-   `jarvis/engine/speech.py`: Handles Speech-to-Text and Text-to-Speech.
-   `jarvis/brain/llm.py`: Interface for the Gemini LLM and fallback logic.
-   `jarvis/vision/gestures.py`: Computer vision logic for hands and eyes using MediaPipe.
-   `jarvis/actions/system.py`: System-level automation tasks.

## Requirements

-   Python 3.10+
-   Webcam (for vision features)
-   Microphone (for voice features)
-   Active internet connection (for LLM and some voice features)

---
*At your service, Sir.*
