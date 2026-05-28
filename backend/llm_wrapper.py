import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from ingestion import save_log

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_response(message, session_id, history):

    start_time = time.time()

    try:

        prompt = ""

        for item in history:
            prompt += f"{item['role']}: {item['content']}\n"

        response = model.generate_content(prompt)

        output_text = response.text

        latency = int(
            (time.time() - start_time) * 1000
        )

        save_log({
            "session_id": session_id,
            "model": "gemini-1.5-flash",
            "provider": "google",
            "latency": latency,
            "input_tokens": len(prompt.split()),
            "output_tokens": len(output_text.split()),
            "status": "success",
            "input_preview": message[:100],
            "output_preview": output_text[:100]
        })

        return output_text

    except Exception as e:

        print("Gemini Error:", str(e))

        return f"Error: {str(e)}"