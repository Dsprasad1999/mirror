import shutil, psutil
import signal
import pickle

from os import execl, path, remove
from sys import executable
import time

from telegram.ext import CommandHandler, run_async
from bot import dispatcher, updater, botStartTime
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, delete


@run_async
def stats(update, context):
    currentTime = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>⦿ Bᴏᴛ Uᴘᴛɪᴍᴇ:</b> {currentTime}\n' \
            f'<b>⦿ Tᴏᴛᴀʟ Dɪsᴋ Sᴘᴀᴄᴇ:</b> {total}\n' \
            f'<b>⦿ Usᴇᴅ:</b> {used}  ' \
            f'<b>Free:</b> {free}\n\n' \
            f' \n<b>📊⁍Dᴀᴛᴀ Usᴀɢᴇ⁌📊</b>\n<b>⦿Uᴘʟᴏᴀᴅ:</b> {sent}\n' \
            f'<b>⦿ Dᴏᴡɴ:</b> {recv}\n\n' \
            f'<b>⦿ CPU:</b> {cpuUsage}% ' \
            f'<b>⦿ RAM:</b> {memory}% ' \
            f'<b>⦿ Dɪsᴋ:</b> {disk}%'
    sendMessage(stats, context.bot, update)


@run_async
def start(update, context):
    LOGGER.info('UID: {} - UN: {} - MSG: {}'.format(update.message.chat.id,update.message.chat.username,update.message.text))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        if update.message.chat.type == "private" :
            sendMessage(f"<b>Hɪ👋</b>  <b>{update.message.chat.first_name}</b>.  <b>Wᴇʟᴄᴏᴍᴇ Tᴏ Mɪʀʀᴏʀ Bᴏᴛ Sᴇɴᴅ /help Tᴏ Cʜᴇᴄᴋ Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅs Iɴ Mʏ Sᴇʀᴠɪᴄᴇ\n\n👮𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: @Dsp_Sai</b>", context.bot, update)
        else :
            sendMessage("<b>I'ᴍ Aʟɪᴠᴇ Yᴀᴀʀ💞, ➼Tʜᴀɴᴋs Fᴏʀ Cʜᴇᴄᴋɪɴɢ😋🥰.</b>", context.bot, update)
    else :
        sendMessage("<b>Oᴏᴘs!🤭 Yᴏᴜ Aʀᴇ Nᴏᴛ ᴀɴ Aᴜᴛʜᴏʀɪᴢᴇᴅ Usᴇʀ Tᴏ Usᴇ Mᴇ.</b>", context.bot, update)


@run_async
def restart(update, context):
    restart_message = sendMessage("<b>⛽ Rᴇsᴛᴀʀᴛɪɴɢ Mʏ Sᴇʀᴠɪᴄᴇs, Pʟᴇᴀsᴇ Wᴀɪᴛ!</b>", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'<b>{end_time - start_time} ᴍs</b>', reply)


@run_async
def log(update, context):
    sendLogFile(context.bot, update)


