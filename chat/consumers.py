import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"group_{self.room_name}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        event = text_data_json["event"]
        message = text_data_json["message"]
        
        if event == "message" :
       
            await self.channel_layer.group_send(
                #This will handle for a group of channels the dict will call the event handler
                #with the other keys value as arguments 
                self.room_group_name , {
                    "type" : "chat_message",
                    "message" : message
                    }
            )
        
        else:
            print("some other event handler here")

        # Send message to room group
        
    #Handler at indivitual channel level 
    async def chat_message(self , event):
        
        message = event["message"]
        
        await self.send(text_data=json.dumps({"message" : message}))