from fastapi import FastAPI
from scanner import load_attacks, run_scan
from llm_judge import llm_judge
import weak_bot
import target_bot
from fastapi.responses import FileResponse
from pydantic import BaseModel
from auto_bot import AutoBot

app = FastAPI()

BOTS = {
    "weak": weak_bot.ask_bot,
    "safe": target_bot.ask_bot,
}

@app.get("/scan/{bot_name}")
def scan(bot_name: str):
    if bot_name not in BOTS:
        return {"error": "Unknown bot. Use 'weak' or 'safe'."}
    return run_scan(BOTS[bot_name], load_attacks(), llm_judge, runs=2)

@app.get("/")
def home():
    return FileResponse("index.html")

class UrlScanRequest(BaseModel):
    url: str
    authorized: bool

@app.post("/scan-url")
def scan_url(req: UrlScanRequest):
    if not req.authorized:
        return {"error": "You must confirm you own this site or have permission to test it."}
    if not req.url.startswith(("http://", "https://")):
        return {"error": "Enter a full link starting with http:// or https://"}
    try:
        bot = AutoBot(req.url)
    except Exception as e:
        return {"error": f"Could not find a chat box on that page: {e}"}
    try:
        return run_scan(bot.ask, load_attacks(), llm_judge, runs=2)
    finally:
        bot.close()

class ChatRequest(BaseModel):
    message: str

@app.post("/demo-chat")
def demo_chat(req: ChatRequest):
    return {"reply": weak_bot.ask_bot(req.message)}

@app.get("/demo")
def demo_page():
    return FileResponse("demo.html")

@app.get("/demo-launcher")
def demo_launcher_page():
    return FileResponse("demo_launcher.html")