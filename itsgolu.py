import os
import re
import time
import mmap
import datetime
import aiohttp
import aiofiles
import asyncio
import logging
import requests
import tgcrypto
import subprocess
import concurrent.futures
from math import ceil
from utils import progress_bar
from pyrogram import Client, filters
from pyrogram.types import Message
from io import BytesIO
from pathlib import Path  
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
import math
import m3u8
from urllib.parse import urljoin
from vars import *  # Add this import
from db import Database

import requests

def create_session():
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=10,
        pool_maxsize=10,
        max_retries=3
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
import os
import requests
import zipfile
import subprocess
import tempfile
import shutil

# RAW FILE DOWNLOAD
# ==============================
import os
import yt_dlp
import os
import asyncio
import subprocess

import os
import subprocess

import os
import subprocess
import os
import subprocess

def download_appx_m3u8(url: str, name: str) -> str | None:
    """
    Download m3u8 (APPX) using ffmpeg with max parallel requests for 15x speed.
    Works for video + audio.
    """
    os.makedirs("downloads", exist_ok=True)
    output = f"downloads/{name}.mp4"

    headers = (
        "User-Agent: Mozilla/5.0 (Linux; Android 13)\r\n"
        "Referer: https://player.akamai.net.in/\r\n"
        "Origin: https://akstechnicalclasses.classx.co.in\r\n"
        "Accept: */*\r\n"
    )

    cmd = [
        "ffmpeg",
        "-y",

        # 🔥 FAST NETWORK
        "-headers", headers,
        "-http_persistent", "1",
        "-multiple_requests", "1",
        "-reconnect", "1",
        "-reconnect_at_eof", "1",
        "-reconnect_streamed", "1",
        "-reconnect_delay_max", "5",

        # 🔥 THREADS = 16 for 15x speed
        "-threads", "16",

        # 🔥 INPUT
        "-i", url,

        # 🔥 FIX PLAYBACK ISSUES
        "-map", "0:v:0",
        "-map", "0:a?",
        "-c:v", "copy",
        "-c:a", "aac",
        "-bsf:a", "aac_adtstoasc",

        # 🔥 CRITICAL FOR MOBILE / TELEGRAM
        "-movflags", "+faststart",

        output
    ]

    print(f"⚡ Running ffmpeg for {name} with 15x speed...")
    process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if process.returncode == 0 and os.path.exists(output):
        print("✅ APPX 15x download OK:", output)
        return output
    else:
        print("❌ APPX ffmpeg error:\n", process.stderr.decode())
        return None




def download_youtube(url, name, output_path="downloads"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"[INFO] Created directory: {output_path}")

    print(f"[INFO] Starting YouTube download for: {url}")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",   # HD quality
        "merge_output_format": "mp4",           # final file format
        "outtmpl": os.path.join(output_path, f"{name}.%(ext)s"),
        "noplaylist": True,
        "quiet": False,
        "extractor_args": {"youtube": {"player_client": ["default"]}},  # avoid JS runtime warning
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("[SUCCESS] YouTube download completed.")
        return os.path.join(output_path, f"{name}.mp4")
    except Exception as e:
        print(f"[ERROR] YouTube download failed: {e}")
        return None



def process_url(url):
    if "youtube" in url:
        print("[INFO] Detected YouTube URL.")
        download_youtube_video(url)
    else:
        print("[INFO] Unsupported URL type.")


# ==============================
def get_duration(filename):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

def split_large_video(file_path, max_size_mb=1900):
    size_bytes = os.path.getsize(file_path)
    max_bytes = max_size_mb * 1024 * 1024

    if size_bytes <= max_bytes:
        return [file_path]  # No splitting needed

    duration = get_duration(file_path)
    parts = ceil(size_bytes / max_bytes)
    part_duration = duration / parts
    base_name = file_path.rsplit(".", 1)[0]
    output_files = []

    for i in range(parts):
        output_file = f"{base_name}_part{i+1}.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-i", file_path,
            "-ss", str(int(part_duration * i)),
            "-t", str(int(part_duration)),
            "-c", "copy",
            output_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(output_file):
            output_files.append(output_file)

    return output_files


def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


def get_mps_and_keys(api_url):
    response = requests.get(api_url)
    response_json = response.json()
    mpd = response_json.get('mpd_url')
    keys = response_json.get('keys')
    return mpd, keys


   
