from flask import Flask, request
import os
from handler import message_handler, callback_query_handler

app = Flask(__name__)

@app.route('/',methods=['POST'])
def main():
    """
    
    RUNS FLASK APP AND CALLS HANDLERS FOR EACH TYPE OF QUERY
    :return: 200
    
    """
    answer=request.get_json()
    del answer["update_id"]
    print(answer)
    type = next(iter(answer.keys()))

    try:
        if (type == "message"):
            #print(answer)
            text = answer["message"]["text"]
            chat_id = answer["message"]["chat"]["id"]
            answer = {"chat_id": chat_id,
                      "text":text}
            message_handler(answer)

        elif (type == "callback_query"):
            #print(answer)
            chat_id = answer["callback_query"]["message"]["chat"]["id"]
            data = answer["callback_query"]["data"]
            message_id = answer["callback_query"]["message"]["message_id"]
            callback_query_id = answer["callback_query"]["id"]
            answer = {"chat_id":chat_id,
                      "data":data,
                      "message_id":message_id,
                      "callback_query_id":callback_query_id
                      }
            callback_query_handler(answer)

    except Exception: return 'ok'

    return 'ok'


@app.route('/test')
def test():
    return 'working'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 443))
    app.run(host='0.0.0.0', port=port)