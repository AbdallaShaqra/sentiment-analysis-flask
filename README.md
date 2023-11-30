# sentiment-analysis-flask

This is a sentiment analysis project created with Tensorflow and Keras the model trained with arabic text data from Levant area also it supports text with emoji


## Installation Steps:
1. `git clone https://github.com/AbdallaShaqra/sentiment-analysis-flask.git`
2. `pip3 install -r requirements.txt`
3. `python3 app.py`

## Usage:
`http://127.0.0.1:5000/api?text="<arabic_text>"`

## Example:
`http://127.0.0.1:5000/api?text="اشي سيء كتير"`

## Response:

```json
{
  "data": {
    "lang": "ar",
    "created": "2023-11-30 17:58:06.070271",
    "result": {
      "sentence": "\"اشي سيء كتير\"",
      "symbol": 0,
      "sentiment": "negative",
      "confidence": 98.6
    }
  }
}

```

