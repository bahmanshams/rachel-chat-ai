from decouple import config
from functions.database import get_recent_messages
from openai import OpenAI

client = OpenAI(api_key=config("OPEN_AI_KEY"), organization=config("OPEN_AI_ORG"))


def convert_audio_to_text(audio_file):
    try:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return transcription
    except Exception as e:
        print(e)
        return


def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {
        "role": "user",
        "content": message_input
    }
    messages.append(user_message)
    print("++++++++++++++++++++++++++++++messages+++++++++++++++++++++++++++++++")
    print(messages)
    print("==============================messages--------------------------------")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        print(response)
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return
