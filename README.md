# LLM Red-Team Scanner

A web tool that automatically attacks a chatbot with prompt injection, jailbreak, prompt-leak, and data-leak attempts, then scores how safe the bot is and suggests fixes.

> **Use only on chatbots you own or have written permission to test.** The web page requires you to confirm this before scanning any link.

## How it works

1. **Attack library** (`attacks/attacks.json`): 20 attacks across 4 categories.
2. **Target**: a demo bot, or any website chat widget. A Playwright browser robot finds the chat box (including inside iframes or behind a "Chat with us" button), types each attack, and reads the reply.
3. **Judge** (`llm_judge.py`): a second LLM reads each attack and reply and decides whether the bot misbehaved.
4. **Repeats**: each attack runs more than once, because LLM answers vary.
5. **Report**: a 0-100 security score, severity per finding, and a suggested fix.

## Project structure

| File | Purpose |
|------|---------|
| `app.py` | FastAPI server and web endpoints |
| `scanner.py` | Scan engine, severity weights, fixes, score |
| `llm_judge.py` | LLM-based judge |
| `auto_bot.py` | Browser robot that finds and uses chat widgets |
| `index.html` | The scanner web page |
| `weak_bot.py`, `target_bot.py` | Demo bots (weak and safe) to practice on |
| `demo.html`, `demo_launcher.html` | Practice chat pages |

## Setup (Mac/Linux)

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

Create a `.env` file with a free Groq API key:

```
GROQ_API_KEY=your_key_here
```

## Run

```bash
python3 -m uvicorn app:app --reload
```

Open http://127.0.0.1:8000/, then either scan a demo bot or paste a link (try `http://127.0.0.1:8000/demo`), tick the permission box, and click **Scan link**. A full scan takes several minutes.

## Limitations

- Results vary between runs because LLM answers are random. Repeated tries reduce this but do not remove it.
- The LLM judge can make mistakes, so read the reported replies yourself.
- The robot picks the first visible text box, which may not be the chat on busy pages. Sites with bot protection, closed shadow DOM, or login walls are not supported.
- 20 attacks is a starting point, not complete coverage.
- Model names (`openai/gpt-oss-20b`, `openai/gpt-oss-120b`) may change on Groq. Check the list available to your account if you get a "model not found" error.

## Roadmap

- DPDPA Compliance Copilot: checks a privacy policy against India's Digital Personal Data Protection Act.