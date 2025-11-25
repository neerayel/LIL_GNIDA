import logging
from ollama import AsyncClient, chat, ChatResponse
import json
from config import settings
  

logger = logging.getLogger(__name__)

# Обработка inline запроса; 1 неизменный system промт
async def llm_process_single(message):
  inputData = read_json_data(settings.ollama_single_input_json_path)
  input_message = {
        "content": message,
        "role": "user"
    }
  inputData.append(input_message)

  options = {
    'temperature': 0 # max -> 1.5
  }
  
  return await AsyncClient(settings.ollama_server_base_url).chat(model=settings.ollama_inline_model, messages=inputData, options=options)


# Обработка сообщения из чата; 1 неизменный system промт + история чата
# Пока что не внедрено
def llm_process_chat(message):
  inputData = read_json_data(settings.ollama_chat_input_json_path)
  input_message = {
        "content": message,
        "role": "user"
    }
  inputData.append(input_message)
  
  response: ChatResponse = chat(model=settings.ollama_chat_model, messages=inputData)
  response_message = {
        "content": response,
        "role": "assistant"
    }
  inputData.append(response_message)
  write_json_data(settings.ollama_chat_input_json_path, inputData)

  return save_llm_response(response)
  

def read_json_data(path):
  fileStream = open(path, "r", encoding="utf-8")
  jsonObj = json.load(fileStream)
  fileStream.close()
  return jsonObj

def write_json_data(path, jsonObj):
  fileStream = open(path, "w", encoding="utf-8")
  fileStream.write( json.dumps(jsonObj, sort_keys=True, indent=4, separators=(",", ": ")) )
  fileStream.close()

def save_llm_response(response):
  fileStream = open(settings.llm_response_path,"w", encoding="utf-8")
  fileStream.write(str(response.message.content))
  fileStream.close()
  return True

