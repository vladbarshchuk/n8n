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
        llm = ChatGoogle(
            model="gemini-2.0-flash-exp",
            api_key=os.getenv("GOOGLE_API_KEY")  # Reads from Railway environment variable
        )

        agent = Agent(
            task="Search the latest news on Trump, and send the one by BBC",
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
