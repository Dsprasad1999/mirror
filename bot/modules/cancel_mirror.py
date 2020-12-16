from telegram.ext import CommandHandler, run_async

from bot import download_dict, dispatcher, download_dict_lock, DOWNLOAD_DIR
from bot.helper.ext_utils.fs_utils import clean_download
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import *

from time import sleep
from bot.helper.ext_utils.bot_utils import getDownloadByGid, MirrorStatus


@run_async
def cancel_mirror(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    mirror_message = None
    if len(args) > 1:
        gid = args[1]
        dl = getDownloadByGid(gid)
        if not dl:
            sendMessage(f"<b>Gɪᴅ:</b> <code>{gid}</code> <b>Nᴏᴛ Fᴏᴜɴᴅ🚫.</b>", context.bot, update)
            return
        with download_dict_lock:
            keys = list(download_dict.keys())
        mirror_message = dl.message
    elif update.message.reply_to_message:
        mirror_message = update.message.reply_to_message
        with download_dict_lock:
            keys = list(download_dict.keys())
            dl = download_dict[mirror_message.message_id]
    if len(args) == 1:
        if mirror_message is None or mirror_message.message_id not in keys:
            if BotCommands.MirrorCommand in mirror_message.text or \
                    BotCommands.TarMirrorCommand in mirror_message.text:
                msg = "<b>☘️Mɪʀʀᴏʀ Aʟʀᴇᴀᴅʏ Hᴀᴠᴇ Bᴇᴇɴ Cᴀɴᴄᴇʟʟᴇᴅ</b>"
                sendMessage(msg, context.bot, update)
                return
            else:
                msg = "<b>⛽Pʟᴇᴀsᴇ Rᴇᴘʟʏ Tᴏ Tʜᴇ</b> /{BotCommands.MirrorCommand} <b>Mᴇssᴀɢᴇ Wʜɪᴄʜ Wᴀs Usᴇᴅ Tᴏ Sᴛᴀʀᴛ Tʜᴇ Dᴏᴡɴʟᴏᴀᴅ Oʀ</b> /{BotCommands.CancelMirror} <b>Gɪᴅ Tᴏ Cᴀɴᴄᴇʟ Mɪʀʀᴏʀ Yᴏᴜʀ Pʀᴏᴄᴇss!</b>"
                sendMessage(msg, context.bot, update)
                return
    if dl.status() == "Uploading":
        sendMessage("<b>📤Uᴘʟᴏᴀᴅ Oꜰ Yᴏᴜʀ Fɪʟᴇ Is Aʟʀᴇᴀᴅʏ Iɴ Pʀᴏɢʀᴇss, Pʟᴇᴀsᴇ 🚫Dᴏɴ'ᴛ Cᴀɴᴄᴇʟ Iᴛ!</b>", context.bot, update)
        return
    elif dl.status() == "Archiving":
        sendMessage("<b>🔐Aʀᴄʜɪᴠᴀʟ Oꜰ Yᴏᴜʀ Fɪʟᴇ Is Aʟʀᴇᴀᴅʏ Iɴ Pʀᴏɢʀᴇss, Pʟᴇᴀsᴇ 🚫Dᴏɴ'ᴛ Cᴀɴᴄᴇʟ Iᴛ!</b>", context.bot, update)
        return
    else:
        dl.download().cancel_download()
    sleep(1)  # Wait a Second For Aria2 To free Resources.
    clean_download(f'{DOWNLOAD_DIR}{mirror_message.message_id}/')


@run_async
def cancel_all(update, context):
    with download_dict_lock:
        count = 0
        for dlDetails in list(download_dict.values()):
            if dlDetails.status() == MirrorStatus.STATUS_DOWNLOADING \
                    or dlDetails.status() == MirrorStatus.STATUS_WAITING:
                dlDetails.download().cancel_download()
                count += 1
    delete_all_messages()
    sendMessage(f'<b>⛽Cᴀɴᴄᴇʟʟᴇᴅ ➼ {count} Dᴏᴡɴʟᴏᴀᴅs!</b>!', context.bot, update)


cancel_mirror_handler = CommandHandler(BotCommands.CancelMirror, cancel_mirror,
                                       filters=(CustomFilters.authorized_chat | CustomFilters.authorized_user) & CustomFilters.mirror_owner_filter)
cancel_all_handler = CommandHandler(BotCommands.CancelAllCommand, cancel_all,
                                    filters=CustomFilters.owner_filter)
dispatcher.add_handler(cancel_all_handler)
dispatcher.add_handler(cancel_mirror_handler)
