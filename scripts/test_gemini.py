#%%
import google.generativeai as genai
import os
from dotenv import load_dotenv
#%%
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

#%%
prompt = "Di una frase corta en español."
response = model.generate_content(prompt)
print(response.text)

