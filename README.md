# V - Desktop Assistant

V is a high-tech, desktop-based AI assistant featuring a stunning, circular interface inspired by Iron Man Built with Python, it combines elegant HUD animations with the power of the Gemini AI brain and advanced hardware controls.

## Key Features

-   **Circular Interface**: A borderless, floating circular interface with dynamic, state-aware animations (Listening, Thinking, Processing).
-   **Gemini AI**: Full conversational capabilities with context awareness and memory.
-   **Music Control**: Instant music playback on YouTube.
-   **Hardware Integration**: Voice-controlled adjustment of system volume and screen brightness.
-   **System Monitoring**: Real-time reporting of CPU usage and battery levels.
-   **App Control**: Voice commands to open and close specific applications (YouTube, Google, VS Code, etc.).

## Voice Commands

This desktop assistant supports a wide range of natural language commands:

### General & AI
- **Any Question/Talk**: You can interact with the assistant and it will respond according to gemini ai.

### Music & Media
- **Play Song**: "Play [Song Name]", "Song [Song Name]", or "Music [Song Name]".
- **Stop Music**: "Stop music", "Pause music", or "Stop playing" (Closes the browser).

### System Controls
- **Volume**: 
  - "Set volume to 50" (or any 0-100).
  - "Increase volume", "Decrease volume".
  - "Full volume", "Half volume", "Mute volume".
- **Brightness**:
  - "Set brightness to 80" (or any 0-100).
  - "Increase brightness", "Decrease brightness".
  - "Full brightness", "Low brightness".

### Information & Stats
- **Wikipedia**: "Wikipedia [Topic]" (Summarizes the topic).
- **Time**: "What is the time?" or "The time".
- **CPU**: "CPU usage" or "CPU percentage".
- **Battery**: "Battery level" or "Battery percentage".

### Browser & Apps
- **Open**: "Open YouTube", "Open Google".
- **Close**: "Close YouTube", "Close Google", or "Close Browser".

### Shutdown 
- "Exit", "Quit", or "Stop".

## Setup & Installation

### 1. Prerequisites
- **Python 3.10+**
- **Gemini API Key** (Preferred) or you can use any other resource and accordingly you have to make changes in the code.

### 2. Dependencies

pip install -r requirements.txt

### 3. Configuration
1.  Create a `.env` file in the root directory and add your API key:
  
    GEMINI_API_KEY=your_actual_key_here
    
2.  Edit `config.json` to change the user name or assistant name.

## How to Run

python ui.py

## Author 
- Vaibhav Agarwal
- vaibhavwork478@gmail.com