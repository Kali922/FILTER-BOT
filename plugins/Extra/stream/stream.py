from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import STREAM_MODE, URL, LOG_CHANNEL
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
import humanize

@Client.on_message(filters.private & filters.command("stream"))
async def stream_start(client, message):
    if not STREAM_MODE:
        await message.reply("**Streaming mode is currently disabled.**")
        return

    # Ask user to send a file
    try:
        msg = await client.ask(message.chat.id, "**Send me your file/video to get stream and download links.**")
    except Exception as e:
        await message.reply(f"**An error occurred: {e}**")
        return

    # Validate the media type
    if not msg.media or msg.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        await message.reply("**Please send a supported video or document file.**")
        return

    # Extract file details
    file = getattr(msg, msg.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)
    fileid = file.file_id
    user_id = message.from_user.id
    username = message.from_user.mention

    # Send media to the log channel
    log_msg = await client.send_cached_media(chat_id=LOG_CHANNEL, file_id=fileid)

    # Generate links
    file_name_encoded = quote_plus(get_name(log_msg))
    stream_link = f"{URL}watch/{str(log_msg.id)}/{file_name_encoded}?hash={get_hash(log_msg)}"
    download_link = f"{URL}{str(log_msg.id)}/{file_name_encoded}?hash={get_hash(log_msg)}"

    # Notify log channel
    await log_msg.reply_text(
        text=f"**Link Generated for User ID #{user_id}**\n"
             f"**Username:** {username}\n"
             f"**File Name:** {get_name(log_msg)}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🚀 Fast Download 🚀", url=download_link),
                    InlineKeyboardButton("🖥 Watch Online 🖥", url=stream_link)
                ]
            ]
        )
    )

    # Reply to the user
    msg_text = (
        f"<i><u>Your Link is Generated!</u></i>\n\n"
        f"<b>📂 File Name:</b> <i>{get_name(log_msg)}</i>\n"
        f"<b>📦 File Size:</b> <i>{filesize}</i>\n"
        f"<b>📥 Download:</b> <i>{download_link}</i>\n"
        f"<b>🖥 Watch Online:</b> <i>{stream_link}</i>\n\n"
        f"<b>🚸 Note:</b> Link will remain valid until the file is deleted."
    )

    await message.reply_text(
        text=msg_text,
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🖥 Stream", url=stream_link),
                    InlineKeyboardButton("📥 Download", url=download_link)
                ]
            ]
        )
    )








#-----------------------------------------------


# from pyrogram import Client, filters, enums
# from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
# from info import STREAM_MODE, URL, LOG_CHANNEL
# from urllib.parse import quote_plus
# from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
# from TechVJ.util.human_readable import humanbytes
# import humanize
# import random

# @Client.on_message(filters.private & filters.command("stream"))
# async def stream_start(client, message):
#     if STREAM_MODE == False:
#         return 
#     msg = await client.ask(message.chat.id, "**Now send me your file/video to get stream and download link**")
#     if not msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
#         return await message.reply("**Please send me supported media.**")
#     if msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
#         file = getattr(msg, msg.media.value)
#         filename = file.file_name
#         filesize = humanize.naturalsize(file.file_size) 
#         fileid = file.file_id
#         user_id = message.from_user.id
#         username =  message.from_user.mention 

#         log_msg = await client.send_cached_media(
#             chat_id=LOG_CHANNEL,
#             file_id=fileid,
#         )
#         fileName = {quote_plus(get_name(log_msg))}
#         stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
#         download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
 
#         await log_msg.reply_text(
#             text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
#             quote=True,
#             disable_web_page_preview=True,
#             reply_markup=InlineKeyboardMarkup(
#                 [[
#                     InlineKeyboardButton("🚀 Fast Download 🚀", url=download),  # web download Link
#                     InlineKeyboardButton('🖥️ Watch online 🖥️', url=stream)   # web stream Link
#                 ]]
#             )
#         )
#         rm=InlineKeyboardMarkup(
#             [[
#                 InlineKeyboardButton("sᴛʀᴇᴀᴍ 🖥", url=stream),
#                 InlineKeyboardButton('ᴅᴏᴡɴʟᴏᴀᴅ 📥', url=download)
#             ]] 
#         )
#         msg_text = """<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n\n<b> 🖥ᴡᴀᴛᴄʜ  :</b> <i>{}</i>\n\n<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ</b>"""

#         await message.reply_text(text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(msg)), download, stream), quote=True, disable_web_page_preview=True, reply_markup=rm)
