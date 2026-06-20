#(©)CodeXBotz

import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "0"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "0"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

#Port
PORT = os.environ.get("PORT", "8000")

#Database
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "AdultFilmsPlus")

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))
JOIN_REQUEST_ENABLE = os.environ.get("JOIN_REQUEST_ENABLED", None)

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_PIC = os.environ.get("START_PIC","https://te.legra.ph/file/91820fa385ba7e60324de-d01cc4acc318dd71e3.jpg")
START_MSG = """<b>Hello 🤗, {username}
 
🌟 I'm <a href='https://t.me/AnonFileStoreBot'>Anonymous File Store Bot</a>

✨ Powered By : <a href='https://t.me/AdultFilmsPlus'>Adult Films</a>

☀️ Files Will Be Deleted In 10 Mins Due To Copyrights

🌊 Make Sure To Download (or) Forward Files Before They Deleted</b>
"""
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Auto delete time in seconds.
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "600"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "<b>🗂️ 𝐅𝐢𝐥𝐞𝐬 𝐖𝐢𝐥𝐥 𝐁𝐞 𝐃𝐞𝐥𝐞𝐭𝐞𝐝 𝐈𝐧 𝟏𝟎 𝐌𝐢𝐧𝐬 𝐃𝐮𝐞 𝐓𝐨 𝐂𝐨𝐩𝐲𝐫𝐢𝐠𝐡𝐭 𝐑𝐞𝐚𝐬𝐨𝐧𝐬\n📥 𝐒𝐚𝐯𝐞 (𝐨𝐫) 𝐅𝐨𝐫𝐰𝐚𝐫𝐝 𝐓𝐡𝐞𝐦 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐒𝐚𝐯𝐞𝐝 𝐌𝐞𝐬𝐬𝐚𝐠𝐞𝐬.</b>")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "🗂️ 𝐘𝐨𝐮𝐫 𝐅𝐢𝐥𝐞𝐬 𝐀𝐫𝐞 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐞𝐥𝐞𝐭𝐞𝐝 𝐁𝐲 𝐁𝐨𝐭.")
#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

#==================== gplinks Verification Gate ====================#
# Master switch for the verification gate. Set "False" to disable.
VERIFY_ENABLE = os.environ.get("VERIFY_ENABLE", "True") == "True"

# Your gplinks Developer API key (gplinks dashboard -> Developer API). REQUIRED.
SHORTLINK_API = os.environ.get("SHORTLINK_API", "")
# gplinks API endpoint. Usually no need to change.
SHORTLINK_API_URL = os.environ.get("SHORTLINK_API_URL", "https://api.gplinks.com/api")

# Public HTTPS URL of THIS bot's web server (e.g. https://your-app.koyeb.app), NO trailing slash.
# Koyeb/Render/Heroku expose the bot's PORT here. The /link and /confirm pages live on this URL.
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")

# How long (seconds) one successful verification grants free access. 86400 = 24 hours.
VERIFY_EXPIRE = int(os.environ.get("VERIFY_EXPIRE", "86400"))
# How long (seconds) an issued token stays valid to be completed. 900 = 15 minutes.
VERIFY_TOKEN_TTL = int(os.environ.get("VERIFY_TOKEN_TTL", "900"))
# Reject completions faster than this many seconds (catches instant bypass tools).
VERIFY_MIN_SECONDS = int(os.environ.get("VERIFY_MIN_SECONDS", "6"))

# Fernet secret key used to encrypt/sign verification tokens. Generate ONCE with:
#   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# Keep it stable; changing it invalidates all outstanding verification links.
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# Optional "how to verify" tutorial link (video/post). Button hidden if empty.
TUTORIAL = os.environ.get("TUTORIAL", "")

# Message shown together with the verify button.
VERIFY_MSG = os.environ.get("VERIFY_MSG", "<b>🔒 Verification Required\n\nPlease complete a quick verification to unlock your files.\nIt only takes a few seconds and keeps this bot free.</b>")

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "<b>You Are Not Allowed To Do That , Only Owner And Admins Can Use Me 🔌</b>"

ADMINS.append(OWNER_ID)

LOG_FILE_NAME = "AdultFilmsPlus.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
