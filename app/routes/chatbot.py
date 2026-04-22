from flask import Blueprint, render_template, request, jsonify
from groq import Groq
import os

chatbot_bp = Blueprint('chatbot', __name__)

# Initialize Groq client
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# System prompt — this makes AI behave like Ayurveda expert
SYSTEM_PROMPT = """You are AyurBot, an expert Ayurveda assistant for AyurSutra clinic.
You specialize in:
- Panchakarma therapies (Abhyanga, Shirodhara, Vamana, Virechana, Basti, Nasya)
- Ayurvedic diet and lifestyle advice
- Dosha types (Vata, Pitta, Kapha) and their treatments
- Pre and post therapy precautions
- Herbal medicines and remedies

Rules:
- Always be helpful, warm and professional
- Give practical Ayurveda advice
- For serious medical conditions, recommend consulting a doctor
- Keep answers clear and simple
- Use bullet points for lists
- Always mention relevant precautions
"""

@chatbot_bp.route('/')
def chatbot():
    return render_template('chatbot.html')

@chatbot_bp.route('/ask', methods=['POST'])
def ask():
    try:
        # Get question from user
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Send to Groq AI
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Get AI response
        answer = response.choices[0].message.content

        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500