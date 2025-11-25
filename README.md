A telegram chat-bot for using different remote/local-hosted stuff

Before running bot, copy .env_example as .env, and change .env as described inside.

If you have an error installing pydantic on termux > run this (not guarantied, but worked for me):
1) pkg install binutils
2) pkg install rust
3) pkg install build-essential
4) python -m pip install pydantic
5) python -m pip install fastapi

