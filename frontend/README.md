Stock Assistant AI
Production-grade AI Stock Market Assistant that uses Groq-hosted Llama 3.3 70B, FastAPI, React + TypeScript, and Agentic Tool Calling to answer stock market questions using real-time market data, fundamentals, news, and portfolio analysis.

Architecture
User Question
     ↓
 Router Agent (Groq Llama 3.3 70B)
     ↓
 ┌────────────────────────────────────┐
 │ Price Tool                         │
 │ Fundamentals Tool                  │
 │ News Tool                          │
 └────────────────────────────────────┘
     ↓
 Multi-Tool Execution (Parallel)
     ↓
 Answer Generation (Groq Llama 3.3 70B, Streaming)
     ↓
 React + TypeScript Chat UI
The backend is built using FastAPI and Python. It exposes a streaming chat endpoint and health endpoint.

The frontend is built using React + TypeScript (Vite) and supports:

Streaming responses
Chat history
Markdown rendering
Tool-driven AI answers
Conversation memory
Model & Tool Choices + Reasoning
Groq Llama 3.3 70B Versatile
Chosen because:

Free hosted inference
Very fast response generation
Strong reasoning capabilities
Excellent tool-routing performance
yFinance
Used as the primary stock market data source.

Provides:

Stock prices
Fundamentals
Market capitalization
Revenue
Sector information
News articles
Completely free and easy to integrate.

FastAPI
Chosen because:

High performance
Native streaming support
Automatic Swagger documentation
Easy deployment
React + TypeScript
Chosen because:

Strong type safety
Modern frontend ecosystem
Excellent developer experience
Suitable for production dashboards
How Routing Works
The assistant follows an agentic workflow.

Step 1 — Routing
Groq Llama receives the user question and determines which tools are required.

Example:

Question:

What is TCS PE ratio?
Router Output:

{
  "tools": ["fundamental_tool"],
  "ticker": "TCS.NS"
}
Question:

Compare TCS PE ratio and latest news.
Router Output:

{
  "tools": [
    "fundamental_tool",
    "news_tool"
  ],
  "ticker": "TCS.NS"
}
Step 2 — Tool Execution
Selected tools execute in parallel using ThreadPoolExecutor.

Example:

fundamental_tool
+
news_tool
Both run simultaneously.

Step 3 — Answer Generation
Tool outputs are combined and sent back to Groq Llama.

The model generates a natural language answer using only the tool results.

Step 4 — Streaming
The answer streams token-by-token to the React frontend.

Similar to ChatGPT.

Repository Structure
stock-assistant/

├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── router.py
│   ├── stock_tools.py
│   ├── portfolio_tool.py
│   ├── tools.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── main.tsx
│   │   └── types.ts
│   │
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
└── README.md
Setup & Run
Clone Repository
git clone <repository-url>

cd stock-assistant
Backend Setup
Create virtual environment:

python -m venv venv
Activate:

Mac/Linux

source venv/bin/activate
Windows

venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Create .env

GROQ_API_KEY=your_groq_api_key
Run backend:

uvicorn main:app --reload
Backend:

http://localhost:8000
Swagger:

http://localhost:8000/docs
Frontend Setup
Install dependencies:

npm install
Run frontend:

npm run dev
Frontend:

http://localhost:5173
API
POST /chat-stream
Request:

{
  "question": "What is TCS PE ratio?",
  "history": [
    {
      "role": "user",
      "content": "Previous question"
    },
    {
      "role": "assistant",
      "content": "Previous answer"
    }
  ]
}
Response Stream:

The
PE
ratio
of
TCS
is
14.88
GET /health
Returns:

{
  "status": "healthy"
}
Example Questions to Test
Price Tool
What is the current price of TCS?
Show latest Reliance price.
What is Infosys trading at right now?
Fundamentals Tool
Show TCS fundamentals.
What is Infosys PE ratio?
Give me Reliance market cap.
News Tool
Show latest TCS news.
Recent Infosys developments.
Reliance headlines.
Multi Tool Queries
Compare TCS PE ratio and latest news.
Expected Tools:

fundamental_tool
+
news_tool
Give me current price and PE ratio of Reliance.
Expected Tools:

price_tool
+
fundamental_tool
Give me current price, fundamentals and latest news of Infosys.
Expected Tools:

price_tool
+
fundamental_tool
+
news_tool
Memory Tests
Question:

What is TCS PE ratio?
Then:

Show its fundamentals.
Expected:

Assistant understands:

its = TCS
Question:

Show Infosys fundamentals.
Then:

Show latest news about it.
Expected:

Assistant understands:

it = Infosys
Planned Features
Real portfolio tracking
Technical indicators
Stock comparison engine
Watchlists
Alerts
LangGraph workflows
MCP server integration
RAG over annual reports
Multi-agent architecture
AI stock screener
Investment recommendation engine
Known Limitations
Depends on yFinance data availability.
News coverage depends on Yahoo Finance.
Portfolio data is currently static.
No user authentication.
Single-user local deployment.
Agent Loop reasoning is still under development.
Learning Outcomes
This project demonstrates:

FastAPI APIs
React + TypeScript
Streaming LLM responses
Tool Calling
Multi-Tool Agents
Agentic Workflows
Conversation Memory
Parallel Tool Execution
Groq LLM Integration
Production AI Architecture