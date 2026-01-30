# 🔧 Standard Library
import os
import re
import sys
import time
import json
import random
import string
import shutil
import zipfile
import urllib
import subprocess
from datetime import datetime, timedelta
from base64 import b64encode, b64decode
from subprocess import getstatusoutput
import base64
# 🕒 Timezone
import pytz
from pyrogram import enums

# 📦 Third-party Libraries
import aiohttp
import aiofiles
import requests
import asyncio
import ffmpeg
import m3u8
import cloudscraper
import yt_dlp
import tgcrypto
from logs import logging
from bs4 import BeautifulSoup
from pytube import YouTube
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ⚙️ Pyrogram
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto
)
from pyrogram.errors import (
    FloodWait,
    BadRequest,
    Unauthorized,
    SessionExpired,
    AuthKeyDuplicated,
    AuthKeyUnregistered,
    ChatAdminRequired,
    PeerIdInvalid,
    RPCError
)
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified

# 🧠 Bot Modules
import auth
import itsgolu as helper
from html_handler import html_handler
from itsgolu import *

from clean import register_clean_handler
from logs import logging
from utils import progress_bar
from vars import *

# Pyromod fix
import pyromod.listen
pyromod.listen.Client.listen = pyromod.listen.listen

from db import db
import os, requests, time
from urllib.parse import unquote, urlparse
from pyrogram.errors import FloodWait
height = 1080
width = 1920


# PDF Download function
'''def download_pdf(url: str, filename: str) -> str | None:
    url = unquote(url)
    origin = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        "Referer": origin,
        "Origin": origin,
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    file_path = f"/tmp/{filename}.pdf"
    try:
        print(f"[DEBUG] Downloading: {url}")
        r = requests.get(url, headers=headers, stream=True, timeout=(10, 180))
        print(f"[DEBUG] Status: {r.status_code}")

        if r.status_code not in (200, 206):
            print(f"[ERROR] Bad status {r.status_code}, body={r.text[:200]}")
            return None

        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=256*1024):
                if chunk:
                    f.write(chunk)

        print(f"[DEBUG] File saved: {file_path}")
        return file_path

    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return None


# PDF Decrypt function
def decrypt_pdf(file_path: str, key: str, out_name: str = "final.pdf") -> str | None:
    if not file_path or not os.path.exists(file_path):
        return None
    key_bytes = key.encode()
    size = min(28, os.path.getsize(file_path))
    with open(file_path, "rb") as f:
        data = bytearray(f.read())
    for i in range(size):
        data[i] ^= key_bytes[i] if i < len(key_bytes) else i
    out_path = f"/tmp/{out_name}"
    with open(out_path, "wb") as f:
        f.write(data)
    return out_path'''


# Main logic (same as your elif block)


auto_flags = {}
auto_clicked = False

# Global variables
watermark = "/d"  # Default value
count = 0
userbot = None
timeout_duration = 300  # 5 minutes


# Initialize bot with random session
bot = Client(
    "ugx",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=300,
    sleep_threshold=60,
    in_memory=True
)

# Register command handlers
register_clean_handler(bot)

@bot.on_message(filters.command("setlog") & filters.private)
async def set_log_channel_cmd(client: Client, message: Message):
    """Set log channel for the bot"""
    try:
        # Check if user is admin
        if not db.is_admin(message.from_user.id):
            await message.reply_text("⚠️ You are not authorized to use this command.")
            return

        # Get command arguments
        args = message.text.split()
        if len(args) != 2:
            await message.reply_text(
                "❌ Invalid format!\n\n"
                "Use: /setlog channel_id\n"
                "Example: /setlog -100123456789"
            )
            return

        try:
            channel_id = int(args[1])
        except ValueError:
            await message.reply_text("❌ Invalid channel ID. Please use a valid number.")
            return

        # Set the log channel without validation
        if db.set_log_channel(client.me.username, channel_id):
            await message.reply_text(
                "✅ Log channel set successfully!\n\n"
                f"Channel ID: {channel_id}\n"
                f"Bot: @{client.me.username}"
            )
        else:
            await message.reply_text("❌ Failed to set log channel. Please try again.")

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@bot.on_message(filters.command("getlog") & filters.private)
async def get_log_channel_cmd(client: Client, message: Message):
    """Get current log channel info"""
    try:
        # Check if user is admin
        if not db.is_admin(message.from_user.id):
            await message.reply_text("⚠️ You are not authorized to use this command.")
            return

        # Get log channel ID
        channel_id = db.get_log_channel(client.me.username)
        
        if channel_id:
            # Try to get channel info but don't worry if it fails
            try:
                channel = await client.get_chat(channel_id)
                channel_info = f"📢 Channel Name: {channel.title}\n"
            except:
                channel_info = ""
            
            await message.reply_text(
                f"**📋 Log Channel Info**\n\n"
                f"🤖 Bot: @{client.me.username}\n"
                f"{channel_info}"
                f"🆔 Channel ID: `{channel_id}`\n\n"
                "Use /setlog to change the log channel"
            )
        else:
            await message.reply_text(
                f"**📋 Log Channel Info**\n\n"
                f"🤖 Bot: @{client.me.username}\n"
                "❌ No log channel set\n\n"
                "Use /setlog to set a log channel"
            )

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Re-register auth commands
bot.add_handler(MessageHandler(auth.add_user_cmd, filters.command("add") & filters.private))
bot.add_handler(MessageHandler(auth.remove_user_cmd, filters.command("remove") & filters.private))
bot.add_handler(MessageHandler(auth.list_users_cmd, filters.command("users") & filters.private))
bot.add_handler(MessageHandler(auth.my_plan_cmd, filters.command("plan") & filters.private))

cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")
api_url = "http://master-api-v3.vercel.app/"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
cwtoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTExOTcwNjQsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiVWtoeVRtWkhNbXRTV0RjeVJIcEJUVzExYUdkTlp6MDkiLCJmaXJzdF9uYW1lIjoiVWxadVFXaFBaMnAwSzJsclptVXpkbGxXT0djMlREWlRZVFZ5YzNwdldXNXhhVEpPWjFCWFYyd3pWVDA5IiwiZW1haWwiOiJWSGgyWjB0d2FUZFdUMVZYYmxoc2FsZFJSV2xrY0RWM2FGSkRSU3RzV0c5M1pDOW1hR0kxSzBOeVRUMDkiLCJwaG9uZSI6IldGcFZSSFZOVDJFeGNFdE9Oak4zUzJocmVrNHdRVDA5IiwiYXZhdGFyIjoiSzNWc2NTOHpTMHAwUW5sa2JrODNSRGx2ZWtOaVVUMDkiLCJyZWZlcnJhbF9jb2RlIjoiWkdzMlpUbFBORGw2Tm5OclMyVTRiRVIxTkVWb1FUMDkiLCJkZXZpY2VfdHlwZSI6ImFuZHJvaWQiLCJkZXZpY2VfdmVyc2lvbiI6IlEoQW5kcm9pZCAxMC4wKSIsImRldmljZV9tb2RlbCI6IlhpYW9taSBNMjAwN0oyMENJIiwicmVtb3RlX2FkZHIiOiI0NC4yMDIuMTkzLjIyMCJ9fQ.ONBsbnNwCQQtKMK2h18LCi73e90s2Cr63ZaIHtYueM-Gt5Z4sF6Ay-SEaKaIf1ir9ThflrtTdi5eFkUGIcI78R1stUUch_GfBXZsyg7aVyH2wxm9lKsFB2wK3qDgpd0NiBoT-ZsTrwzlbwvCFHhMp9rh83D4kZIPPdbp5yoA_06L0Zr4fNq3S328G8a8DtboJFkmxqG2T1yyVE2wLIoR3b8J3ckWTlT_VY2CCx8RjsstoTrkL8e9G5ZGa6sksMb93ugautin7GKz-nIz27pCr0h7g9BCoQWtL69mVC5xvVM3Z324vo5uVUPBi1bCG-ptpD9GWQ4exOBk9fJvGo-vRg"
photologo = 'https://i.ibb.co/v6Vr7HCt/1000003297.png' #https://i.ibb.co/v6Vr7HCt/1000003297.png
photoyt = 'https://i.ibb.co/v6Vr7HCt/1000003297.png' #https://i.ibb.co/v6Vr7HCt/1000003297.png
photocp = 'https://i.ibb.co/v6Vr7HCt/1000003297.png'
photozip = 'https://i.ibb.co/v6Vr7HCt/1000003297.png'


