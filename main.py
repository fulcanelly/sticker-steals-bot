from telethon import TelegramClient, events
import telethon
 
import logindata

client = TelegramClient("a", logindata.api_id, logindata.api_hash)
client.session.save()


async def add_sticker_to_pack(pack_name: str, sticker: str, emoji: str):
    await client.send_message("Stickers", "/addsticker")
    await client.send_message("Stickers", pack_name)
    await client.send_file("Stickers", sticker)
    await client.send_message("Stickers", emoji)


async def get_exact_message(where, id: int):
    async for msg in client.iter_messages(where, ids=[id]):
        return msg


@client.on(events.NewMessage(chats=["me"]))
async def stickerStealer(event: telethon.tl.custom.message.Message):
    packname = None
    
    try:
        _, packname = str(event.text).split(' ')
    except ValueError:
        pass
    
    if not event.text.startswith(".addsticker"):
        return 

    if not packname:
        return await client.send_message('me', "Specify pack name!")

    
    msg = await get_exact_message('me', event.reply_to.reply_to_msg_id)

    for attr in msg.document.attributes:
        if type(attr) == telethon.types.DocumentAttributeSticker:
            await add_sticker_to_pack(packname, await msg.download_media("stickers"), attr.alt)

    

with client:
    client.start()
    client.run_until_disconnected()