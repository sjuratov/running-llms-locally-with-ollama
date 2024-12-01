from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import ollama
import base64

app = FastAPI()

class Query(BaseModel):
    prompt: str = "Why is sky blue?"
    model: str = "llama3.1"

class ImageQuery(BaseModel):
    prompt: str = ""
    model: str = ""
    images: str = ""

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# Run following curl command to make a chat request to the FastAPI server
# curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d '{"prompt": "Explain why is sky blue in max 20 words", "model": "phi3.5"}'

@app.post("/generate")
async def generate_text(query: Query):
    try:
        model = query.model
        messages = [{'role': 'user', 'content': f'{query.prompt}'}]

        response = ollama.chat(
            model = model,
            messages= messages
        )
        return response.message.content

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")

# Run following curl command to make a image request to the FastAPI server
# curl -X POST "http://localhost:8000/describeimage" -H "Content-Type: application/json" -d '{"prompt": "Describe this image", "model": "llava", "images": "images/house.jpeg"}'

@app.post("/describeimage")
async def describe_image(query: ImageQuery):
    try:
        model = query.model
        prompt = f'{query.prompt}'
        images = [image_to_base64(query.images)]

        response = ollama.generate(
            model = model,
            prompt = prompt,
            images = images,
            stream = False
        )
        return response.response

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")

# Run following curl command to make a chat request to the FastAPI server
# curl -X POST "http://localhost:8000/chunks" -H "Content-Type: application/json" -d '{"prompt": "Explain why is sky blue in max 20 words", "model": "phi3.5"}'

@app.post("/chunks")
async def stream_chat(query: Query):
    try:
        model = query.model
        messages = [{'role': 'user', 'content': f'{query.prompt}'}]

        stream = ollama.chat(
            model = model,
            messages= messages,
            stream=True
        )

        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)