import pika
from flask import Flask,request
app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

def event_stream():
    return 'data: %s\n\n' % 'test'

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/sendmessage')
def send_message():
    somemessage = request.args.get('msg')
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=somemessage)
    return somemessage

@app.route('/listen')
def listen_for_message():
    return flask.Response(event_stream(),
                          mimetype="text/event-stream")

if __name__ == '__main__':
    app.run()