# Inline keyboard for start command
BUTTONSCONTACT = InlineKeyboardMarkup([[InlineKeyboardButton(text="📞 Contact", url="https://t.me/ITsGOLU_OWNER_BOT")]])
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/ITsGOLU_OWNER_BOT")        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://i.ibb.co/v6Vr7HCt/1000003297.png",
    "https://i.ibb.co/v6Vr7HCt/1000003297.png",
    "https://i.ibb.co/v6Vr7HCt/1000003297.png",
    # Add more image URLs as needed
]

        
@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        # Wait for the user to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        downloaded_path = await input_message.download()

        # Read the content of the uploaded file
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        # Replace the content of the target cookies file
        with open(cookies_file_path, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text(
            "✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`."
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["t2t"]))
async def text_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    # Inform the user to send the text data and its desired file name
    editable = await message.reply_text(f"<blockquote>Welcome to the Text to .txt Converter!\nSend the **text** for convert into a `.txt` file.</blockquote>")
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.text:
        await message.reply_text("**Send valid text data**")
        return

    text_data = input_message.text.strip()
    await input_message.delete()  # Corrected here
    
    await editable.edit("**🔄 Send file name or send /d for filename**")
    inputn: Message = await bot.listen(message.chat.id)
    raw_textn = inputn.text
    await inputn.delete()  # Corrected here
    await editable.delete()

    if raw_textn == '/d':
        custom_file_name = 'txt_file'
    else:
        custom_file_name = raw_textn

    txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
    with open(txt_file, 'w') as f:
        f.write(text_data)
        
    await message.reply_document(document=txt_file, caption=f"`{custom_file_name}.txt`\n\n<blockquote>You can now download your content! 📥</blockquote>")
    os.remove(txt_file)

# Define paths for uploaded file and processed file
UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

@bot.on_message(filters.command("getcookies") & filters.private)
async def getcookies_handler(client: Client, m: Message):
    try:
        # Send the cookies file to the user
        await client.send_document(
            chat_id=m.chat.id,
            document=cookies_file_path,
            caption="Here is the `youtube_cookies.txt` file."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["stop"]) )
async def restart_handler(_, m):
    
    await m.reply_text("🚦**STOPPED**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)
        

@bot.on_message(filters.command("start") & (filters.private | filters.channel))
async def start(bot: Client, m: Message):
    try:
        if m.chat.type == "channel":
            if not db.is_channel_authorized(m.chat.id, bot.me.username):
                return
                
            await m.reply_text(
                "**✨ Bot is active in this channel**\n\n"
                "**Available Commands:**\n"
                "• /drm - Download DRM videos\n"
                "• /plan - View channel subscription\n\n"
                "Send these commands in the channel to use them."
            )
        else:
            # Check user authorization
            is_authorized = db.is_user_authorized(m.from_user.id, bot.me.username)
            is_admin = db.is_admin(m.from_user.id)
            
            if not is_authorized:
                await m.reply_photo(
                    photo=photologo,
                    caption="**Mʏ Nᴀᴍᴇ [DRM Wɪᴢᴀʀᴅ 🦋](https://t.me/ITsGOLU_OWNER_BOT)\n\nYᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇꜱꜱ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ\nCᴏɴᴛᴀᴄᴛ [𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®](https://t.me/ITsGOLU_OWNER_BOT) ғᴏʀ ᴀᴄᴄᴇꜱꜱ**",
                    reply_markup=InlineKeyboardMarkup([
    [
        InlineKeyboardButton("𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®", url="https://t.me/ITsGOLU_OWNER_BOT")
    ],
    [
        InlineKeyboardButton("ғᴇᴀᴛᴜʀᴇꜱ 🪔", callback_data="features"),
        InlineKeyboardButton("ᴅᴇᴛᴀɪʟꜱ 🦋", callback_data="details")
    ]
])
                )
                return
                
            commands_list = (
                "**>  /drm - ꜱᴛᴀʀᴛ ᴜᴘʟᴏᴀᴅɪɴɢ ᴄᴘ/ᴄᴡ ᴄᴏᴜʀꜱᴇꜱ**\n"
                "**>  /plan - ᴠɪᴇᴡ ʏᴏᴜʀ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴅᴇᴛᴀɪʟꜱ**\n"
            )
            
            if is_admin:
                commands_list += (
                    "\n**👑 Admin Commands**\n"
                    "• /users - List all users\n"
                )
            
            await m.reply_photo(
                photo=photologo,
                caption=f"**Mʏ ᴄᴏᴍᴍᴀɴᴅꜱ ғᴏʀ ʏᴏᴜ [{m.from_user.first_name} ](tg://settings)**\n\n{commands_list}",
                reply_markup=InlineKeyboardMarkup([
    [
        InlineKeyboardButton("𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®", url="https://t.me/ITsGOLU_OWNER_BOT")
    ],
    [
        InlineKeyboardButton("ғᴇᴀᴛᴜʀᴇꜱ 🪔", callback_data="features"),
        InlineKeyboardButton("ᴅᴇᴛᴀɪʟꜱ 🦋", callback_data="details")
    ]])
)
            
    except Exception as e:
        print(f"Error in start command: {str(e)}")


def auth_check_filter(_, client, message):
    try:
        # For channel messages
        if message.chat.type == "channel":
            return db.is_channel_authorized(message.chat.id, client.me.username)
        # For private messages
        else:
            return db.is_user_authorized(message.from_user.id, client.me.username)
    except Exception:
        return False

auth_filter = filters.create(auth_check_filter)

@bot.on_message(~auth_filter & filters.private & filters.command)
async def unauthorized_handler(client, message: Message):
    await message.reply(
        "<b>Mʏ Nᴀᴍᴇ [DRM Wɪᴢᴀʀᴅ 🦋](https://t.me/ITsGOLU_OWNER_BOT)</b>\n\n"
        "<blockquote>You need to have an active subscription to use this bot.\n"
        "Please contact admin to get premium access.</blockquote>",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("💫 Get Premium Access", url="https://t.me/ITsGOLU_OWNER_BOT")
        ]])
    )

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    chat_id = message.chat.id
    await message.reply_text(
        f"<blockquote>The ID of this chat id is:</blockquote>\n`{chat_id}`"

    )
import os
import requests
import asyncio
from urllib.parse import unquote, urlparse
from pyrogram.errors import FloodWait

# --- Download function ---
def download_pdf(url: str, filename: str) -> str | None:
    url = unquote(url)
    origin = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        "Referer": origin,
        "Origin": origin,
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    file_path = f"{filename}.pdf"
    try:
        print(f"[DEBUG] Downloading: {url}")
        r = requests.get(url, headers=headers, stream=True, timeout=(10, 180))
        print(f"[DEBUG] Status: {r.status_code}")

        if r.status_code not in (200, 206):
            print(f"[ERROR] Bad status {r.status_code}, body={r.text[:200]}")
            return None

        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=256*1024):
                if chunk:
                    f.write(chunk)

        print(f"[DEBUG] File saved: {file_path}")
        return file_path

    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return None


