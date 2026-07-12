import os 
from dotenv import load_dotenv
from google import genai
class Generation:
    def __init__(self):
        pass
    def ask_question(self,user_question,context):
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)

        
       
        sysprompt = f'''
            You are a senior ai  modal advisor
            Give answer within the  context .Do not predict

            you have user query {user_question} and this is context {context} you have to give response well arranged 
            sentence

            If question is out of context tehn give answer  give accurate answer
        '''
        response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=sysprompt
        )
        return response.text

