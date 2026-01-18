# 🧠 Playbook Brain - Basketball Coach AI Backend

**Advanced Multi-Agent AI System** powered by LangGraph, OpenAI, and FastAPI

The backend intelligence engine for Basketball Coach AI, featuring a sophisticated multi-agent workflow that analyzes court positioning, generates tactical plays, and provides real-time coaching insights.

---

## 📋 Overview

Playbook Brain is a Python-based AI backend that uses LangGraph to orchestrate multiple specialized AI agents:

- **Greeter Agent**: Filters casual messages and handles initial user interaction
- **Analyzer Agent**: Analyzes court state, player positioning, and spacing
- **Router Agent**: Determines user intent and routes to appropriate specialist
- **Consultant Agent**: Provides tactical advice and strategic recommendations
- **Playbook Selector**: Retrieves and executes pre-defined NBA plays
- **Generative Play Agent**: Creates custom plays based on natural language
- **Executor Agent**: Executes plays step-by-step with animations

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **pip** or **poetry** for package management

### Installation

```bash
# Navigate to backend directory
cd playbook-brain

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the Server

#### Option 1: Using LangGraph CLI (Recommended)

```bash
# Install LangGraph CLI
pip install langgraph-cli

# Start the development server
langgraph dev

# Server will start on http://127.0.0.1:2024
```

#### Option 2: Direct Python Execution

```bash
# Run the FastAPI server directly
python server.py

# Server will start on http://localhost:8000
```

---

## 📁 Project Structure

```
playbook-brain/
├── graph/                      # LangGraph workflow definitions
│   ├── workflow.py            # Main graph orchestration
│   ├── state.py               # Shared state schema
│   ├── roster.py              # NBA player data management
│   ├── geometry.py            # Court geometry & spacing analysis
│   └── constants.py           # NBA teams & court configuration
│
├── nodes/                      # AI Agent implementations
│   ├── greeter.py             # Initial message filtering
│   ├── analyzer.py            # Court state analysis
│   ├── router.py              # Intent classification
│   ├── consultant.py          # Tactical advice
│   ├── playbook_selector.py  # Pre-defined plays
│   ├── generative_play_node.py # Custom play generation
│   ├── executor.py            # Play execution
│   └── llm_utils.py           # LLM helper functions
│
├── coach/                      # Basketball playbook library
│   └── playbook.py            # NBA play definitions
│
├── utils/                      # Utility functions
│   └── data_processor.py      # NBA data loading
│
├── data/                       # NBA player statistics
│   └── nba_stats_cleaned.csv  # Real NBA player data
│
├── scripts/                    # Helper scripts
│   ├── start.sh               # Startup script
│   └── clean_csv.py           # Data cleaning
│
├── langgraph.json             # LangGraph configuration
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
└── README.md                  # This file
```

---

## 🎯 Features

### Multi-Agent Workflow

The system uses a **graph-based workflow** where each agent specializes in a specific task:

1. **Greeter** → Filters casual messages
2. **Analyzer** → Analyzes court state
3. **Router** → Determines intent (SETUP, CONSULT, PLAYBOOK, GENERATE, ADJUST)
4. **Specialist Agents** → Execute specific tasks
5. **Executor** → Animates plays step-by-step

### Real NBA Data

- **30 NBA Teams** with complete rosters
- **Real player statistics** (PPG, RPG, APG, shooting %)
- **Position-based analysis** (PG, SG, SF, PF, C)
- **Advanced metrics** (Plus/Minus, efficiency)

### Court Analysis

- **Zone identification** (Paint, Mid-Range, 3-Point, Corner)
- **Spacing analysis** (Player distance calculations)
- **Tactical recommendations** (Pick & Roll, Isolation, etc.)

### Play Library

Pre-defined NBA plays including:
- **Horns** - High pick & roll from elbows
- **Spain Pick & Roll** - Advanced screening action
- **Flex Offense** - Continuous motion offense
- **Triangle Offense** - Phil Jackson's system
- **Princeton Offense** - Back-door cuts

---

## 🛠️ Technology Stack

- **Python 3.11** - Programming language
- **LangGraph 1.0+** - AI workflow orchestration
- **LangChain** - LLM framework
- **OpenAI GPT-4** - Language model
- **FastAPI** - Web framework (optional)
- **Pandas** - Data processing
- **Pydantic** - Data validation

---

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...          # Your OpenAI API key

# Optional
PORT=8000                       # Server port
HOST=0.0.0.0                   # Server host
FRONTEND_URL=http://localhost:3000  # Frontend URL for CORS
```

### LangGraph Configuration

The `langgraph.json` file defines the graph entry point:

```json
{
  "dependencies": ["."],
  "graphs": {
    "basketball_coach": "./graph/workflow.py:graph"
  },
  "env": ".env"
}
```

---

## 📚 API Documentation

### LangGraph Endpoints

When running with `langgraph dev`, the following endpoints are available:

- `POST /basketball_coach/invoke` - Synchronous invocation
- `POST /basketball_coach/stream` - Streaming responses
- `GET /basketball_coach/playground` - Interactive playground

---

## 🧪 Testing

```bash
# Run tests (if available)
pytest

# Test specific module
pytest tests/test_analyzer.py
```

---

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment instructions.

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) file for details.

---

**Built with ❤️ using LangGraph and OpenAI**

