from dotenv import load_dotenv
load_dotenv()
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

try:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello!"}]
    )
    print(response)
except Exception as e:
    import traceback; traceback.print_exc() 