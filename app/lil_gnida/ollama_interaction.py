from ollama import AsyncClient
import logging

from filewriter import read_json_data, write_json_data, save_llm_response

logger = logging.getLogger(__name__)

ollama_error = "Ошибка при обращении к ollama" # temp var (move later in json table)


async def ollama_processer(settings, chat_model, input_data, options):
  """ Обращение к олламе. Возвращает -> response: object | None """

  ollama_server = settings.ollama_server["host"] + ":" + settings.ollama_server["port"]
  response = None
  try:
    response = await AsyncClient(ollama_server).chat(model=chat_model, messages=input_data, options=options)
  except Exception as e:
    logger.exception("Ошибка при обращении к ollama -> " + str(e))
  return response


def set_input_data(message: str, chat_history, temperature):
  """ Установка инпутов. Возвращает -> chat_history: object, options: object """

  input_message = {
        "content": "Message: " + message,
        "role": "user"
    }
  chat_history.append(input_message)
  options = {
    'temperature': temperature # max -> 1.5
  }
  return chat_history, options


async def llm_process_single(message: str, settings) -> str:
  """ Обработка inline запроса; 1 неизменный system промт """

  chat_history = read_json_data(settings.ollama_single_input_json_path)
  chat_history, options = set_input_data(message, chat_history, 1.)

  response = await ollama_processer(settings, settings.ollama_inline_model, chat_history, options)
  if not response: return ollama_error
  return response.message.content


async def llm_process_chat(message: str, settings) -> str:
  """ Обработка сообщения из чата; 1 неизменный system промт + история чата """

  chat_history = read_json_data(settings.ollama_chat_input_json_path)
  chat_history, options = set_input_data(message, chat_history, 1.)

  response = await ollama_processer(settings, settings.ollama_chat_model, chat_history, options)
  if not response: return ollama_error
  
  response_message = {
        "content": response.message.content,
        "role": "assistant"
    }
  chat_history.append(response_message)
  write_json_data(settings.ollama_chat_input_json_path, chat_history)

  return response.message.content
  
