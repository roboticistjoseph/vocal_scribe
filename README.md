<div align="center">

# 🎨 Vocal Scribe

### Transform hand gestures into speech through an interactive air-drawing interface

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8+-00897B?style=for-the-badge)](https://google.github.io/mediapipe/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

<img src="assets/demo.gif" alt="Paint to Talk Demo" width="600"/>

**Paint to Talk** is an experimental computer vision project that lets users draw text in the air using hand gestures, which then converts to speech in multiple languages. Built as a creative exploration of MediaPipe's hand-tracking capabilities, it combines gesture recognition, OCR, and text-to-speech to create an engaging multimodal interface.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Demo](#-demo) • [Performance Metrics](#-metrics)

</div>

---

## ✨ Features

<table>
<tr>
<td>

### 🖌️ **Air Drawing**
- Real-time hand tracking with 21 landmarks
- Smooth brush strokes with customizable thickness
- Natural drawing gestures (index finger up)

### 🗣️ **Text-to-Speech**
- OCR text recognition from drawings
- Multi-language support (English & French)
- Instant audio feedback

</td>
<td>

### 🎯 **Smart Modes**
- **Drawing Mode** - Create text in the air
- **Eraser Mode** - Clean up mistakes easily
- **Save Canvas** - Export your creations
- **Translation Modes** - Speak in different languages
- **Finger Counter** - Fun gesture recognition demo

### 🚀 **Performance**
- 30+ FPS on standard webcams
- Low-latency gesture detection
- Optimized for real-time interaction

</td>
</tr>
</table>

---


## 🛠️ Installation

### 1. Clone the Repository
```
git clone https://github.com/roboticistjoseph/vocal_scribe
cd vocal_scribe
```

### 2. Create Virtual Environment (Recommended)
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. 📋 **Dependencies & Installation**

#### **🐍 Python Version**
```
⚠️ CRITICAL: Python 3.7, 3.8, 3.9, or 3.10 ONLY
MediaPipe doesn't play nice with Python 3.11+ yet!
```

#### **📦 Python Packages**
```
opencv-python
mediapipe
pytesseract
ibm_watson
playsound
```

---

#### **🛠️ System Dependencies**

#### **1. Tesseract OCR Engine (Required)**
- **Download**: https://github.com/UB-Mannheim/tesseract/wiki
- **Pro Tip**: Install to default C drive location (`C:\Program Files\Tesseract-OCR`)
- No PATH headaches this way! 🎉

#### **2. Visual C++ Redistributable (SUPER IMPORTANT!)**
```
⚠️ INSTALL THIS EVEN IF YOU THINK YOU HAVE IT!
```
- **Download**: https://aka.ms/vs/17/release/vc_redist.x64.exe
- MediaPipe will cry without these DLLs
- This fixes 90% of "MediaPipe won't import" issues

---

#### **☁️ IBM Watson Setup**

##### **API Services Needed**
You need **TWO separate services**:

1. **Text-to-Speech**
   - Sign up: https://www.ibm.com/products/text-to-speech
   - Free tier: 10,000 characters/month
   - Voice options: https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-voices

2. **Language Translator** 
   - Docs: https://watson-developer-cloud.github.io/python-sdk/v4.7.1/apis/ibm_watson.language_translator_v3.html
   - Free tier: 1,000,000 characters/month

> **Note**: "I've disabled my API key - please create your own! The Lite plan is free within limits." 

---

#### **🚀 Quick Installation Order**

1. **Install Python 3.10 or lower**
   ```bash
   python --version  # Verify it's <=3.10
   ```

2. **Install Visual C++ Redistributable**
   - Just run the installer, click through, done

3. **Install Tesseract OCR**
   - Run installer → Choose default location → Easy peasy

4. **Install Python packages**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up IBM Watson**
   - Create IBM Cloud account
   - Generate API keys for both services
   - Update your config with the keys

---

## 🚀 Usage
Quick Start
```
python paint_interface.py

||Controls||
- Select Mode: Move hand to header buttons
- Draw: Index finger up, middle finger down
- Stop Drawing: Show two or more fingers
- Clear Canvas: Press 'C'
- Quick Save: Press 'S'
- Exit: Press 'Q' or ESC
```

---

## 📄 Demo
- 🌍 Demo and more details on the project included in my Portfolio: [link](https://josephkatakam.vercel.app/projects/cv_vocal_scribe)

---

## 🎯 Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **FPS** | 30-45 | Depends on hardware |
| **Hand Detection Accuracy** | 95%+ | Good lighting conditions |
| **Gesture Recognition** | 87% | All orientations |
| **OCR Accuracy** | 80%+ | Clear, separated letters |
| **Latency** | <100ms | Real-time response |

---

<div align="center">
  
### If you found this helpful, please ⭐ this repository!
Made with ❤️ and lots of ☕ by Joseph

</div>
