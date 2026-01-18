# 🏀 Basketball Coach AI

**Advanced Tactical Basketball Strategy Platform** powered by AI, LangGraph, and Next.js

An intelligent basketball coaching assistant that combines real NBA player data with AI-powered tactical analysis to help coaches design plays, analyze court positioning, and make strategic decisions in real-time.

---

## 📋 Project Overview

This project consists of two main components:

### 🎨 **playbook-ai** (Frontend)
- **Technology**: Next.js 16, React 19, TypeScript, TailwindCSS
- **Features**: Interactive basketball court visualization, real-time AI chat interface, play animation
- **Framework**: CopilotKit for AI integration

### 🧠 **playbook-brain** (Backend)
- **Technology**: Python 3.11, LangGraph, FastAPI, OpenAI
- **Features**: Multi-agent AI system, NBA player database, tactical analysis engine, play generation
- **Architecture**: Graph-based workflow with specialized AI agents

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm/yarn/pnpm
- **Python** 3.11+
- **OpenAI API Key**

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd basketball_coach
```

### 2️⃣ Setup Backend (playbook-brain)
```bash
cd playbook-brain

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the server
python server.py
```

The backend will start on `http://localhost:8000`

### 3️⃣ Setup Frontend (playbook-ai)
```bash
cd playbook-ai

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will start on `http://localhost:3000`

---

## 📁 Project Structure

```
basketball_coach/
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
│
├── playbook-ai/                 # Frontend (Next.js)
│   ├── src/
│   │   ├── app/                 # Next.js app router
│   │   └── components/          # React components
│   ├── package.json
│   └── README.md
│
└── playbook-brain/              # Backend (Python)
    ├── src/
    │   └── playbook_brain/      # Main package
    │       ├── graph/           # LangGraph workflow
    │       ├── nodes/           # AI agent nodes
    │       ├── coach/           # Basketball playbook
    │       └── utils/           # Utilities
    ├── data/                    # NBA player data (CSV)
    ├── scripts/                 # Helper scripts
    ├── server.py                # FastAPI server
    ├── requirements.txt         # Python dependencies
    ├── setup.py                 # Package setup
    └── README.md                # Backend documentation
```

---

## 🎯 Features

### ✨ AI-Powered Coaching
- **Natural Language Interface**: Chat with the AI coach in Hebrew or English
- **Tactical Analysis**: Real-time court positioning and spacing analysis
- **Play Execution**: Execute pre-defined NBA plays step-by-step
- **Custom Play Generation**: Create custom plays based on natural language descriptions

### 📊 Real NBA Data
- **Player Statistics**: Real NBA player stats and capabilities
- **Team Rosters**: Complete rosters for all NBA teams
- **Advanced Metrics**: Shooting percentages, plus/minus, and more

### 🎨 Interactive Visualization
- **Basketball Court**: Drag-and-drop player positioning
- **Play Animation**: Visualize plays step-by-step
- **Real-time Updates**: See AI suggestions applied instantly

---

## 🛠️ Technology Stack

### Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **CopilotKit** - AI integration
- **React Flow** - Court visualization

### Backend
- **Python 3.11** - Programming language
- **LangGraph** - AI workflow orchestration
- **FastAPI** - Web framework
- **OpenAI GPT-4** - Language model
- **Pandas** - Data processing

---

## 📚 Documentation

- [Backend Documentation](playbook-brain/README.md) - Detailed backend architecture and API
- [Deployment Guide](playbook-brain/DEPLOYMENT.md) - How to deploy to production

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- NBA player data sourced from official statistics
- Built with LangGraph by LangChain
- UI powered by CopilotKit

---

**Made with ❤️ for basketball coaches and AI enthusiasts**

