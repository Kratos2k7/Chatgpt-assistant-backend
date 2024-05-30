from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
import os
app = Flask(__name__)

CORS(app)
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
client = OpenAI(api_key=openai_api_key)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    print(data)
    prompt = data['prompt']
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(thread_id=thread.id,role="user",content=prompt,)
    run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id=assistant_id)
    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
        print(f"Run status: {keep_retrieving_run.status}")
        if keep_retrieving_run.status == "completed":
            print("\n")
            break
    # Retrieve messages added by the Assistant to the thread
    all_messages = client.beta.threads.messages.list(thread_id=thread.id)

    response = {
        'user_input': prompt,
        'expanded_query': all_messages.data[0].content[0].text.value
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)