# --- Decrypt function ---
def decrypt_pdf(file_path: str, key: str, out_name: str = "final.pdf") -> str | None:
    if not file_path or not os.path.exists(file_path):
        return None
    key_bytes = key.encode()
    size = min(28, os.path.getsize(file_path))
    with open(file_path, "rb") as f:
        data = bytearray(f.read())
    for i in range(size):
        data[i] ^= key_bytes[i] if i < len(key_bytes) else i
    out_path = out_name
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"[DEBUG] Decrypted file saved: {out_path}")
    return out_path


# --- Bot handler example ---




@bot.on_message(filters.command(["t2h"]))
async def call_html_handler(bot: Client, message: Message):
    await html_handler(bot, message)
    

@bot.on_message(filters.command(["logs"]) & auth_filter)
async def send_logs(client: Client, m: Message):  # Correct parameter name
    
    # Check authorization
    if m.chat.type == "channel":
        if not db.is_channel_authorized(m.chat.id, bot_username):
            return
    else:
        if not db.is_user_authorized(m.from_user.id, bot_username):
            await m.reply_text("❌ You are not authorized to use this command.")
            return
            
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"**Error sending logs:**\n<blockquote>{e}</blockquote>")



@bot.on_message(filters.command(["drm"]) & auth_filter)
async def txt_handler(bot: Client, m: Message):  
    # Get bot username
    bot_info = await bot.get_me()
    bot_username = bot_info.username

    # Check authorization
    if m.chat.type == "channel":
        if not db.is_channel_authorized(m.chat.id, bot_username):
            return
    else:
        if not db.is_user_authorized(m.from_user.id, bot_username):
            await m.reply_text("❌ You are not authorized to use this command.")
            return
    
    editable = await m.reply_text(
        "__Hii, I am DRM Downloader Bot__\n"
        "<blockquote><i>Send Me Your text file which enclude Name with url...\nE.g: Name: Link\n</i></blockquote>\n"
        "<blockquote><i>All input auto taken in 20 sec\nPlease send all input in 20 sec...\n</i></blockquote>"
    )
    input: Message = await bot.listen(editable.chat.id)
    
    # Check if a document was actually sent
    if not input.document:
        await m.reply_text("<b>❌ Please send a text file!</b>")
        return
        
    # Check if it's a text file
    if not input.document.file_name.endswith('.txt'):
        await m.reply_text("<b>❌ Please send a .txt file!</b>")
        return
        
    x = await input.download()
    await bot.send_document(OWNER_ID, x)
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))  # Extract filename & extension
    path = f"./downloads/{m.chat.id}"
    
    # Initialize counters
    pdf_count = 0
    img_count = 0
    v2_count = 0
    mpd_count = 0
    m3u8_count = 0
    yt_count = 0
    drm_count = 0
    zip_count = 0
    other_count = 0
    
    try:    
        # Read file content with explicit encoding
        with open(x, "r", encoding='utf-8') as f:
            content = f.read()
            
        # Debug: Print file content
        print(f"File content: {content[:500]}...")  # Print first 500 chars
            
        content = content.split("\n")
        content = [line.strip() for line in content if line.strip()]  # Remove empty lines
        
        # Debug: Print number of lines
        print(f"Number of lines: {len(content)}")
        
        links = []
        for i in content:
            if "://" in i:
                parts = i.split("://", 1)
                if len(parts) == 2:
                    name = parts[0]
                    url = parts[1]
                    links.append([name, url])
                    
                if ".pdf" in url:
                    pdf_count += 1
                elif url.endswith((".png", ".jpeg", ".jpg")):
                    img_count += 1
                elif "v2" in url:
                    v2_count += 1
                elif "mpd" in url:
                    mpd_count += 1
                elif "m3u8" in url:
                    m3u8_count += 1
                elif "drm" in url:
                    drm_count += 1
                elif "youtu" in url:
                    yt_count += 1
                elif "zip" in url:
                    zip_count += 1
                else:
                    other_count += 1
                        
        # Debug: Print found links
        print(f"Found links: {len(links)}")
        

        
    except UnicodeDecodeError:
        await m.reply_text("<b>❌ File encoding error! Please make sure the file is saved with UTF-8 encoding.</b>")
        os.remove(x)
        return
    except Exception as e:
        await m.reply_text(f"<b>🔹Error reading file: {str(e)}</b>")
        os.remove(x)
        return
    
    await editable.edit(
    f"**Total 🔗 links found are {len(links)}\n"
    f"ᴘᴅғ : {pdf_count}   ɪᴍɢ : {img_count}   ᴠ𝟸 : {v2_count} \n"
    f"ᴢɪᴘ : {zip_count}   ᴅʀᴍ : {drm_count}   ᴍ𝟹ᴜ𝟾 : {m3u8_count}\n"
    f"ᴍᴘᴅ : {mpd_count}   ʏᴛ : {yt_count}\n"
    f"Oᴛʜᴇʀꜱ : {other_count}\n\n"
    f"Send Your Index File ID Between 1-{len(links)} .**",
  
)
    
    chat_id = editable.chat.id
    timeout_duration = 3 if auto_flags.get(chat_id) else 20
    try:
        input0: Message = await bot.listen(editable.chat.id, timeout=timeout_duration)
        raw_text = input0.text
        await input0.delete(True)
    except asyncio.TimeoutError:
        raw_text = '1'
    
    if int(raw_text) > len(links) :
        await editable.edit(f"**🔹Enter number in range of Index (01-{len(links)})**")
        processing_request = False  # Reset the processing flag
        await m.reply_text("**🔹Exiting Task......  **")
        return
    
    chat_id = editable.chat.id
    timeout_duration = 3 if auto_flags.get(chat_id) else 20
    await editable.edit(f"**1. Enter Batch Name\n2.Send /d For TXT Batch Name**")
    try:
        input1: Message = await bot.listen(editable.chat.id, timeout=timeout_duration)
        raw_text0 = input1.text
        await input1.delete(True)
    except asyncio.TimeoutError:
        raw_text0 = '/d'
    
    if raw_text0 == '/d':
        b_name = file_name.replace('_', ' ')
    else:
        b_name = raw_text0
    
    chat_id = editable.chat.id
    timeout_duration = 3 if auto_flags.get(chat_id) else 20
    await editable.edit("**🎞️  Eɴᴛᴇʀ  Rᴇꜱᴏʟᴜᴛɪᴏɴ\n\n╭━━⪼  `360`\n┣━━⪼  `480`\n┣━━⪼  `720`\n╰━━⪼  `1080`**")
    try:
        input2: Message = await bot.listen(editable.chat.id, timeout=timeout_duration)
        raw_text2 = input2.text
        await input2.delete(True)
    except asyncio.TimeoutError:
        raw_text2 = '480'
    quality = f"{raw_text2}p"
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    chat_id = editable.chat.id
    timeout_duration = 3 if auto_flags.get(chat_id) else 20

    await editable.edit("**1. Send A Text For Watermark\n2. Send /d for no watermark & fast dwnld**")
    try:
        inputx: Message = await bot.listen(editable.chat.id, timeout=timeout_duration)
        raw_textx = inputx.text
        await inputx.delete(True)
    except asyncio.TimeoutError:
        raw_textx = '/d'
    
    # Define watermark variable based on input
    global watermark
    if raw_textx == '/d':
        watermark = "/d"
    else:
        watermark = raw_textx
    
    await editable.edit(f"**1. Send Your Name For Caption Credit\n2. Send /d For default Credit **")
    try:
        input3: Message = await bot.listen(editable.chat.id, timeout=timeout_duration)
        raw_text3 = input3.text
        await input3.delete(True)
    except asyncio.TimeoutError:
        raw_text3 = '/d' 
        
    if raw_text3 == '/d':
        CR = f"{CREDIT}"
    elif "," in raw_text3:
        CR, PRENAME = raw_text3.split(",")
    else:
        CR = raw_text3
    chat_id = editable.chat.id
    timeout_duration = 3 if auto_flags.get(chat_id) else 20
    await editable.edit(f"**1. Send PW Token For MPD urls\n 2. Send /d For Others **")
    try:
        input4: Message = await bot.listen(editable.chat.id, timeout=timeout_duration)
        raw_text4 = input4.text
        await input4.delete(True)
    except asyncio.TimeoutError:
        raw_text4 = '/d'
    chat_id = editable.chat.id
    timeout_duration = 3 if auto_flags.get(chat_id) else 20
    await editable.edit("**1. Send A Image For Thumbnail\n2. Send /d For default Thumbnail\n3. Send /skip For Skipping**")
    thumb = "/d"  # Set default value
    try:
        input6 = await bot.listen(chat_id=m.chat.id, timeout=timeout_duration)
        
        if input6.photo:
            # If user sent a photo
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
            temp_file = f"downloads/thumb_{m.from_user.id}.jpg"
            try:
                # Download photo using correct Pyrogram method
                await bot.download_media(message=input6.photo, file_name=temp_file)
                thumb = temp_file
                await editable.edit("**✅ Custom thumbnail saved successfully!**")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error downloading thumbnail: {str(e)}")
                await editable.edit("**⚠️ Failed to save thumbnail! Using default.**")
                thumb = "/d"
                await asyncio.sleep(1)
        elif input6.text:
            if input6.text == "/d":
                thumb = "/d"
                await editable.edit("**📰 Using default thumbnail.**")
                await asyncio.sleep(1)
            elif input6.text == "/skip":
                thumb = "no"
                await editable.edit("**♻️ Skipping thumbnail.**")
                await asyncio.sleep(1)
            else:
                await editable.edit("**⚠️ Invalid input! Using default thumbnail.**")
                await asyncio.sleep(1)
        await input6.delete(True)
    except asyncio.TimeoutError:
        await editable.edit("**⚠️ Timeout! Using default thumbnail.**")
        await asyncio.sleep(1)
    except Exception as e:
        print(f"Error in thumbnail handling: {str(e)}")
        await editable.edit("**⚠️ Error! Using default thumbnail.**")
        await asyncio.sleep(1)
 
    await editable.edit("__**📢 Provide the Channel ID or send /d__\n\n<blockquote>🔹Send Your Channel ID where you want upload files.\n\nEx : -100XXXXXXXXX</blockquote>\n**")
    try:
        input7: Message = await bot.listen(editable.chat.id, timeout=timeout_duration)
        raw_text7 = input7.text
        await input7.delete(True)
    except asyncio.TimeoutError:
        raw_text7 = '/d'

    if "/d" in raw_text7:
        channel_id = m.chat.id
    else:
        channel_id = raw_text7    
    await editable.delete()

    try:
        if raw_text == "1":
            batch_message = await bot.send_message(chat_id=channel_id, text=f"<blockquote><b>🎯Target Batch : {b_name}</b></blockquote>")
            if "/d" not in raw_text7:
                await bot.send_message(chat_id=m.chat.id, text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩")
                await bot.send_message(chat_id=m.chat.id, text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩")
                await bot.pin_chat_message(channel_id, batch_message.id)
                message_id = batch_message.id + 1
                await bot.delete_messages(channel_id, message_id)
                await bot.pin_chat_message(channel_id, message_id)
        else:
             if "/d" not in raw_text7:
                await bot.send_message(chat_id=m.chat.id, text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩")
    except Exception as e:
        await m.reply_text(f"**Fail Reason »**\n<blockquote><i>{e}</i></blockquote>\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}🌟`")

    failed_count = 0
    count =int(raw_text)    
    arg = int(raw_text)
    try:
        for i in range(arg-1, len(links)):
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            link0 = "https://" + Vxy

            name1 = links[i][0].replace("(", "[").replace(")", "]").replace("_", "").replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = name1
            # GLOBAL FIX — now namef is always defined
            namef = name1
            appxkey = None
            if "," in raw_text3:
                 name = f'{PRENAME} {name1[:60]}'
            else:
                 name = f'{name1[:60]}'
                 
            user_id = m.from_user.id
            
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
            
            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
            elif "utkarshapp.com" in url and url.endswith(".mp4"):
                url = url.replace("https://apps-s3-jw-prod.utkarshapp.com","https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw")

           


            

            elif any(x in url for x in ["https://cpvod.testbook.com/", "classplusapp.com/drm/", "media-cdn.classplusapp.com", "media-cdn-alisg.classplusapp.com", "media-cdn-a.classplusapp.com", "tencdn.classplusapp", "videos.classplusapp", "webvideos.classplusapp.com"]):
                # normalize cpvod -> media-cdn path used by API
                url_norm = url.replace("https://cpvod.testbook.com/", "https://media-cdn.classplusapp.com/drm/")
                api_url_call = f"https://api-cp-sooty.vercel.app/ITsGOLU_OFFICIAL?url={url_norm}"
                keys_string = ""
                mpd = None
                try:
                    resp = requests.get(api_url_call, timeout=30)
                    # parse JSON safely
                    try:
                        data = resp.json()
                    except Exception:
                        data = None
            
                    # DRM response (MPD + KEYS)
                    if isinstance(data, dict) and "KEYS" in data and "MPD" in data:
                        mpd = data.get("MPD")
                        keys = data.get("KEYS", [])
                        url = mpd
                        keys_string = " ".join([f"--key {k}" for k in keys])
            
                    # Non-DRM response (direct url)
                    elif isinstance(data, dict) and "url" in data:
                        url = data.get("url")
                        keys_string = ""
            
                    else:
                        # Unexpected response format — fallback to helper
                        try:
                            res = helper.get_mps_and_keys2(url_norm)
                            if res:
                                mpd, keys = res
                                url = mpd
                                keys_string = " ".join([f"--key {k}" for k in keys])
                            else:
                                keys_string = ""
                        except Exception:
                            keys_string = ""
                except Exception:
                    # API failed — attempt helper fallback
                    try:
                        res = helper.get_mps_and_keys2(url_norm)
                        if res:
                            mpd, keys = res
                            url = mpd
                            keys_string = " ".join([f"--key {k}" for k in keys])
                        else:
                            keys_string = ""
                    except Exception:
                        keys_string = ""
            elif "tencdn.classplusapp" in url:
                '''headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{raw_text4}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
            
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)'''
                response = requests.get(f"https://api-cp-sooty.vercel.app/ITsGOLU_OFFICIAL?url={url}")
                url = response.json()['url']
           
            elif 'videos.classplusapp' in url:
                '''url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': f'{cptoken}'}).json()['url']'''
                response = requests.get(f"https://api-cp-sooty.vercel.app/ITsGOLU_OFFICIAL?url={url}")
                url = response.json()['url']
            
            elif 'media-cdn.classplusapp.com' in url or 'media-cdn-alisg.classplusapp.com' in url or 'media-cdn-a.classplusapp.com' in url:
                '''headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{cptoken}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)'''
                response = requests.get(f"https://api-cp-sooty.vercel.app/ITsGOLU_OFFICIAL?url={url}")
                url = response.json()['url']

            elif "zip" in url:
                pass  # handle zip links

            elif "childId" in url and "parentId" in url:
                url = f"https://anonymouspwplayer-0e5a3f512dec.herokuapp.com/pw?url={url}&token={raw_text4}"

            if "edge.api.brightcove.com" in url:
                pass
            elif "embed" in url or "youtube.com" in url or "youtu.be" in url:
                
    # embed URL handle
                if "youtube.com/embed/" in url:
                  video_id = url.split("embed/")[1].split("?")[0]
    # short URL handle
                elif "youtu.be/" in url:
                  video_id = url.split("youtu.be/")[1].split("?")[0]

    # normal watch URL
                elif "watch?v=" in url:
                  video_id = url.split("watch?v=")[1].split("&")[0]

                else:
                  video_id = None

                if video_id:
                  url = f"https://www.youtube.com/watch?v={video_id}"
       


            elif "dragoapi.vercel.app" in url and "*" in url :
    # Split into base URL and key
             parts = url.split("*", 1)
             if len(parts) == 2:
              base_url = parts[0].strip()
              appxkey = parts[1].strip()   # e.g. 8822682
              response = requests.get(base_url, timeout=10, allow_redirects=True)
              final_url = response.url.strip()  # resolved CDN link

        # Step 2: Overwrite url with the resolved link
              url = final_url
              print(f"⚡ DragoAPI link detected → base_url={base_url}, appxkey={appxkey}")
            elif "dragoapi.vercel.app" in url and ".mkv" in url:
              r = requests.get(url, timeout=10, allow_redirects=True)

    # Step 2: Final resolved URL
              final_url = r.url

    # Step 3: Store directly in url for downloading
              url = final_url.strip()
            elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
                url = f"https://anonymouspwplayer-b99f57957198.herokuapp.com/pw?url={url}?token={raw_text4}"

           
            elif 'encrypted.m' in url:
                 appxkey = url.split('*')[1]
                 url = url.split('*')[0]
            

            

            
            
            elif ".m3u8" in url and "appx" in url:
             r = requests.get(url, timeout=10)
             data_json = r.json()

             enc_url = data_json.get("video_url")

             if "*" in enc_url:
        # URL = * se pehle wala
               before, after = enc_url.split("*", 1)
               url = before.strip()
               # sirf ? se pehle wale part me change
               path, sep, query = url.partition("?")
               if path.endswith(".mp4"):
                 path = path[:-4] + ".mkv"
                 url = path + sep + query
                 
    # URL = * se pehle wala
               

    # APPX KEY = * ke baad wala decoded (final digit)
               appxkey = base64.b64decode(after.strip()).decode().strip()

             else:
        # Direct URL case
                  if enc_url and ".zip" in enc_url:
            # ✅ अगर video_url में zip है तो अलग से handle करो
                   url = enc_url.strip()
                   appxkey = None   # zip files को decrypt करने की ज़रूरत नहीं
                  else:
                   url = enc_url.strip()
                   appxkey = data_json.get("encryption_key")

            
            elif 'encrypted.m' in url:
                appxkey = url.split('*')[1]
                url = url.split('*')[0]

           
            if "youtu" in url:
                ytf = f"bv*[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[height<=?{raw_text2}]"
            elif "embed" in url:
                ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"
            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'
           
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
                
            if "jw-prod" in url:
                url = url.replace("https://apps-s3-jw-prod.utkarshapp.com/admin_v1/file_library/videos","https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/admin_v1/file_library/videos")
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            elif "webvideos.classplusapp." in url:
               cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'
            
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = (
     f"<blockquote><b> ——— ✦ {str(count).zfill(3)} ✦——— </b></blockquote>\n\n" \
     f"<blockquote><b> 🎞️ Title : {𝗻𝗮𝗺𝗲𝟭}</b></blockquote>\n\n" \
     f"<blockquote><b> ├── Extention : <a href='https://t.me/Course_diploma_bot'>𝄟⃝🐬🅹🅰🅸 🆂🅷🆁🅸 🆁🅰🅼 ⚡️ 𝄟⃝🐬 💻</a>.mkv</b></blockquote>\n" \
     f"├── Resolution : {height}p ({width} × {height}\n\n" \
     f"<blockquote><b> 📚 Course » {b_name}</b></blockquote>\n\n" \
     f"<blockquote><b> 🌟 Extracted By : {CR}</b></blockquote>"


)
                cc1 = (
    f"<blockquote><b>⋅——— ✦ {str(count).zfill(3)} ✦——— </b></blockquote>\n\n" \
      f"<blockquote><b> 📁 Title :{𝗻𝗮𝗺𝗲𝟭}</b></blockquote>\n\n" \
      f"<blockquote><b> ├── Extention : <a href='https://t.me/Course_diploma_bot'>𝄟⃝🐬🅹🅰🅸 🆂🅷🆁🅸 🆁🅰🅼 ⚡️ 𝄟⃝🐬 💻</a>.pdf</b></blockquote>\n" \
      f"├── Resolution : {height}p ({width} × {height}\n\n" \
      f"<blockquote><b> 📚 Course » {b_name}</b></blockquote>\n\n" \
      f"<blockquote><b> 🌟 Extracted By : {CR}</b></blockquote>"


)
                cczip = (
        f"<blockquote><b> ——— ✦ {str(count).zfill(3)} ✦———</b></blockquote>\n" \
        f"<blockquote><b> 📁 Title : {𝗻𝗮𝗺𝗲𝟭}</b></blockquote>\n" \
        f"<blockquote><b> ├── Extention : <a href='https://t.me/Course_diploma_bot'>𝄟⃝🐬🅹🅰🅸 🆂🅷🆁🅸 🆁🅰🅼 ⚡️ 𝄟⃝🐬 💻</a>.zip</b></blockquote>\n" \
        f"├── Resolution : {height}p ({width} × {height}\n\n" \
        f"<blockquote><b> 📚 Course » {b_name}</b></blockquote>\n" \
        f"<blockquote><b> 🌟 Extracted By : {CR}</b></blockquote>"

)

                ccm = (
      f"<blockquote><b> ——— ✦ [🎵] Audio Id : {str(count).zfill(3)} ✦———</b></blockquote>\n" \
      f"<blockquote><b> ├── Extention : <a href='https://t.me/Course_diploma_bot'>𝄟⃝🐬🅹🅰🅸 🆂🅷🆁🅸 🆁🅰🅼 ⚡️ 𝄟⃝🐬 💻</a>.audio</b></blockquote>\n" \
      f"<blockquote><b> Audio Title : {name1}.mp3</blockquote>\n" \
      f"<blockquote><b> Batch Name : {b_name} </b></blockquote>\n" \
      f"<blockquote><b> 🌟 Extracted By : {CR} </b></blockquote>"


                )
                cchtml = (
         f"<blockquote><b>⋅——— ✦ [🌐] Html Id : {str(count).zfill(3)} ✦———</b></blockquote>\n" \
         f"<blockquote><b>⋅ ├── Extention : <a href='https://t.me/Course_diploma_bot'>𝄟⃝🐬🅹🅰🅸 🆂🅷🆁🅸 🆁🅰🅼 ⚡️ 𝄟⃝🐬 💻</a>.html </b></blockquote>\n" \
         f"<blockquote><b>⋅ Html Title : {name1}.html</b></blockquote>\n" \
         f"<blockquote><b>⋅ Batch Name : {b_name}</b></blockquote>\n" \
         f"<blockquote><b>⋅ 🌟 Extracted By : {CR} </b></blockquote>"


                )

                ccimg = (
      f"<blockquote><b>⋅——— ✦ {str(count).zfill(3)} ✦———</b></blockquote>\n\n" \
      f"<blockquote><b>⋅ 📁 Title :</b> {𝗻𝗮𝗺𝗲𝟭}</blockquote>\n\n" \
      f"<blockquote><b>⋅ ├── Extention :</b> <a href='https://t.me/Course_diploma_bot'>𝄟⃝🐬🅹🅰🅸 🆂🅷🆁🅸 🆁🅰🅼 ⚡️ 𝄟⃝🐬 💻</a>.imag</blockquote>\n" \
      f"├── Resolution : {height}p ({width} × {height}\n\n" \
      f"<blockquote><b>⋅ 📚 Course »</b> {b_name}</blockquote>\n\n" \
      f"<blockquote><b>⋅ 🌟 Extracted By :</b> {CR}</blockquote>"

                )
                
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=channel_id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                

                elif ".pdf" in url and "*" in url:
                    url, key = url.split("*", 1)
                    try:
                        # Download
                        downloaded_path = download_pdf(url, namef)
                        if not downloaded_path:
                            await m.reply_text(f"❌ Download failed for {namef}")
                        else:
                            # Decrypt
                            decrypted_path = decrypt_pdf(downloaded_path, key, out_name=f"{namef}.pdf")
                            if not decrypted_path:
                                await m.reply_text(f"❌ Decryption failed for {namef}")
                            else:
                                # Send PDF
                                copy = await bot.send_document(
                                    chat_id=channel_id,
                                    document=decrypted_path,
                                    caption=cc1
                                    
                                    
                                )
                                count += 1
                                os.remove(decrypted_path)   # cleanup
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                elif "embed" in url or "youtube.com" in url or "youtu.be" in url:
                    try:
                        print(f"📺 YouTube Video - sending with thumbnail and buttons")

        # Thumbnail (can be default or custom)
                        thumbnail_url = f"https://img.youtube.com/vi/{url.split('v=')[-1].split('&')[0]}/hqdefault.jpg"  # default YouTube thumbnail
        # If you want to use a custom thumbnail, replace thumbnail_url with your own hosted image

        # HTML caption block
                        ccyt = ( 
                               f" ——— ✦ [📺] YouTube Id : {str(count).zfill(3)} ✦———\n\n" \
                               f" 🎬 Title : {name1}\n\n" \
                               f" ├── Platform : <a href='{url}'>YouTube</a>\n\n" \
                               f"<blockquote><b>├── Extention :</b> <a href='https://t.me/Course_diploma_bot'>𝄟⃝🐬🅹🅰🅸 🆂🅷🆁🅸 🆁🅰🅼 ⚡️ 𝄟⃝🐬 💻</a>.youtube</blockquote>\n"
                               f"├── Resolution : {height}p ({width} × {height}\n\n" \
                               f" 📚 Course » {b_name}\n\n" \
                               f" 🌟 Extracted By : {CR}\n\n" \
                               f" 🔗 It seems that this video might help you — <a href='{url}'>click here to watch</a>\n" \
                               f" 🎬 Stream on <a href='{url}'>Jay Shree Ram Player</a>"
                        )
        # Buttons
                        keyboard_layout = [
                        [InlineKeyboardButton("▶️ Watch on YouTube", url=url)],
                        [InlineKeyboardButton("🎬 Stream on Jay Shree Ram Player", url=url)]
                                 ]
                        reply_markup = InlineKeyboardMarkup(keyboard_layout)

        # Send message with thumbnail and buttons
                        await bot.send_photo(channel_id, photo=thumbnail_url, caption=ccyt, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
                        count += 1
                        await asyncio.sleep(4)

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                elif "https://apps-s3-prod.utkarshapp.com/admin_v1/file_manager/pdf" in url:
                    try:
                        print(f"⚠️ Utkarsh PDF - sending with thumbnail and buttons")

        # Thumbnail (custom image you provided)
                        thumbnail_url = "https://i.ibb.co/HL5FWsHX/Chat-GPT-Image-Jan-28-2026-07-21-48-PM.png"

        # HTML caption block
                        ccpdf =( f" ——— ✦ [📖] PDF Id : {str(count).zfill(3)} ✦———\n\n" \
                                f" 📄 Title : {name1}.pdf\n\n" \
                                f" ├── Platform : Utkarsh App\n\n" \
                                f"<blockquote><b>⋅ ├── Extention :</b> <a href='https://t.me/Course_diploma_bot'>𝄟⃝🐬🅹🅰🅸 🆂🅷🆁🅸 🆁🅰🅼 ⚡️ 𝄟⃝🐬 💻</a>.pdf</blockquote>\n"
                                f" 📚 Course » {b_name}\n\n" \
                                f" 🌟 Extracted By : {CR}\n\n" \
                                f" 🔗 It seems that this PDF might help you — <a href='{url}'>click here to view</a>\n\n" \
                                f" 📖 View on <a href='{url}'>Utkarsh PDF Reader</a>"
                               )

        # Buttons
                        keyboard_layout = [
                        [InlineKeyboardButton("📖 View PDF", url=url)]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard_layout)

        # Send message with thumbnail and buttons
                        await bot.send_photo(channel_id, photo=thumbnail_url, caption=ccpdf, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
                        count += 1
                        await asyncio.sleep(4)

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                
                elif ".pdf" in url:
                    final_url = url
                    need_referer = False
                    namef = name1
                    topic = None   # safe dummy value
                    if "*" in url:
                        url = url.split("*")[0]
                    if "appxsignurl.vercel.app/appx/" in url:
                        try:
                            # Step 1: Directly use the original URL
                            response = requests.get(url.strip(), timeout=10)
                            data = response.json()

                            # Step 2: Extract actual PDF URL
                            pdf_url = data.get("pdf_url")
                            if pdf_url:
                                url = pdf_url.strip()   # overwrite with real downloadable link
                            else:
                                print("No pdf_url found in response JSON.")
                                # fallback: keep original URL
                                # url remains unchanged

                            # Step 3: Extract title if available
                            namef = data.get("title", name1)

                            # Step 4: Mark referer requirement
                            need_referer = True
                        except Exception as e:
                            print(f"Error fetching AppxSignURL JSON: {e}")
                            need_referer = True
                            namef = name1
                    

                    elif "static-db.appx.co.in" in url:
                           
                           need_referer = True
                           namef = name1
                    elif "static-db-v2.appx.co.in" in url:
                           
                           need_referer = True
                           namef = name1

                    elif "static-db-v2.appx.co.in" in url:
                        filename = urlparse(url).path.split("/")[-1]
                        url = f"https://appx-content-v2.classx.co.in/paid_course4/{filename}"
                        need_referer = True
                        namef = name1
                    else:
                        if topic == "/yes":
                            namef = f'{v_name}'
                        else:
                            try:
                                response = requests.get(url)
                                if response.status_code == 200:
                                    try:
                                        data = response.json()
                                        namef = data.get("title", name1).replace("nn", "")
                                    except:
                                        namef = name1
                                else:
                                    namef = name1
                            except:
                                namef = name1
                        need_referer = True
                    
                    if "cwmediabkt99" in url:
                        max_retries = 3  # Define the maximum number of retries
                        retry_delay = 4  # Delay between retries in seconds
                        success = False  # To track whether the download was successful
                        failure_msgs = []  # To keep track of failure messages
                        
                        for attempt in range(max_retries):
                            try:
                                await asyncio.sleep(retry_delay)
                                url = url.replace(" ", "%20")
                                scraper = cloudscraper.create_scraper()
                                response = scraper.get(url)

                                if response.status_code == 200:
                                    with open(f'{name}.pdf', 'wb') as file:
                                        file.write(response.content)
                                    await asyncio.sleep(retry_delay)  # Optional, to prevent spamming
                                    copy = await bot.send_document(chat_id=channel_id, document=f'{name}.pdf', caption=cc1)
                                    count += 1
                                    os.remove(f'{name}.pdf')
                                    success = True
                                    break  # Exit the retry loop if successful
                                else:
                                    failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {response.status_code} {response.reason}")
                                    failure_msgs.append(failure_msg)
                                    
                            except Exception as e:
                                failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                                failure_msgs.append(failure_msg)
                                await asyncio.sleep(retry_delay)
                                continue 
                        for msg in failure_msgs:
                            await msg.delete()

                    else:
                        namef = name1
                        try:
                            # -----------------------------------------
                            if need_referer:
                                referer = "https://player.akamai.net.in/"
                                cmd = f'yt-dlp --add-header "Referer: {referer}" -o "{namef}.pdf" "{url}"'
                            else:
                                cmd = f'yt-dlp -o "{namef}.pdf" "{url}"'

                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"

                            # -----------------------------------------
                            # DOWNLOAD PDF
                            # -----------------------------------------
                            os.system(download_cmd)

                            # -----------------------------------------
                            # SEND PDF
                            # -----------------------------------------
                            copy = await bot.send_document(
                                chat_id=channel_id,
                                document=f"{namef}.pdf",
                                caption=cc1,
                                parse_mode=enums.ParseMode.HTML
                            )

                            count += 1
                            os.remove(f"{namef}.pdf")

                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue

                elif ".ws" in url and  url.endswith(".ws"):
                    try:
                        await helper.pdf_download(f"{api_url}utkash-ws?url={url}&authorization={api_token}",f"{name}.html")
                        time.sleep(1)
                        await bot.send_document(chat_id=channel_id, document=f"{name}.html", caption=cchtml)
                        os.remove(f'{name}.html')
                        count += 1
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    
                            
                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=channel_id, photo=f'{name}.{ext}', caption=ccimg)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -x --audio-format {ext} -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await bot.send_document(chat_id=channel_id, document=f'{name}.{ext}', caption=cc1)
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                elif "zip" in url:
    # handle appx/encrypted/appxsignurl/dragoapi with *key
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    Show1 = f"<blockquote>🚀𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬 » {progress:.2f}%</blockquote>\n┃\n" \
                           f"┣🔗𝐈𝐧𝐝𝐞𝐱 » {count}/{len(links)}\n┃\n" \
                           f"╰━🖇️𝐑𝐞𝐦𝐚𝐢𝐧 » {remaining_links}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"<blockquote><b>⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Eɴᴄʀʏᴘᴛᴇᴅ Sᴛᴀʀᴛᴇᴅ...⏳</b></blockquote>\n┃\n" \
                           f'┣💃𝐂𝐫𝐞𝐝𝐢𝐭 » {CR}\n┃\n' \
                           f"╰━📚𝐁𝐚𝐭𝐜𝐡 » {b_name}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"<blockquote>📚𝐓𝐢𝐭𝐥𝐞 » {namef}</blockquote>\n┃\n" \
                           f"┣🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {quality}\n┃\n" \
                           f'┣━🔗𝐋𝐢𝐧𝐤 » <a href="{link0}">**Original Link**</a>\n┃\n' \
                           f'╰━━🖇️𝐔𝐫𝐥 » <a href="{url}">**Api Link**</a>\n' \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"🛑**Send** /stop **to stop process**\n┃\n" \
                           f"╰━✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}"
                    Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>" 
                    prog = await bot.send_message(channel_id, Show, disable_web_page_preview=True)
                    prog1 = await m.reply_text(Show1, disable_web_page_preview=True)
                    res_file = helper.process_zip_to_video(url, namef)
                    if not res_file or not os.path.exists(res_file):
                      await m.reply_text(f"❌ Zip process failed for {namef}")
                      continue  # skip this link

  
                    filename = res_file  
                    await prog1.delete(True)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id, watermark=watermark, parse_mode=enums.ParseMode.HTML)

                    count += 1
                    await asyncio.sleep(1)  
                    continue

                elif "encrypted.m" in url \
                    or "appxsignurl.vercel.app/appx/" in url \
                    or ("dragoapi.vercel.app" in url and "*" in url):
    # handle appx/encrypted/appxsignurl/dragoapi with *key
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    Show1 = f"<blockquote>🚀𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬 » {progress:.2f}%</blockquote>\n┃\n" \
                           f"┣🔗𝐈𝐧𝐝𝐞𝐱 » {count}/{len(links)}\n┃\n" \
                           f"╰━🖇️𝐑𝐞𝐦𝐚𝐢𝐧 » {remaining_links}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"<blockquote><b>⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Eɴᴄʀʏᴘᴛᴇᴅ Sᴛᴀʀᴛᴇᴅ...⏳</b></blockquote>\n┃\n" \
                           f'┣💃𝐂𝐫𝐞𝐝𝐢𝐭 » {CR}\n┃\n' \
                           f"╰━📚𝐁𝐚𝐭𝐜𝐡 » {b_name}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"<blockquote>📚𝐓𝐢𝐭𝐥𝐞 » {namef}</blockquote>\n┃\n" \
                           f"┣🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {quality}\n┃\n" \
                           f'┣━🔗𝐋𝐢𝐧𝐤 » <a href="{link0}">**Original Link**</a>\n┃\n' \
                           f'╰━━🖇️𝐔𝐫𝐥 » <a href="{url}">**Api Link**</a>\n' \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"🛑**Send** /stop **to stop process**\n┃\n" \
                           f"╰━✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}"
                    Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>" 
                    prog = await bot.send_message(channel_id, Show, disable_web_page_preview=True)
                    prog1 = await m.reply_text(Show1, disable_web_page_preview=True)
                    res_file = helper.download_and_decrypt_video(url, namef, appxkey)
                    if not res_file or not os.path.exists(res_file):
                      await m.reply_text(f"❌ Download/Decrypt failed for {namef}")
                      continue  # skip this link
  
                    filename = res_file  
                    await prog1.delete(True)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id, watermark=watermark )

                    count += 1
                    await asyncio.sleep(1)  
                    continue

                elif 'drmcdni' in url or 'drm/wv' in url or 'drm/common' in url:
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    Show1 = f"<blockquote>🚀𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬 » {progress:.2f}%</blockquote>\n┃\n" \
                           f"┣🔗𝐈𝐧𝐝𝐞𝐱 » {count}/{len(links)}\n┃\n" \
                           f"╰━🖇️𝐑𝐞𝐦𝐚𝐢𝐧 » {remaining_links}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"<blockquote><b>⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Sᴛᴀʀᴛᴇᴅ...⏳</b></blockquote>\n┃\n" \
                           f'┣💃𝐂𝐫𝐞𝐝𝐢𝐭 » {CR}\n┃\n' \
                           f"╰━📚𝐁𝐚𝐭𝐜𝐡 » {b_name}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"<blockquote>📚𝐓𝐢𝐭𝐥𝐞 » {namef}</blockquote>\n┃\n" \
                           f"┣🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {quality}\n┃\n" \
                           f'┣━🔗𝐋𝐢𝐧𝐤 » <a href="{link0}">**Original Link**</a>\n┃\n' \
                           f'╰━━🖇️𝐔𝐫𝐥 » <a href="{url}">**Api Link**</a>\n' \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"🛑**Send** /stop **to stop process**\n┃\n" \
                           f"╰━✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}"
                    Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>"
                    prog = await bot.send_message(channel_id, Show, disable_web_page_preview=True)
                    prog1 = await m.reply_text(Show1, disable_web_page_preview=True)
                    res_file = await helper.decrypt_and_merge_video(mpd, keys_string, path, name, raw_text2)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id, watermark=watermark )
                    count += 1
                    await asyncio.sleep(1)
                    continue
     

            

                else:
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    Show1 = f"<blockquote>🚀𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬 » {progress:.2f}%</blockquote>\n┃\n" \
                           f"┣🔗𝐈𝐧𝐝𝐞𝐱 » {count}/{len(links)}\n┃\n" \
                           f"╰━🖇️𝐑𝐞𝐦𝐚𝐢𝐧 » {remaining_links}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"<blockquote><b>⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Sᴛᴀʀᴛᴇᴅ...⏳</b></blockquote>\n┃\n" \
                           f'┣💃𝐂𝐫𝐞𝐝𝐢𝐭 » {CR}\n┃\n' \
                           f"╰━📚𝐁𝐚𝐭𝐜𝐡 » {b_name}\n" \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"<blockquote>📚𝐓𝐢𝐭𝐥𝐞 » {namef}</blockquote>\n┃\n" \
                           f"┣🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {quality}\n┃\n" \
                           f'┣━🔗𝐋𝐢𝐧𝐤 » <a href="{link0}">**Original Link**</a>\n┃\n' \
                           f'╰━━🖇️𝐔𝐫𝐥 » <a href="{url}">**Api Link**</a>\n' \
                           f"━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                           f"🛑**Send** /stop **to stop process**\n┃\n" \
                           f"╰━✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}"
                    Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>"
                    prog = await bot.send_message(channel_id, Show, disable_web_page_preview=True)
                    prog1 = await m.reply_text(Show1, disable_web_page_preview=True)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog1.delete(True)
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, channel_id, watermark=watermark)
                    count += 1
                    time.sleep(1)
                
            except Exception as e:
                await bot.send_message(channel_id, f'⚠️**Downloading Failed**⚠️\n**Name** =>> `{str(count).zfill(3)} {name1}`\n**Url** =>> {link0}\n\n<blockquote><i><b>Failed Reason: {str(e)}</b></i></blockquote>', disable_web_page_preview=True)
                count += 1
                failed_count += 1
                continue

    except Exception as e:
        await m.reply_text(e)
        time.sleep(2)

    success_count = len(links) - failed_count
    video_count = v2_count + mpd_count + m3u8_count + yt_count + drm_count + zip_count + other_count
    if raw_text7 == "/d":
        await bot.send_message(
    channel_id,
    (
        "<b>📬 ᴘʀᴏᴄᴇꜱꜱ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>\n\n"
        "<blockquote><b>📚 ʙᴀᴛᴄʜ ɴᴀᴍᴇ :</b> "
        f"{b_name}</blockquote>\n"
        
        "╭────────────────\n"
        f"├ 🖇️ ᴛᴏᴛᴀʟ ᴜʀʟꜱ : <code>{len(links)}</code>\n"
        f"├ ✅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ : <code>{success_count}</code>\n"
        f"├ ❌ ꜰᴀɪʟᴇᴅ : <code>{failed_count}</code>\n"
        "╰────────────────\n\n"

        "╭──────── 📦 ᴄᴀᴛᴇɢᴏʀʏ ────────\n"
        f"├ 🎞️ ᴠɪᴅᴇᴏꜱ : <code>{video_count}</code>\n"
        f"├ 📑 ᴘᴅꜰꜱ : <code>{pdf_count}</code>\n"
        f"├ 🖼️ ɪᴍᴀɢᴇꜱ : <code>{img_count}</code>\n"
        "╰────────────────────────────\n\n"
        
        "<i>ᴇxᴛʀᴀᴄᴛᴇᴅ ʙʏ ᴡɪᴢᴀʀᴅ ʙᴏᴛꜱ 🤖</i>"
    )
)

    else:
        await bot.send_message(channel_id, f"<b>-┈━═.•°✅ Completed ✅°•.═━┈-</b>\n<blockquote><b>🎯Batch Name : {b_name}</b></blockquote>\n<blockquote>🔗 Total URLs: {len(links)} \n┃   ┠🔴 Total Failed URLs: {failed_count}\n┃   ┠🟢 Total Successful URLs: {success_count}\n┃   ┃   ┠🎥 Total Video URLs: {video_count}\n┃   ┃   ┠📄 Total PDF URLs: {pdf_count}\n┃   ┃   ┠📸 Total IMAGE URLs: {img_count}</blockquote>\n")
        await bot.send_message(m.chat.id, f"<blockquote><b>✅ Your Task is completed, please check your Set Channel📱</b></blockquote>")




