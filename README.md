# Hybrid Speech Translator

This project is a Python-based multilingual speech translation application that combines offline speech recognition, translation, and text-to-speech capabilities.

The application also includes a phrase assistant system that allows users to quickly access common phrases categorized by context such as greetings, emergencies, travel, and shopping.

The system is designed to work offline-first, allowing core features to function even without an internet connection.


## Features

### Live Speech Translator
- Record speech directly from the microphone
- Convert speech to text using VOSK offline speech recognition
- Translate text using Argos Translate
- Speak translated output using gTTS (online) or pyttsx3 (offline)

### Hybrid Online / Offline Mode
- Automatic switching between:
  - Online Text-to-Speech
  - Offline Text-to-Speech
- Most features function without internet connectivity

### Phrase Category Assistant
Predefined phrase collections grouped into categories:

- Greetings
- Emergencies
- Travel
- Shopping

Each phrase can be translated between multiple languages instantly.

### Quick Phrase Translator
A simplified interface allowing users to translate commonly used phrases quickly.

### Graphical Interface
- Built using CustomTkinter
- Minimal and modern interface
- Language switching controls
- Status indicators and navigation menu


## Supported Languages

### Speech Recognition
- English
- Hindi
- French
- German
- Russian

### Translation and Text-to-Speech
- English
- Hindi
- Marathi
- Tamil
- Telugu
- Spanish
- French
- German
- Russian


## Technologies Used

- Python
- CustomTkinter
- VOSK Speech Recognition
- Argos Translate
- gTTS (Google Text-to-Speech)
- pyttsx3 (Offline Text-to-Speech)
- SoundDevice
- Playsound


## Installation

### 1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/speech-translator.git

cd speech-translator


### 2. Install Dependencies

pip install customtkinter  
pip install vosk  
pip install sounddevice  
pip install argostranslate  
pip install gtts  
pip install pyttsx3  
pip install playsound  


### 3. Download VOSK Speech Models

Download language models from:

https://alphacephei.com/vosk/models

Place them inside a folder structure like this:

vosk/
 ├── en
 ├── hi
 ├── fr
 ├── de
 └── ru


## Running the Application

python main.py


## Project Structure

speech-translator/
│
├── main.py
├── vosk/
│   ├── en/
│   ├── hi/
│   └── ...
│
├── README.md
└── requirements.txt


## Use Cases

This project can be useful for:

- Travelers communicating in different languages
- Language learning assistance
- Quick phrase translation
- Offline multilingual communication tools


## Future Improvements

Possible future enhancements include:

- Real-time streaming speech recognition
- Automatic language detection
- Mobile application support
- AI-based phrase prediction
- Voice speed and pitch controls


## License

This project is released under the MIT License.
