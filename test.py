import asyncio
from browser_use import Agent, Browser, Tools
from browser_use.llm import ChatOpenAI

async def main():
    browser = Browser(
        headless=True,  # Run in headless mode to reduce overhead
        cdp_url="http://localhost:9222"
    )
    tools = Tools()

    # Use cheaper GPT-4 Mini model with optimized settings
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # Much cheaper than gpt-4
        api_key=" ",  # Replace with your actual key
        temperature=0.1,  # Lower temperature for more deterministic responses   # Limit response length to reduce costs
    )

    # Batch URLs into smaller groups to reduce context size per run
    urls = [
        "https://www.instagram.com/direct",
        # ... (include all your URLs here)
    ]
    
    # Process in batches of 10-15 URLs to minimize context size
    batch_size = 10
    total_tokens = 0
    username_list=[]
    for i in range(0, len(urls), batch_size):
        batch_urls = urls[i:i+batch_size]
        url_list = "\n".join(batch_urls)
        
        # More concise and specific task description
        task = f'''Go to this link
{url_list}

For each chat on the left side:
1. Click on the chat.
2. Copy the username.
3. Add the name in the https://blankslate.io/
4. Go through 30 chats.'''

        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
            tools=tools,
            max_actions_per_step=3,  # Limit actions to reduce token usage
        )

        try:
            history = await agent.run()
            total_tokens += history.usage.total_tokens
            print(f"Batch {i//batch_size + 1} completed. Tokens used: {history.usage.total_tokens}")
            
            # Optional: Add delay between batches to avoid rate limiting
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {e}")
            continue

    print("Current URL:", await browser.get_current_page_url())
    print("Total tokens spent:", total_tokens)



if __name__ == "__main__":
    # Choose your approach:
    asyncio.run(main()) 
