<h1>A telegram chat-bot for using different remote/local-hosted stuff</h1>

<div>
  <p>Used python -> 3.11</p>
  <p>Container image -> python:3.11-slim</p>
  <p>Container does not require volumes or exposed ports.</p>
</div>
</br>

<p>Before running bot, copy .env_example as .env, and change .env as described inside.</p>
</br>

<p>If you have an error installing pydantic on termux(android) > run this (not guarantied, but worked for me):</p>
<ul>
    <li>1) pkg install binutils</li>
    <li>2) pkg install rust</li>
    <li>3) pkg install build-essential</li>
    <li>4) python -m pip install pydantic</li>
    <li>5) python -m pip install fastapi</li>
</ul>