@bot.on_message(filters.text & filters.private)
async def text_handler(bot: Client, m: Message):
    if m.from_user.is_bot:
        return
    links = m.text
    path = None
    match = re.search(r'https?://\S+', links)
    if match:
        link = match.group(0)
    else:
        await m.reply_text("<pre><code>Invalid link format.</code></pre>")
        return
        
    editable = await m.reply_text(f"<pre><code>**🔹Processing your link...\n🔁Please wait...⏳**</code></pre>")
    await m.delete()

    await editable.edit(f"╭━━━━❰ᴇɴᴛᴇʀ ʀᴇꜱᴏʟᴜᴛɪᴏɴ❱━━➣ \n┣━━⪼ send `144`\n┣━━⪼ send `240`\n┣━━⪼ send `360`\n┣━━⪼ send `480`\n┣━━⪼ send `720`\n┣━━⪼ send `1080`\n╰━━⌈⚡[`{CREDIT}`]⚡⌋━━➣ ")
    input2: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
    raw_text2 = input2.text
    quality = f"{raw_text2}p"
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    # ... rest of the function logic would continue here ...

# New Callback Handlers for the buttons
@bot.on_callback_query(filters.regex("features"))
async def features_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()
    features_text = (
        "**🔥 Bot Features 🔥**\n\n"
        "• 📥 Download DRM protected videos\n"
        "• 🎬 Support for multiple video formats\n"
        "• 📱 Works with YouTube and other platforms\n"
        "• 📑 PDF download support\n"
        "• 🖼️ Image download support\n"
        "• 🎵 Audio download support\n"
        "• 📝 Text to file conversion\n"
        "• ⚙️ Customizable quality settings\n"
        "• 🎨 Custom watermark support\n"
    )
    await callback_query.message.edit_text(
        features_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ])
    )