def exec(cmd):
        process = subprocess.run(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = process.stdout.decode()
        print(output)
        return output
        #err = process.stdout.decode()
def pull_run(work, cmds):
    with concurrent.futures.ThreadPoolExecutor(max_workers=work) as executor:
        print("Waiting for tasks to complete")
        fut = executor.map(exec,cmds)
async def aio(url,name):
    k = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(k, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return k


async def download(url,name):
    ka = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ka, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return ka

async def pdf_download(url, file_name, chunk_size=1024 * 10):
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
    return file_name   
   

def parse_vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = []
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ",2)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.append((i[0], i[2]))
            except:
                pass
    return new_info


def vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = dict()
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ",3)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    
                    # temp.update(f'{i[2]}')
                    # new_info.append((i[2], i[0]))
                    #  mp4,mkv etc ==== f"({i[1]})" 
                    
                    new_info.update({f'{i[2]}':f'{i[0]}'})

            except:
                pass
    return new_info


def create_session():
    import requests
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=3)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def repair_mp4(input_file):
    fixed = input_file.replace(".mp4", "_fixed.mp4")
    cmd = f'ffmpeg -y -i "{input_file}" -map 0 -c copy -movflags +faststart "{fixed}"'
    subprocess.run(cmd, shell=True)
    os.replace(fixed, input_file)

# ==============================
# FILE DECRYPT FUNCTION
# ==============================
def decrypt_file_fixed(file_path: str, key: str) -> bool:
    if not file_path or not os.path.exists(file_path):
        return False
    if not key:
        return True
    key_bytes = key.encode()
    file_size = os.path.getsize(file_path)
    decrypt_size = min(1024*2, file_size)  # 2KB header safe
    with open(file_path, "r+b") as f:
        with mmap.mmap(f.fileno(), decrypt_size, access=mmap.ACCESS_WRITE) as mm:
            for i in range(decrypt_size):
                mm[i] ^= key_bytes[i % len(key_bytes)]
    return True
# ==============================
# RAW FILE DOWNLOAD
# ==============================
# FAST DOWNLOAD
# ==============================
async def download_raw_file_fast(url: str, filename: str) -> str | None:
    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{filename}"
    max_chunks = 16
    headers = {"User-Agent":"Mozilla/5.0","Referer":"https://player.akamai.net.in/","Accept":"*/*","Connection":"keep-alive"}

    session = aiohttp.ClientSession()
    try:
        async with session.head(url, headers=headers) as resp:
            if resp.status != 200:
                await session.close()
                return None
            total_size = int(resp.headers.get("Content-Length", 0))
        chunk_size = math.ceil(total_size / max_chunks)
        tasks = []

        async def download_chunk(start, end, idx):
            for attempt in range(3):
                try:
                    range_header = {"Range": f"bytes={start}-{end}", **headers}
                    async with session.get(url, headers=range_header) as r:
                        if r.status in [200, 206]:
                            data = await r.read()
                            async with aiofiles.open(f"{file_path}.part{idx}", "wb") as f:
                                await f.write(data)
                            return True
                except:
                    await asyncio.sleep(1)
            return False

        for i in range(max_chunks):
            start = i * chunk_size
            end = min(start + chunk_size - 1, total_size - 1)
            tasks.append(download_chunk(start, end, i))

        results = await asyncio.gather(*tasks)
        if not all(results):
            await session.close()
            return None

        # Merge parts
        async with aiofiles.open(file_path, "wb") as out_f:
            for i in range(max_chunks):
                async with aiofiles.open(f"{file_path}.part{i}", "rb") as part_f:
                    await out_f.write(await part_f.read())
                os.remove(f"{file_path}.part{i}")
        await session.close()
        return file_path
    except Exception as e:
        await session.close()
        print(f"Fast download error: {e}")
        return None
# ==============================
# DOWNLOAD + DECRYPT WRAPPER
# ==============================
import os
import mmap
import requests
from tqdm import tqdm
from base64 import b64decode




import os
import asyncio
from pathlib import Path

async def decrypt_and_merge_video(mpd_url, keys_string, output_path, output_name, quality="720"):
    """
    Fast download + decrypt + merge exactly as original logic,
    but using aria2c for max speed and ensuring final video is playable.
    """

    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        # ------------------------------
        # 1) Download video + audio fast
        # ------------------------------
        cmd_download = (
            f'yt-dlp -f "bv[height<={quality}]+ba/b" '
            f'-o "{output_path}/file.%(ext)s" '
            f'--allow-unplayable-format --no-check-certificate '
            f'--external-downloader aria2c '
            f'--downloader-args "aria2c:-x 16 -j 32 -s 16 -k 1M" '
            f'"{mpd_url}"'
        )
        print(f"▶️ Downloading at 15x speed: {cmd_download}")
        os.system(cmd_download)

        # ------------------------------
        # 2) List downloaded files
        # ------------------------------
        av_files = list(output_path.iterdir())
        print(f"📄 Downloaded files: {av_files}")

        video_decrypted = False
        audio_decrypted = False

        # ------------------------------
        # 3) Decrypt video and audio
        # ------------------------------
        for f in av_files:
            if f.suffix.lower() in [".mp4", ".mkv"] and not video_decrypted:
                cmd_video = f'mp4decrypt {keys_string} --show-progress "{f}" "{output_path}/video.mp4"'
                print(f"🔓 Decrypting video: {cmd_video}")
                os.system(cmd_video)
                if (output_path / "video.mp4").exists():
                    video_decrypted = True
                f.unlink()
            elif f.suffix.lower() == ".m4a" and not audio_decrypted:
                cmd_audio = f'mp4decrypt {keys_string} --show-progress "{f}" "{output_path}/audio.m4a"'
                print(f"🔓 Decrypting audio: {cmd_audio}")
                os.system(cmd_audio)
                if (output_path / "audio.m4a").exists():
                    audio_decrypted = True
                f.unlink()

        if not video_decrypted or not audio_decrypted:
            raise FileNotFoundError("❌ Decryption failed: video or audio missing.")

        # ------------------------------
        # 4) Merge video + audio
        # ------------------------------
        merged_file = output_path / f"{output_name}.mp4"
        cmd_merge = f'ffmpeg -y -i "{output_path}/video.mp4" -i "{output_path}/audio.m4a" -c copy -movflags +faststart "{merged_file}"'
        print(f"🎬 Merging video + audio: {cmd_merge}")
        os.system(cmd_merge)

        # Cleanup decrypted temp files
        if (output_path / "video.mp4").exists():
            (output_path / "video.mp4").unlink()
        if (output_path / "audio.m4a").exists():
            (output_path / "audio.m4a").unlink()

        if not merged_file.exists():
            raise FileNotFoundError("❌ Merged video not created")

        # ------------------------------
        # 5) Duration info
        # ------------------------------
        cmd_duration = f'ffmpeg -i "{merged_file}" 2>&1 | grep "Duration"'
        duration_info = os.popen(cmd_duration).read()
        print(f"✅ Video ready: {merged_file} | {duration_info.strip()}")

        return str(merged_file)

    except Exception as e:
        print(f"❌ Error in decrypt_and_merge_video: {e}")
        return None


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if proc.returncode == 1:
        return False
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'

    

def old_download(url, file_name, chunk_size = 1024 * 10 * 10):
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
    return file_name


def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"


async def fast_download(url, name):
    """Fast direct download implementation without yt-dlp"""
    max_retries = 5
    retry_count = 0
    success = False
    
    while not success and retry_count < max_retries:
        try:
            if "m3u8" in url:
                # Handle m3u8 files
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        m3u8_text = await response.text()
                        
                    playlist = m3u8.loads(m3u8_text)
                    if playlist.is_endlist:
                        # Direct download of segments
                        base_url = url.rsplit('/', 1)[0] + '/'
                        
                        # Download all segments concurrently
                        segments = []
                        async with aiohttp.ClientSession() as session:
                            tasks = []
                            for segment in playlist.segments:
                                segment_url = urljoin(base_url, segment.uri)
                                task = asyncio.create_task(session.get(segment_url))
                                tasks.append(task)
                            
                            responses = await asyncio.gather(*tasks)
                            for response in responses:
                                segment_data = await response.read()
                                segments.append(segment_data)
                        
                        # Merge segments and save
                        output_file = f"{name}.mp4"
                        with open(output_file, 'wb') as f:
                            for segment in segments:
                                f.write(segment)
                        
                        success = True
                        return [output_file]
                    else:
                        # For live streams, fall back to ffmpeg
                        cmd = f'ffmpeg -hide_banner -loglevel error -stats -i "{url}" -c copy -bsf:a aac_adtstoasc -movflags +faststart "{name}.mp4"'
                        subprocess.run(cmd, shell=True)
                        if os.path.exists(f"{name}.mp4"):
                            success = True
                            return [f"{name}.mp4"]
            else:
                # For direct video URLs
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            output_file = f"{name}.mp4"
                            with open(output_file, 'wb') as f:
                                while True:
                                    chunk = await response.content.read(1024*1024)  # 1MB chunks
                                    if not chunk:
                                        break
                                    f.write(chunk)
                            success = True
                            return [output_file]
            
            if not success:
                print(f"\nAttempt {retry_count + 1} failed, retrying in 3 seconds...")
                retry_count += 1
                await asyncio.sleep(3)
                
        except Exception as e:
            print(f"\nError during attempt {retry_count + 1}: {str(e)}")
            retry_count += 1
            await asyncio.sleep(3)
    
    return None
    
def process_zip_to_video(url: str, name: str) -> str:
    import os, re, zipfile, tempfile, shutil, subprocess, requests
    from Crypto.Cipher import AES
    from urllib.parse import urljoin, urlparse

    REFERER = "https://player.akamai.net.in/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Referer": REFERER
    }

    tmp = tempfile.mkdtemp(prefix="zip_")
    zip_path = os.path.join(tmp, "video.zip")
    extract_dir = os.path.join(tmp, "extract")
    decrypt_dir = os.path.join(tmp, "decrypt")

    os.makedirs(extract_dir)
    os.makedirs(decrypt_dir)

    safe_name = re.sub(r'[^A-Za-z0-9_-]', '_', name)
    out_mp4 = os.path.join(tmp, safe_name + ".mp4")

    try:
        # ==========================================================
        # 1) FAST ZIP DOWNLOAD WITH PROGRESS
        # ==========================================================
        print("⬇️ Downloading ZIP...")
        r = requests.get(url, headers=HEADERS, stream=True, timeout=60)
        r.raise_for_status()

        total = int(r.headers.get("content-length", 0))
        done = 0

        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024 * 4):  # 4MB chunk
                if chunk:
                    f.write(chunk)
                    done += len(chunk)
                    if total:
                        percent = done * 100 // total
                        print(f"⬇️ {done/1024/1024:.2f} MB / {total/1024/1024:.2f} MB ({percent}%)")

        print("✅ ZIP downloaded successfully")

        # ==========================================================
        # 2) EXTRACT ZIP
        # ==========================================================
        print("📦 Extracting ZIP...")
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(extract_dir)
        print("✅ Extract complete")

        # ==========================================================
        # 3) FIND M3U8
        # ==========================================================
        print("🔍 Searching m3u8...")
        m3u8 = None
        for f in os.listdir(extract_dir):
            if f.endswith(".m3u8"):
                m3u8 = os.path.join(extract_dir, f)
                break
        if not m3u8:
            raise RuntimeError("❌ m3u8 not found")

        print(f"✅ m3u8 found: {os.path.basename(m3u8)}")
        lines = open(m3u8, encoding="utf-8", errors="ignore").read().splitlines()

        # ==========================================================
        # 4) PARSE KEY URI + IV
        # ==========================================================
        print("🔑 Parsing KEY & IV...")
        key_uri, iv = None, None

        for l in lines:
            if l.startswith("#EXT-X-KEY"):
                key_uri = re.search(r'URI="([^"]+)"', l).group(1)
                iv_hex = re.search(r'IV=0x([0-9A-Fa-f]+)', l)
                if iv_hex:
                    iv = bytes.fromhex(iv_hex.group(1))
                break

        if not key_uri:
            raise RuntimeError("❌ Key URI not found")

        print(f"✅ Key URI: {key_uri}")

        # ==========================================================
        # 5) RESOLVE KEY (LOCAL → RELATIVE → ABSOLUTE)
        # ==========================================================
        print("⬇️ Loading key...")
        key = None

        # (a) local key inside ZIP
        local_key = os.path.join(extract_dir, key_uri)
        if os.path.exists(local_key):
            key = open(local_key, "rb").read()
            print("🔑 Key found locally")

        # (b) relative to ZIP base
        if key is None:
            base = url.rsplit("/", 1)[0] + "/"
            try_url = urljoin(base, key_uri)
            print(f"🌐 Trying key URL: {try_url}")
            r = requests.get(try_url, headers=HEADERS, timeout=15)
            if r.ok:
                key = r.content

        # (c) absolute URI
        if key is None and key_uri.startswith("http"):
            r = requests.get(key_uri, headers=HEADERS, timeout=15)
            if r.ok:
                key = r.content

        if key is None:
            raise RuntimeError("❌ Key not found (all methods failed)")

        print("✅ Key loaded")

        # ==========================================================
        # 6) COLLECT TS SEGMENTS
        # ==========================================================
        segments = []
        for f in os.listdir(extract_dir):
            if f.lower().endswith((".ts", ".tsb", ".tse")):
                m = re.search(r'(\d+)', f)
                if m:
                    segments.append((int(m.group(1)), f))

        segments.sort(key=lambda x: x[0])
        print(f"📄 Total segments: {len(segments)}")

        # ==========================================================
        # 7) DECRYPT (🔥 CORRECT LOGIC – NO PADDING ERROR)
        # ==========================================================
        print("🔓 Decrypting segments...")
        total_seg = len(segments)

        for i, (_, f) in enumerate(segments):
            cipher = AES.new(key, AES.MODE_CBC, iv)  # 🔥 NEW cipher every segment
            enc = open(os.path.join(extract_dir, f), "rb").read()
            dec = cipher.decrypt(enc)

            # 🔥 remove PKCS7 padding ONLY for last segment
            if i == total_seg - 1:
                pad = dec[-1]
                if 1 <= pad <= 16:
                    dec = dec[:-pad]

            open(os.path.join(decrypt_dir, f"{i}.ts"), "wb").write(dec)

            if i % 20 == 0 or i == total_seg - 1:
                print(f"🔓 Decrypted {i+1}/{total_seg}")

        # ==========================================================
        # 8) CONCAT LIST
        # ==========================================================
        with open(os.path.join(decrypt_dir, "list.txt"), "w") as f:
            for i in range(total_seg):
                f.write(f"file '{i}.ts'\n")

        # ==========================================================
        # 9) MERGE USING FFMPEG
        # ==========================================================
        print("🎬 Creating final MP4...")
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", "list.txt",
            "-c", "copy",
            out_mp4
        ], cwd=decrypt_dir, check=True)

        shutil.move(out_mp4, os.getcwd())
        print("✅ Video created successfully")

        return safe_name + ".mp4"

    finally:
        shutil.rmtree(tmp, ignore_errors=True)
