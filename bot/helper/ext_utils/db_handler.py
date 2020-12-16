import psycopg2
from psycopg2 import Error
from bot import AUTHORIZED_CHATS, SUDO_USERS, DB_URI, LOGGER

class DbManger:
    def __init__(self):
        self.err = False

    def connect(self):
        try:
            self.conn = psycopg2.connect(DB_URI)
            self.cur = self.conn.cursor()
        except psycopg2.DatabaseError as error :
            LOGGER.error("Error in dbMang : ", error)
            self.err = True

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def db_auth(self,chat_id: int):
        self.connect()
        if self.err :
            return "<b>Tʜᴇʀᴇ's Sᴏᴍᴇ Eʀʀᴏʀ Cʜᴇᴄᴋ Lᴏɢ Fᴏʀ Dᴇᴛᴀɪʟs</b>"
        else:
            sql = 'INSERT INTO users VALUES ({});'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            AUTHORIZED_CHATS.add(chat_id)
            return '<b>Aᴜᴛʜᴏʀɪᴢᴇᴅ Sᴜᴄᴄᴇssꜰᴜʟʟʏ</b>'

    def db_unauth(self,chat_id: int):
        self.connect()
        if self.err :
            return "<b>Tʜᴇʀᴇ's Sᴏᴍᴇ Eʀʀᴏʀ Cʜᴇᴄᴋ Lᴏɢ Fᴏʀ Dᴇᴛᴀɪʟs</b>"
        else:
            sql = 'DELETE from users where uid = {};'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            AUTHORIZED_CHATS.remove(chat_id)
            if chat_id in SUDO_USERS:
                SUDO_USERS.remove(chat_id)
            return '<b>UɴAᴜᴛʜᴏʀɪᴢᴇᴅ Sᴜᴄᴄᴇssꜰᴜʟʟʏ<b>'

    def db_addsudo(self,chat_id: int):
        self.connect()
        if self.err :
            return "<b>Tʜᴇʀᴇ's Sᴏᴍᴇ Eʀʀᴏʀ Cʜᴇᴄᴋ Lᴏɢ Fᴏʀ Dᴇᴛᴀɪʟs</b>"
        else:
            if chat_id in AUTHORIZED_CHATS:
                sql = 'UPDATE users SET sudo = TRUE where uid = {};'.format(chat_id)
                self.cur.execute(sql)
                self.conn.commit()
                self.disconnect()
                SUDO_USERS.add(chat_id)
                return '<b>Sᴜᴄᴄᴇssꜰᴜʟʟʏ Pʀᴏᴍᴏᴛᴇᴅ Usᴇʀ As Sᴜᴅᴏ</b>'
            else:
                sql = 'INSERT INTO users VALUES ({},TRUE);'.format(chat_id)
                self.cur.execute(sql)
                self.conn.commit()
                self.disconnect()
                AUTHORIZED_CHATS.add(chat_id)
                SUDO_USERS.add(chat_id)
                return '<b>Sᴜᴄᴄᴇssꜰᴜʟʟʏ Aᴜᴛʜᴏʀɪᴢᴇᴅ Aɴᴅ Pʀᴏᴍᴏᴛᴇᴅ Usᴇʀ As Sᴜᴅᴏ</b>'

    def db_rmsudo(self,chat_id: int):
        self.connect()
        if self.err :
            return "<b>Tʜᴇʀᴇ's Sᴏᴍᴇ Eʀʀᴏʀ Cʜᴇᴄᴋ Lᴏɢ Fᴏʀ Dᴇᴛᴀɪʟs</b>"
        else:
            sql = 'UPDATE users SET sudo = FALSE where uid = {};'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            SUDO_USERS.remove(chat_id)
            return '<b>Sᴜᴄᴄᴇssꜰᴜʟʟʏ Rᴇᴍᴏᴠᴇᴅ Usᴇʀ Fʀᴏᴍ Sᴜᴅᴏ</b>'
