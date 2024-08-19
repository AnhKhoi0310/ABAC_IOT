
import os
from dotenv import load_dotenv
load_dotenv()
from interfaces.getHistory import get_history
import google.generativeai as genai

def get_peaks(SubjectAddress):
    history_list = get_history(SubjectAddress)
    print(history_list)
    GEMINI_KEY = os.getenv('GEMINI_API')
    genai.configure(api_key= GEMINI_KEY )
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Given a list of timestamps in milliseconds representing when requests were made, identify the peak times. A peak is defined as a time period where requests are clustered closely together and occur frequently, indicating the time when the owner typically returns home."},
            {"role": "user", "parts": "No more than 3 peaks. Only return answer in a space-separated list of milliseconds timestamps"},
        ]
    )
    response = chat.send_message(str(history_list))
    print(response.text)
    return (response.text.split(), history_list[-1])

# get_peaks()