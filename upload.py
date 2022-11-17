import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetAllChatsRequest
from datetime import datetime, timedelta
import sys, os

api_id = Your_api_id_number
api_hash = 'Your_api_hash_string'
chat_title = 'Chat_Title_to_Upload'

# Printing download progress
def callback(current, total):
    with open(".config/data_log", "w") as file:
        file.write(str(current))
    global count_called; global mb_size
    if count_called > 700:
        print('Downloaded', current, 'out of', total, 'bytes: {:.2%}'.format(current / total))
        print("Calling_Count is = ", count_called)
        count_called = 0
        mb_size = round(total/1024/1024)
    else:
        count_called += 1

async def main():
    n = len(sys.argv)
    try:
        os.mkdir('.config')
    except:
        pass
    try:
        with open(".config/last_done", "r") as file:
            file_num = int(file.read()) + 1
    except:
        file_num = 1
    if sys.argv[1] == "--fresh":
        file_num = 2
    print("Lenght of args is:", n, "And value of file_num to start with is:", file_num)

    client = TelegramClient('media_downloader', api_id, api_hash)
    await client.start()
    print("Connected now...")
    chats = await client(GetAllChatsRequest(except_ids=[]))
    for _, chat in enumerate(chats.chats):
        if chat.title == chat_title:
            chat_found = True
            print("found chat with title", chat_title)
            print("Attempting to Send Chat-Title a message...")
            global count_called; global mb_size

            while True:
                if not file_num < n:
                    break
                count_called = 0
                lect_caption = sys.argv[file_num].split("/")[-1].split(".")[0]
                file_path = sys.argv[file_num]
                start_time = datetime.now()
                print("Now uploading file", file_path)
                await client.send_file(chat, file_path, caption = lect_caption, supports_streaming=True, progress_callback=callback)
                print("Successfully sent the file...")
                time_taken = (datetime.now() - start_time).total_seconds()
                print("Size-MB was: ", mb_size, "And time taken was: ", time_taken)
                print("Saving last_state to .config/last_done...")
                with open(".config/last_done", "w") as file:
                    file.write(str(file_num))
                file_num += 1
                print("Now Sleeping for 20-seconds before next upload...")
                await asyncio.sleep(20)
    print("Last-Outer:: All done - Now disconnecting...")
    await client.disconnect()
    print("Disconnected now- Sleeping now... check on db -again...")
    await asyncio.sleep(20)

asyncio.run(main())

#
#@client.on(events.NewMessage(pattern='(?i)hi|hello'))
#async def handler(event):
#        await event.respond('Hey!')
