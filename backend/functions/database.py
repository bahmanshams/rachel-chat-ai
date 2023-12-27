import json
import random


def get_recent_messages():
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content": "You are interviewing the user for a job as a retail assistant. Ask short questions that are "
                   "relevant to the junior position. your name is Rachel. The user is called Bahman. Keep your "
                   "answers to under 30 words."
    }

    messages = []

    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include some dry humour."
    else:
        learn_instruction["content"] = (
                learn_instruction["content"] +
                " Your response will include a rather challenging question."
        )

    messages.append(learn_instruction)

    try:
        with open(file_name) as user_file:
            data = json.load(user_file)
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
            else:
                for item in data[-5:]:
                    messages.append(item)
    except Exception as e:
        print(e)

    return messages


def store_messages(request_message, response_message):
    file_name = "stored_data.json"
    messages = get_recent_messages()[1:]
    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    with open(file_name, "w") as f:
        json.dump(messages, f, ensure_ascii=False)


def reset_messages():
    open("stored_data.json", "w")
