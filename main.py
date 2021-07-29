from telethon import TelegramClient, events
import telethon
 
import logindata

client = TelegramClient("a", logindata.api_id, logindata.api_hash)
client.session.save()


async def add_sticker_to_pack(pack_name: str, sticker: str, emoji: str):
    await client.send_message("Stickers", "/addsticker")
    await client.send_message("Stickers", pack_name)
    await client.send_message("Stickers", emoji)
    await client.send_file("Stickers", sticker)


@client.on(events.NewMessage(chats=["me"]))
async def stickerStealer(event: telethon.tl.custom.message.Message):

    if not event.text.startswith(".addsticker"):
        return 
        
    async for msg in client.iter_messages('me', ids=[event.reply_to.reply_to_msg_id]):
        for attr in msg.document.attributes:
            if type(attr) == telethon.types.DocumentAttributeSticker:
                await add_sticker_to_pack("packname", await msg.download_media("stickers"), attr.alt)
    return 



    

with client:
    client.start()
    client.run_until_disconnected()