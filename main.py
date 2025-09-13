from fastapi import FastAPI
import asyncio
from browser_use import Agent, Browser, Tools
from browser_use.llm import ChatGoogle
import os

app = FastAPI()

@app.post("/run")
async def run_script():
    try:
        # Use Playwright browser (works better in containers)
        browser = Browser(headless=True)
        tools = Tools()
        llm = ChatGoogle(model="gemini-2.0-flash-exp")

        agent = Agent(
            task="Go to this URL: https://www.instagram.com/nick_saraev/followers/ follow 5 account that have a profile picture of a person as well as first and last name",
            llm=llm,
            browser=browser,
            tools=tools
        )

        history = await agent.run()
        url = await browser.get_current_page_url()
        
        return {
            "status": "success",
            "current_url": url,
            "tokens_used": history.usage.total_tokens
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    return {"message": "Instagram bot is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
