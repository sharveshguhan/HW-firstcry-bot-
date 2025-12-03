import logging
import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# --- CONFIGURATION ---
TOKEN = "8222361552:AAEj5uUhZUu98PwPT257PzRL-OpKEr4vdZs"
# URL to check (Hot Wheels on FirstCry)
URL = "https://www.firstcry.com/search?q=hot%20wheels&ref2=q_hot%20wheels"

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="I am the Hot Wheels Bot! I am now running on the server."
    )

def check_stock():
    # Setup Chrome options for Render (Headless is mandatory)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    status = "Checking..."
    try:
        driver.get(URL)
        # Wait a bit for the page to load
        driver.implicitly_wait(10)
        
        # Logic: Look for products. This is a basic check for the page title or elements
        # You can customize this to find specific "Sold Out" text later
        title = driver.title
        status = f"Website loaded successfully. Title: {title}"
        
        # Example: Find number of items (FirstCry usually lists items in 'list_img' class)
        items = driver.find_elements(By.CLASS_NAME, "list_img")
        if items:
            status += f"\nFound {len(items)} items on the page."
        else:
            status += "\nNo items found (or structure changed)."
            
    except Exception as e:
        status = f"Error checking website: {str(e)}"
    finally:
        driver.quit()
        
    return status

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = check_stock()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=status_msg)

if __name__ == '__main__':
    # Initialize Bot
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('check', check)) # Type /check to test scraping
    
    # Start the Bot
    print("Bot is starting...")
    application.run_polling()