import asyncio
import subprocess
import logging
import os



import requests
import logging
import requests
import logging

import requests
import logging
import time

import yt_dlp
import requests
import logging
import subprocess
import asyncio
import os

import yt_dlp
import logging


import requests
import logging

import asyncio
import os

async def download_from_player(url: str, output: str) -> str | None:
    """
    Download video using ffmpeg with custom headers.
    """
    headers = (
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/143.0.0.0 Safari/537.36\r\n"
        f"Referer: {url}\r\n"
        "Origin: https://www.youtube.com\r\n"
        "Range: bytes=0-\r\n"
        "Accept: */*\r\n"
        "Accept-Encoding: identity;q=1, *;q=0\r\n"
        "Accept-Language: en-GB,en-US;q=0.9,en;q=0.8\r\n"
        "Sec-Fetch-Dest: video\r\n"
        "Sec-Fetch-Mode: no-cors\r\n"
        "Sec-Fetch-Site: same-origin\r\n"
        "DNT: 1\r\n"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-headers", headers,
        "-i", url,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        output
    ]

    print("⚡ Running ffmpeg command:", " ".join(cmd))

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )

    await process.wait()

    if process.returncode == 0 and os.path.exists(output):
        print("✅ Download complete:", output)
        return output
    else:
        print("❌ ffmpeg failed with code:", process.returncode)
        return None
