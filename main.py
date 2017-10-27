from flask import Flask, request
from bot_token import token
from handler import message_handler, callback_query_handler
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('stats', 0)

app = Flask(__name__)

@app.route('/'+token,methods=['POST'])
def main():
    """
    
    RUNS FLASK APP AND CALLS HANDLERS FOR EACH TYPE OF QUERY
    :return: 200
    
    """
    answer=request.get_json()
    del answer["update_id"]
    print(answer)
    type = next(iter(answer.keys()))

    if (type == "message"):
        #print(answer)
        r.set('stats' , str(int(r.get('stats')) + 1))
        text = answer["message"]["text"]
        first_name = answer["message"]["chat"]["first_name"]
        try:
            last_name = answer["message"]["chat"]["last_name"]
        except KeyError: last_name = ''
        try:
            username = answer["message"]["chat"]["username"]
        except KeyError: username = ''
        chat_id = answer["message"]["chat"]["id"]
        answer = {"chat_id": chat_id,
                  "text":text,
                  "first_name": first_name,
                  "last_name": last_name,
                  "username":username}
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

    return 'ok'

@app.route('/stats')
def fuck():
    response = 'messages: ' + str(int(r.get('stats')))
    return response

if __name__ == '__main__':
    app.run()