import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetAllChatsRequest
from datetime import datetime, timedelta
import sys, os

# Printing download progress
def callback(current, total):
    with open(".config/data_log", "w") as file:
        file.write(str(current))
    global count_called; global mb_size
    if count_called > 150:
        hash_total = 50
        hash_count = round(hash_total*(round(current*100/total))/100)
        dash_count = hash_total - hash_count
        print('  Uploaded', current, 'out of', total, 'bytes [','#' * hash_count, '-' * dash_count, '] {:2.2%}'.format(current/total), end="\r")
        count_called = 0
        mb_size = round(total/1024/1024)
    else:
        count_called += 1

async def main():
    save_oneless = False
    old_heading = "Random_lectName"
    n = len(sys.argv)
    try:
        os.mkdir('.config')
    except:
        pass
    try:
        print("Trying to get api&chat details from .config/api_details if available...")
        with open('.config/api_details', 'r') as f:
            lines = f.read().splitlines()
            api_id = int(lines[0].split()[0])
            api_hash = lines[1].split()[0]
            chat_title = lines[2]
    except:
        print("Looks you running first time & api&chat details are not saved...")
        api_id = int(input("Please enter api-id: "))
        api_hash = input("Now enter api-hash: ")
        chat_title = input("Finally enter the Chat-Title to work upon: ")
        with open('.config/api_details', 'w') as f:
            f.write(str(api_id))
            f.write("\n")
            f.write(api_hash)
            f.write("\n")
            f.write(chat_title)
    try:
        with open(".config/last_done", "r") as file:
            file_num = int(file.read()) + 1
    except:
        file_num = 1
    if sys.argv[1] == "--fresh":
        file_num = 2
        save_oneless = True
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
                new_heading = sys.argv[file_num].split("/")[-1].rsplit("_", 2)[0]
                if not old_heading == new_heading:
                    print("Subject/Series changed... so Changing/Sending the new HEADING before uploading this new series...")
                    send_heading = new_heading.replace("_", " ") + " ✅ ✅"
                    await client.send_message(chat, send_heading)
                    old_heading = new_heading
                count_called = 0
                lect_caption = sys.argv[file_num].split("/")[-1].split(".")[0]
                file_path = sys.argv[file_num]
                start_time = datetime.now()
                print("Now uploading file", file_path)
                await client.send_file(chat, file_path, caption = lect_caption, supports_streaming=True, progress_callback=callback)
                with open('.config/data_log', 'r') as file:
                    final_data = int(file.read())
                print('  Uploaded', final_data, 'out of', final_data, 'bytes [','#' * 50, '] {:2.2%}'.format(1))
                time_taken = (datetime.now() - start_time).total_seconds()
                print("  Successfully uploaded Size-MB:", mb_size, "in time seconds: ", time_taken, "at Speed of:", mb_size/time_taken)
                print("Saving last_state to .config/last_done...")
                with open(".config/last_done", "w") as file:
                    if save_oneless:
                        file.write(str(file_num - 1))
                    else:
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
