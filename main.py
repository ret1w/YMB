import pyrogram as pr
import asyncio
import certifi
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()
api_id=os.getenv("API_ID")
api_hash=os.getenv("api_hash")
url=os.getenv("url")
chatName=os.getenv("chatName")
client = MongoClient(url,tlsCAFile=certifi.where(), server_api=ServerApi('1'))


async def main():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        db = client.test
        coll = db.posts
        lastdata = 0
        for data in coll.find().sort("data", 1):
            lastdata=data['data']

        async with pr.Client("my_account", api_id, api_hash) as app:
            async for dialog in app.get_dialogs():
                if dialog.chat.title in chatName:
                    async for message in app.get_chat_history(dialog.chat.id):
                        obj = []
                        if (lastdata<message.date):
                            if message.caption is not None:
                                obj.append(message.caption)
                                obj.append(message.date)
                                if message.photo is not None:
                                    file = await app.download_media(message)
                                    obj.append(file)
                            elif message.text is not None:
                                obj.append(message.text)
                                obj.append(message.date)
                                if message.photo is not None:
                                    file = await app.download_media(message)
                                    obj.append(file)
                            if len(obj) == 3:
                                print(coll.insert_one({"text":obj[0],"data":obj[1],"file":obj[2]}).inserted_id)
    except Exception as e:
        print(e)

asyncio.run(main())