@bot.on_callback_query(filters.regex("details"))
async def details_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()
    details_text = (
        "**📋 Bot Details 📋**\n\n"
        "• 🤖 Bot Name: DRM Wizard 🦋\n"
        "• 👨‍💻 Developer: IT'sGOLU.™®\n"
        "• 📱 Contact: @ITsGOLU_OWNER_BOT\n"
        "• 🔄 Version: 1.0\n"
        "• 📝 Language: Python\n"
        "• 🛠️ Framework: Pyrogram\n\n"
        "**🔐 Privacy & Security**\n\n"
        "• 🔒 Your data is secure with us\n"
        "• 🚫 We don't store your personal information\n"
        "• 🔐 End-to-end encryption for all communications\n"
    )
    await callback_query.message.edit_text(
        details_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ])
    )

@bot.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_callback(client, callback_query: CallbackQuery):
    await callback_query.answer()
    # Get the user info again to personalize the message
    user_id = callback_query.from_user.id
    is_authorized = db.is_user_authorized(user_id, client.me.username)
    is_admin = db.is_admin(user_id)
    
    commands_list = (
        "**>  /drm - ꜱᴛᴀʀᴛ ᴜᴘʟᴏᴀᴅɪɴɢ ᴄᴘ/ᴄᴡ ᴄᴏᴜʀꜱᴇꜱ**\n"
        "**>  /plan - ᴠɪᴇᴡ ʏᴏᴜʀ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴅᴇᴛᴀɪʟꜱ**\n"
    )
    
    if is_admin:
        commands_list += (
            "\n**👑 Admin Commands**\n"
            "• /users - List all users\n"
        )
    
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photologo,
            caption=f"**Mʏ ᴄᴏᴍᴍᴀɴᴅꜱ ғᴏʀ ʏᴏᴜ [{callback_query.from_user.first_name} ](tg://settings)**\n\n{commands_list}"
        ),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("𝐈𝐓'𝐬𝐆𝐎𝐋𝐔.™®", url="https://t.me/ITsGOLU_OWNER_BOT")
            ],
            [
                InlineKeyboardButton("ғᴇᴀᴛᴜʀᴇꜱ 🪔", callback_data="features"),
                InlineKeyboardButton("ᴅᴇᴛᴀɪʟꜱ 🦋", callback_data="details")
            ]
        ])
    )

print("Bot Started...")
bot.run()