@run_async
def bot_help(update, context):
    help_string_adm = f'''<b>🛰️Tʜᴇsᴇ Aʀᴇ Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅs Iɴ Mʏ Sᴇʀᴠɪᴄᴇ👇👇</b>\n\n
/{BotCommands.StartCommand} <b>: Cʜᴇᴄᴋ Wʜᴇᴛʜᴇʀ Bᴏᴛ Is Aʟɪᴠᴇ ᴏʀ Nᴏᴛ</b>
/{BotCommands.MirrorCommand} <b>[url OR magnet_link]: Mɪʀʀᴏʀ Lɪɴᴋs & Uᴘʟᴏᴀᴅ</b>
/{BotCommands.TarMirrorCommand} <b>[url OR magnet_link]: Mɪʀʀᴏʀ Lɪɴᴋs & Uᴘʟᴏᴀᴅ ᴀs .ᴛᴀʀ</b>
/{BotCommands.UnzipMirrorCommand} <b>[url OR magnet_link] : Uɴᴢɪᴘ Lɪɴᴋs & Mɪʀʀᴏʀ</b>
/{BotCommands.WatchCommand} <b>[link]: Mɪʀʀᴏʀ YT Vɪᴅᴇᴏ</b>
/{BotCommands.TarWatchCommand} <b>[link]: Mɪʀʀᴏʀ YT Vɪᴅᴇᴏ & Uᴘʟᴏᴀᴅ ᴀs .ᴛᴀʀ</b>
/{BotCommands.CloneCommand} <b>[link]: Mɪʀʀᴏʀs ᴀ G-Dʀɪᴠᴇ Lɪɴᴋ ᴏʀ ᴀ Fᴏʟᴅᴇʀ</b>
/{BotCommands.CancelMirror} <b>: Rᴇᴘʟʏ Tᴏ /{BotCommands.MirrorCommand} Cᴏᴍᴍᴀɴᴅ ᴏʀ Eɴᴛᴇʀ /{BotCommands.CancelMirror} Cᴏᴍᴍᴀɴᴅ Gɪᴅ Tᴏ Cᴀɴᴄᴇʟ ᴀ Mɪʀʀᴏʀ Pʀᴏᴄᴇss</b>
/{BotCommands.CancelAllCommand} <b>: Cᴀɴᴄᴇʟ Aʟʟ Mɪʀʀᴏʀ Pʀᴏᴄᴇssᴇs</b>
/{BotCommands.StatusCommand} <b>: Sʜᴏᴡs ᴀ Sᴛᴀᴛᴜs Oꜰ Aʟʟ Tʜᴇ Dᴏᴡɴʟᴏᴀᴅs</b>
/{BotCommands.ListCommand} <b>[name]: Sᴇᴀʀᴄʜᴇs Iɴ Tʜᴇ Oᴡɴᴇʀs Tᴇᴀᴍ ᴅʀɪᴠᴇ Fᴏʟᴅᴇʀ</b>
/{BotCommands.deleteCommand} <b>[link]: Dᴇʟᴇᴛᴇ Fʀᴏᴍ Dʀɪᴠᴇ[Oɴʟʏ Oᴡɴᴇʀ & Sᴜᴅᴏ]</b>
/{BotCommands.StatsCommand} <b>: Sʜᴏᴡ Sᴛᴀᴛs Oꜰ Tʜᴇ Mᴀᴄʜɪɴᴇ</b>
/{BotCommands.PingCommand} <b>: Cʜᴇᴄᴋ Pɪɴɢ!</b>
/{BotCommands.RestartCommand} <b>: Rᴇsᴛᴀʀᴛ Bᴏᴛ[Oɴʟʏ Oᴡɴᴇʀ & Sᴜᴅᴏ]</b>
/{BotCommands.AuthorizeCommand} <b>: Aᴜᴛʜᴏʀɪᴢᴇ[Oɴʟʏ Oᴡɴᴇʀ & Sᴜᴅᴏ]</b>
/{BotCommands.UnAuthorizeCommand} <b>: Uɴᴀᴜᴛʜᴏʀɪᴢᴇ[Oɴʟʏ Oᴡɴᴇʀ & Sᴜᴅᴏ]</b>
/{BotCommands.AuthorizedUsersCommand} <b>: Aᴜᴛʜᴏʀɪᴢᴇᴅ Usᴇʀs[ᴏɴʟʏ Oᴡɴᴇʀ & Sᴜᴅᴏ]</b>
/{BotCommands.AddSudoCommand} <b>: Aᴅᴅ Sᴜᴅᴏ Usᴇʀ[Oɴʟʏ Oᴡɴᴇʀ]</b>
/{BotCommands.RmSudoCommand} <b>: Rᴇᴍᴏᴠᴇ Sᴜᴅᴏ Usᴇʀs[Oɴʟʏ Oᴡɴᴇʀ]</b>
/{BotCommands.LogCommand} <b>: Gᴇᴛ Bᴏᴛ Lᴏɢ Fɪʟᴇ[Oɴʟʏ Oᴡɴᴇʀ & Sᴜᴅᴏ]</b>\n\n
<b>👮𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 : @Dsp_Sai</b>
'''

    help_string = f'''<b>🛰️Tʜᴇsᴇ Aʀᴇ Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅs Iɴ Mʏ Sᴇʀᴠɪᴄᴇ👇👇</b>\n\n
/{BotCommands.StartCommand} <b>: Cʜᴇᴄᴋ Wʜᴇᴛʜᴇʀ Bᴏᴛ Is Aʟɪᴠᴇ ᴏʀ Nᴏᴛ</b>
/{BotCommands.MirrorCommand} <b>[url OR magnet_link]: Mɪʀʀᴏʀ Lɪɴᴋs & Uᴘʟᴏᴀᴅ</b>
/{BotCommands.TarMirrorCommand} <b>[url OR magnet_link]: Mɪʀʀᴏʀ Lɪɴᴋs & Uᴘʟᴏᴀᴅ ᴀs .ᴛᴀʀ</b>
/{BotCommands.UnzipMirrorCommand} <b>[url OR magnet_link] : Uɴᴢɪᴘ Lɪɴᴋs & Mɪʀʀᴏʀ</b>
/{BotCommands.WatchCommand} <b>[link]: Mɪʀʀᴏʀ YT Vɪᴅᴇᴏ</b>
/{BotCommands.TarWatchCommand} <b>[link]: Mɪʀʀᴏʀ YT Vɪᴅᴇᴏ & Uᴘʟᴏᴀᴅ ᴀs .ᴛᴀʀ</b>
/{BotCommands.CloneCommand} <b>[link]: Mɪʀʀᴏʀs ᴀ G-Dʀɪᴠᴇ Lɪɴᴋ ᴏʀ ᴀ Fᴏʟᴅᴇʀ</b>
/{BotCommands.CancelMirror} <b>: Rᴇᴘʟʏ Tᴏ /{BotCommands.MirrorCommand} Cᴏᴍᴍᴀɴᴅ ᴏʀ Eɴᴛᴇʀ /{BotCommands.CancelMirror} Cᴏᴍᴍᴀɴᴅ Gɪᴅ Tᴏ Cᴀɴᴄᴇʟ ᴀ Mɪʀʀᴏʀ Pʀᴏᴄᴇss</b>
/{BotCommands.CancelAllCommand} <b>: Cᴀɴᴄᴇʟ Aʟʟ Mɪʀʀᴏʀ Pʀᴏᴄᴇssᴇs</b>
/{BotCommands.StatusCommand} <b>: Sʜᴏᴡs ᴀ Sᴛᴀᴛᴜs Oꜰ Aʟʟ Tʜᴇ Dᴏᴡɴʟᴏᴀᴅs</b>
/{BotCommands.ListCommand} <b>[name]: Sᴇᴀʀᴄʜᴇs Iɴ Tʜᴇ Oᴡɴᴇʀs Tᴇᴀᴍ ᴅʀɪᴠᴇ Fᴏʟᴅᴇʀ</b>
/{BotCommands.StatsCommand} <b>: Sʜᴏᴡ Sᴛᴀᴛs Oꜰ Tʜᴇ Mᴀᴄʜɪɴᴇ</b>
/{BotCommands.PingCommand} <b>: Cʜᴇᴄᴋ Pɪɴɢ!</b>\n\n
<b>👮𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 : @Dsp_Sai</b>
'''

    if CustomFilters.sudo_user(update) or CustomFilters.owner_filter(update):
        sendMessage(help_string_adm, context.bot, update)
    else:
        sendMessage(help_string, context.bot, update)


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("⛽ 𝐌𝐲 𝐒𝐞𝐫𝐯𝐢𝐜𝐞𝐬 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲!")
        remove('restart.pickle')

    start_handler = CommandHandler(BotCommands.StartCommand, start)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling()
    LOGGER.info("Yeah I'm running!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)


main()
