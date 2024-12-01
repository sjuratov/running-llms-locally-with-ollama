## Prerequisits
- Create new virtual environment

```
python -m venv .venv
````

- Activate virtual environment (on Mac)

```
source .venv/bin/activate
````

- Install Python requirements

```
pip install -r requirements.txt
````

- Install [ollama](https://ollama.com)
- Download [models](https://ollama.com/search) that you would like to work with e.g. phi3.5, mistral, llama3.1 (for chat) and llava (for image analysis)

```
ollama pull phi3.5
ollama pull mistral
ollama pull llama3.1
ollama pull llava
````

- Make sure that ollama is running e.g.
```
ollama serve
````

**main_nb.ipynb**

Simple notebook to demonstrate chat functionality

**main.py**

FastAPI application to demonstrate following functionality. Use curl to call endpoints.
- Chat
```
curl -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d '{"prompt": "Explain why is sky blue in max 20 words", "model": "phi3.5"}'
```
- Streaming chat
```
curl -X POST "http://localhost:8000/chunks" -H "Content-Type: application/json" -d '{"prompt": "Explain why is sky blue in max 20 words", "model": "phi3.5"}'
```
- Image analysis
```
curl -X POST "http://localhost:8000/describeimage" -H "Content-Type: application/json" -d '{"prompt": "Describe this image", "model": "llava", "images": "images/house.jpeg"}'
```