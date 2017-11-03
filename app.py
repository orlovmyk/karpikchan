from flask import Flask, request
import os
from handler import message_handler, callback_query_handler

app = Flask(__name__)


@app.route('/', methods=['POST'])
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
        if type == "message":
            #print(answer)
            update_dict = {}
            answer = answer['message']

            chat_id = answer["chat"]["id"]
            update_dict.update({"chat_id": chat_id})

            if 'text' in answer.keys():
                text = answer["text"]
                update_dict.update({"text": text})

            if 'location' in answer.keys():
                location = {'location': answer['location']}
                update_dict.update(location)

            message_handler(update_dict)

        elif type == "callback_query":
            #print(answer)
            chat_id = answer["callback_query"]["message"]["chat"]["id"]
            data = answer["callback_query"]["data"]
            message_id = answer["callback_query"]["message"]["message_id"]
            callback_query_id = answer["callback_query"]["id"]
            answer = {"chat_id": chat_id,
                      "data": data,
                      "message_id": message_id,
                      "callback_query_id": callback_query_id
                      }
            callback_query_handler(answer)

    except Exception: return 'ok'

    return 'ok'


@app.route('/test')
def test():
    return 'working'

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    app.run(host='0.0.0.0', port=port)