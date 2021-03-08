# Robo-Advisor Project

Provides automated stock reccomendation based on API 

My submission to the Robo Advisor project:
https://github.com/wpp5/robo-advisor

Instructions for the project:
https://github.com/prof-rossetti/intro-to-python/blob/master/projects/robo-advisor/README.md

Guided walkthrough by Michael Rossetti was used in the creation of the code:
https://www.youtube.com/watch?v=UXAVOP1oCog&t=847s


## Setup

Clone or download repo from https://github.com/wpp5/robo-advisor onto your desktop

Nagivate from command line:
```sh
cd Desktop/robo-advisor
```

Obtain a unique API key from AlphaVantage: 
https://www.alphavantage.co

Create a file called .env within the local repo:

Within .env file, assign your unique API to the enviroment variable ALPHAVANTAGE_API_KEY

```sh 
ALPHAVANTAGE_API_KEY="abc123"
```
Substitute your unique API Key for "abc123"


## Environment Setup

Ensure you have python 3.8 downloaded. You can check your current verison by running the command:

```sh
python --version
```

Create a new virtual environment by running the following code in the command line:

```sh
conda create -n stocks-env python=3.8
conda activate stocks-env 
```

Install dotenv and requests packages by executing the following code:

```sh
pip install -r requirements.txt
```

## Usage

After navigating to the library (instructions in Setup), run the following program:

```sh
python app/robo_advisor.py
```