import asyncio
import aiohttp
import subprocess
import os
import logging
from urllib.parse import urljoin

async def download_video(url, cmd, name):
    """
    Async download handler with retries and special cases.
    ✅ 15x fast download
    ✅ Works for m3u8, zip, GoogleVideo/YouTube, direct URLs
    """
    # Special cases first
    if "transcoded" in url and ".m3u8" in url:
        print("⚡ Handling transcoded m3u8 stream")
        return await download_appx_m3u8(url, name)  # your existing function

    if "appx" in url and ".zip" in url:
        print("⚡ Handling appx zip archive")
        return process_zip_to_video(url, name)

    if "googlevideo.com" in url or "youtube.com" in url or "youtu.be" in url or "embed" in url:
        print("⚡ Handling YouTube/GoogleVideo link")
        return await download_from_player(url, name)  # your existing ffmpeg based function

    # Normal direct URL download (aiohttp 15x)
    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=360, headers={"User-Agent":"Mozilla/5.0"}, ssl=False) as resp:
                    if resp.status != 200:
                        raise Exception(f"HTTP {resp.status}")
                    total = int(resp.headers.get("Content-Length", 0))
                    chunk_size = 1024 * 1024 * 10  # 10MB per chunk
                    downloaded = 0
                    temp_file = f"{name}.tmp"
                    with open(temp_file, "wb") as f:
                        async for chunk in resp.content.iter_chunked(chunk_size):
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total:
                                print(f"⬇️ {downloaded/1024/1024:.2f}/{total/1024/1024:.2f} MB ({downloaded*100/total:.1f}%)")
                    os.rename(temp_file, name)
                    print(f"✅ Download complete: {name}")
                    break  # success
        except Exception as e:
            retry_count += 1
            print(f"⚠️ Download attempt {retry_count}/{max_retries} failed: {e}, retrying in 3s...")
            await asyncio.sleep(3)
    else:
        print("❌ All retries failed")
        return None

    # Final check for file
    base = name.rsplit(".", 1)[0]
    if os.path.isfile(name):
        return name
    elif os.path.isfile(f"{base}.mkv"):
        return f"{base}.mkv"
    elif os.path.isfile(f"{base}.mp4"):
        return f"{base}.mp4"
    elif os.path.isfile(f"{base}.webm"):
        return f"{base}.webm"
    
    return name


