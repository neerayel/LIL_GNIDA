A telegram chat-bot for using different local-hosted stuff

Before running bot, copy .env_example as .env, and change .env as described inside.

For literal LOCAL hosted servers you can set TARGET_SERVER_BASE_URL=http://127.0.0.1:8080 in .env file.

If you have an error installing pydantic on termux > run this:
1) pkg install binutils
2) pkg install rust
3) pkg install build-essential
4) python -m pip install pydantic
5) python -m pip install fastapi
(not guarantied, but worked for me)
