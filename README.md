# Google-Drive-Data-Pipeline

## Preamble
I tried to make the code as self-documenting as possible. Please note that I redacted, for obvious reasons, the JSON credentials from main.py. Read [this documentation](https://docs.gspread.org/en/latest/oauth2.html) for more info about what this means.

## How to run this
- This repository is set up to run from Heroku. I'm currently running it entirely on the free plan. If you're worried about dyno time, you can also increase the sleep period (e.g. 5 mins instead of 1 min).

- You're also going to need to setup a Google Cloud Platform (GCP) developer account and enable API access to receive your JSON key. More information [here](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account). Once you have your JSON key, replace the parts of `main.py` that contain `REDACTED` to your JSON key and/or the links to the parts of your data pipeline (such as the form `URL_ID` or the sheet `URL_ID`).

## Why I made this
I live at a student co-op where everyone is required to submit 4 hours of what's known as *Habitability Improvement*, or *HI* for short. This entails activities like cleaning the communal gym, window washing, and so forth. What this repository does is make it so that people can submit a Google Form, and have their response automatically displayed in a public database. This lets them know how close they are to completion, and is quite convenient.

## How does this work
The general pipeline is as follows: |Google Form| --> |Heroku dyno| --> |Google Sheet|. Every minute, `main.py` will access (using Google's API) two spreadsheets. One is a legacy spreadsheet that I have to support, as I only became responsible for HI hours midway through the semester. The other is an active spreadsheet of Google Form responses. When `main.py` runs, it compares the results of the two spreadsheets with `pandas`. Then, it will clean the data, sanitize the results, and output it to a public Google Sheet.

## How to extend this
There are tons of edge cases that I, unfortunately, don't have time to cover as this is currently in `production`. People get fined if they don't have all their HI hours. I would feel really, really bad if I made a buggy deployment and caused people to panic. Anyways, here's a list of features that should/could be added.
- Correcting for when users' input multiple variations of their first name across separate forms
- Correcting for when users' misspell their name (this happens a lot)
