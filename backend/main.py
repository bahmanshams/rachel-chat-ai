from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/reset")
async def reset():
    return reset_messages()

@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    message_decoded = convert_audio_to_text(audio_input)
    print(message_decoded)
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed message_decoded")

    chat_response = get_chat_response(message_decoded)

    if not chat_response:
        return HTTPException(status_code=400, detail="Failed chat_response")
    print(chat_response)
    store_messages(message_decoded, chat_response)

    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        return HTTPException(status_code=400, detail="Failed audio_output")

    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="application/octet-stream")
