import pathlib
import textwrap
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def sendPrompt(message: str):
    pretext = "you are a fact checker. tell me if the message is true or false and why. give me truth percentage out of 100 percent as well. if you are unsure please say 'Sorry, I am unsure'. Explain why you think the message is true or false as well in maximum 2 sentences. so give me truth percentage is (0-100%), this message is likely (true/false). This is the message:"
    try:
        response = model.generate_content(pretext + message)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None





