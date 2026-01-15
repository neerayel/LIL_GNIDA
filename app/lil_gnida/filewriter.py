import json
import logging

logger = logging.getLogger(__name__)


def read_json_data(path: str) -> object:
  json_obj = None
  with open(path, "r", encoding="utf-8") as file_stream:
    json_obj = json.load(file_stream)
  return json_obj

def write_json_data(path: str, json_obj: object) -> bool:
  with open(path, "w", encoding="utf-8") as file_stream:
    file_stream.write( json.dumps(json_obj, sort_keys=True, indent=4, separators=(",", ": ")) )
  return True


def save_llm_response(path: str, response_message: str) -> bool:
  with open(path,"w", encoding="utf-8") as file_stream:
    file_stream.write(response_message)
  return True

def read_start_message(path: str) -> str:
  msg = ""
  with open(path,"r", encoding="utf-8") as file_stream:
    msg = file_stream.read()
  return msg