def download_and_decrypt_video(url: str, name: str, key: str = None) -> str | None:
    """
    Download and decrypt video (mp4/mkv/both) safely.
    No if checks on extension, everything is decrypted and repaired automatically.
    """
    file_path = None

    # 1️⃣ APPX m3u8
    if ".m3u8" in url and "appx" in url:
        file_path = asyncio.run(download_appx_m3u8(url, name))

    # 2️⃣ APPX ZIP
    elif "appx" in url and ".zip" in url:
        from zip_handler import process_zip_to_video  # your existing zip->mp4 logic
        file_path = process_zip_to_video(url, name)

    # 3️⃣ Direct download (mp4/mkv/other)
    else:
        file_path = asyncio.run(download_raw_file_fast(url, f"{name}.mp4"))

    if not file_path or not os.path.exists(file_path):
        print("❌ Download failed")
        return None

    # 🔑 Decrypt file (any extension)
    decrypt_file_fixed(file_path, key)

    # ✅ Repair using ffmpeg (works for mp4/mkv)
    repair_mp4(file_path)

    return file_path


async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog, channel_id, watermark="{CREDIT}", topic_thread_id: int = None):
    try:
        temp_thumb = None  # ✅ Ensure this is always defined for later cleanup

        thumbnail = thumb
        if thumb in ["/d", "no"] or not os.path.exists(thumb):
            temp_thumb = f"downloads/thumb_{os.path.basename(filename)}.jpg"
            
            # Generate thumbnail at 10s
            subprocess.run(
                f'ffmpeg -i "{filename}" -ss 00:00:10 -vframes 1 -q:v 2 -y "{temp_thumb}"',
                shell=True
            )

            # ✅ Only apply watermark if watermark != "/d"
            if os.path.exists(temp_thumb) and (watermark and watermark.strip() != "/d"):
                text_to_draw = watermark.strip()
                try:
                    # Probe image width for better scaling
                    probe_out = subprocess.check_output(
                        f'ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0:s=x "{temp_thumb}"',
                        shell=True,
                        stderr=subprocess.DEVNULL,
                    ).decode().strip()
                    img_width = int(probe_out.split('x')[0]) if 'x' in probe_out else int(probe_out)
                except Exception:
                    img_width = 1280

                # Base size relative to width, then adjust by text length
                base_size = max(28, int(img_width * 0.075))
                text_len = len(text_to_draw)
                if text_len <= 3:
                    font_size = int(base_size * 1.25)
                elif text_len <= 8:
                    font_size = int(base_size * 1.0)
                elif text_len <= 15:
                    font_size = int(base_size * 0.85)
                else:
                    font_size = int(base_size * 0.7)
                font_size = max(32, min(font_size, 120))

                box_h = max(60, int(font_size * 1.6))

                # Simple escaping for single quotes in text
                safe_text = text_to_draw.replace("'", "\\'")

                text_cmd = (
                    f'ffmpeg -i "{temp_thumb}" -vf '
                    f'"drawbox=y=0:color=black@0.35:width=iw:height={box_h}:t=fill,'
                    f'drawtext=fontfile=font.ttf:text=\'{safe_text}\':fontcolor=white:'
                    f'fontsize={font_size}:x=(w-text_w)/2:y=(({box_h})-text_h)/2" '
                    f'-c:v mjpeg -q:v 2 -y "{temp_thumb}"'
                )
                subprocess.run(text_cmd, shell=True)
            
            thumbnail = temp_thumb if os.path.exists(temp_thumb) else None

        await prog.delete(True)  # ⏳ Remove previous progress message

        reply1 = await bot.send_message(channel_id, f" **Uploading Video:**\n<blockquote>{name}</blockquote>")
        reply = await m.reply_text(f"🖼 **Generating Thumbnail:**\n<blockquote>{name}</blockquote>")

        file_size_mb = os.path.getsize(filename) / (1024 * 1024)
        notify_split = None
        sent_message = None

        if file_size_mb < 2000:
            # 📹 Upload as single video
            dur = int(duration(filename))
            start_time = time.time()

            try:
                sent_message = await bot.send_video(
                    chat_id=channel_id,
                    video=filename,
                    caption=cc,
                    supports_streaming=True,
                    height=720,
                    width=1280,
                    thumb=thumbnail,
                    duration=dur,
                    progress=progress_bar,
                    progress_args=(reply, start_time)
                )
            except Exception:
                sent_message = await bot.send_document(
                    chat_id=channel_id,
                    document=filename,
                    caption=cc,
                    progress=progress_bar,
                    progress_args=(reply, start_time)
                )

            # ✅ Cleanup
            if os.path.exists(filename):
                os.remove(filename)
            await reply.delete(True)
            await reply1.delete(True)

        else:
            # ⚠️ Notify about splitting
            notify_split = await m.reply_text(
                f"⚠️ The video is larger than 2GB ({human_readable_size(os.path.getsize(filename))})\n"
                f"⏳ Splitting into parts before upload..."
            )

            parts = split_large_video(filename)

            try:
                first_part_message = None
                for idx, part in enumerate(parts):
                    part_dur = int(duration(part))
                    part_num = idx + 1
                    total_parts = len(parts)
                    part_caption = f"{cc}\n\n📦 Part {part_num} of {total_parts}"
                    part_filename = f"{name}_Part{part_num}.mp4"

                    upload_msg = await m.reply_text(f"📤 Uploading Part {part_num}/{total_parts}...")

                    try:
                        msg_obj = await bot.send_video(
                            chat_id=channel_id,
                            video=part,
                            caption=part_caption,
                            file_name=part_filename,
                            supports_streaming=True,
                            height=720,
                            width=1280,
                            thumb=thumbnail,
                            duration=part_dur,
                            progress=progress_bar,
                            progress_args=(upload_msg, time.time())
                        )
                        if first_part_message is None:
                            first_part_message = msg_obj
                    except Exception:
                        msg_obj = await bot.send_document(
                            chat_id=channel_id,
                            document=part,
                            caption=part_caption,
                            file_name=part_filename,
                            progress=progress_bar,
                            progress_args=(upload_msg, time.time())
                        )
                        if first_part_message is None:
                            first_part_message = msg_obj

                    await upload_msg.delete(True)
                    if os.path.exists(part):
                        os.remove(part)

            except Exception as e:
                raise Exception(f"Upload failed at part {idx + 1}: {str(e)}")

            # ✅ Final messages
            if len(parts) > 1:
                await m.reply_text("✅ Large video successfully uploaded in multiple parts!")

            # Cleanup after split
            await reply.delete(True)
            await reply1.delete(True)
            if notify_split:
                await notify_split.delete(True)
            if os.path.exists(filename):
                os.remove(filename)

            # Return first sent part message
            sent_message = first_part_message

        # 🧹 Cleanup generated thumbnail if applicable
        if thumb in ["/d", "no"] and temp_thumb and os.path.exists(temp_thumb):
            os.remove(temp_thumb)

        return sent_message

    except Exception as err:
        raise Exception(f"send_vid failed: {err}")
