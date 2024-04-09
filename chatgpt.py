# # chatgpt.py
# import openai
# from .config import OPENAI_API_KEY

# # Set up OpenAI API
# openai.api_key = OPENAI_API_KEY

# # Function to interact with ChatGPT
# def chatgpt_fact_check(user_message):
#     # Define the prompt to send to ChatGPT
#     prompt = f"Fact-check: {user_message}"
    
#     # Send the prompt to ChatGPT for completion
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=50  # Adjust this based on the desired length of the response
#     )
    
#     # Extract the generated text from the response
#     generated_text = response.choices[0].text.strip()
    
#     return generated_text
