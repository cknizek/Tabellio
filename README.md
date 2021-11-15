# Cloyne-HI-Automator

I tried to make the code as self-documenting as possible. Please note that I redacted, for obvious reasons, the JSON credentials from main.py. Read this documentation for more info about what this means --> https://docs.gspread.org/en/latest/oauth2.html.

This repository is set up to run from Heroku. I'm currently running it entirely on the free plan. If you're worried about dyno time, you can also increase the sleep period (e.g. 5 mins instead of 1 min).

I'll update this later with .gifs, but for context: I live at a student co-op where everyone is required to submit 4 hours of what's known as *Habitability Improvement*, or *HI* for short. This entails activities like cleaning the communal gym, window washing, and so forth. What this repository does is make it so that people can submit a Google Form, and have their response automatically displayed in a public database. This lets them know how close they are to completion, and is quite convenient.
