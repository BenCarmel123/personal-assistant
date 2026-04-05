# LangChain Introduction — Progress Plan

## Phase 1: Setup

### 1.1 Python Environment
- Create a Python virtual environment (`venv`)
- **Why venv over Docker:** We're learning locally, iterating fast, and don't need reproducible deployments yet. Docker adds friction without value at this stage. We'll Dockerize when we have something worth deploying.

### 1.2 Project Structure (Option B — Domain-Grouped)
- One agent, many tools — the assistant is a single agent that reasons over domain-specific tools
- Each domain (email, calendar, etc.) is a self-contained folder with its own tool, prompts, and samples
```
personal-assistant/
├── domains/
│   └── email/
│       ├── tool.py        # The email cleaning function
│       ├── prompts.py     # Prompt templates for email tasks
│       └── samples/       # Test emails
├── agent/
│   └── assistant.py       # Agent definition — tools, LLM, personality
├── config/
│   └── llm.py             # LLM connection setup
└── main.py                # Entry point
```

### 1.3 Install Dependencies
- LangChain core
- LLM provider SDK (OpenAI or Anthropic)
- python-dotenv for environment variable management
- Create `requirements.txt`

## Phase 2: Email Cleaner Agent

### 2.1 Connect to an LLM
- Set up API key via `.env`
- Create a basic LLM call to verify the connection works

### 2.2 Build the Email Cleaner Chain
- Define a prompt template that takes raw email text as input
- Output a structured summary: sender, subject, action items, priority level
- **LangChain concepts learned:** PromptTemplate, LLMChain, OutputParser

### 2.3 Test with Sample Emails
- Create a few sample emails (casual, formal, newsletter)
- Run the chain and verify output quality
- Iterate on the prompt

## Status
- [x] 1.1 Python environment
- [x] 1.2 Project structure
- [ ] 1.3 Dependencies
- [ ] 2.1 LLM connection
- [ ] 2.2 Email cleaner chain
- [ ] 2.3 Test with samples


