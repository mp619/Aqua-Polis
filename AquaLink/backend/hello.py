import paho.mqtt.client as mqtt
from flask import Flask
from flask_restful import Api, Resource
import threading


app = Flask(__name__)
api = Api(app)
change = 0
myList = [3,4,8,1,change,4,2,0,2,9,3,8,4,7,2,7,0,1]

def thread1():
    mqtt_client.loop_forever()

@app.route('/', methods = ['GET'])
class Update(Resource):
    def get(self,pos):
        if(pos > len(myList)):
            return {"num" : "invalid number: out of list range"}
        else:
            return {"num": str(myList[pos])}

def on_connect(mqtt_client, obj, flags, rc):
    mqtt_client.subscribe("test")

def on_message(mqtt_client, obj, msg):
    print( str(msg.payload))
    change = int(msg.payload) 




api.add_resource(Update, "/Update/<int:pos>")

print("Initializing subscriber")
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("146.169.196.57", 1883) #146.169.193.199
print("Listening")
x = threading.Thread(target = thread1)
x.daemon = True
x.start() 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50162)
    
