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
import logging

def download_appx_m3u8(url: str, name: str) -> str | None:
    os.makedirs("downloads", exist_ok=True)
    safe_name = safe_filename(name)
    output = f"downloads/{safe_name}.mp4"

    headers = (
        "User-Agent: Mozilla/5.0 (Linux; Android 13)\r\n"
        "Referer: https://player.akamai.net.in/\r\n"
        "Origin: https://akstechnicalclasses.classx.co.in\r\n"
    )

    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        cmd = [
            "ffmpeg",
            "-y",
            "-threads", "1",
            "-bufsize", "4M",
            "-stats_period", "5",
            "-loglevel", "error",
            "-headers", headers,
            "-multiple_requests", "1",
            "-i", url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            output
        ]

        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            if os.path.exists(output) and os.path.getsize(output) > 0:
                return output
        except subprocess.CalledProcessError as exc:
            print(f"⚠️ m3u8 retry {retry_count + 1}: {exc}")

        retry_count += 1

    return None


# ==============================
def get_duration(filename):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

def split_large_video(file_path, max_size_mb=1800):
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

import aiohttp
import aiofiles
import requests
import os

async def download_pdf(url: str, name: str) -> str | None:
    os.makedirs("downloads", exist_ok=True)
    safe_name = safe_filename(name)
    file_path = os.path.join("downloads", f"{safe_name}.pdf")

    try:
        timeout = aiohttp.ClientTimeout(total=120)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, allow_redirects=True) as resp:
                if resp.status != 200:
                    print(f"❌ PDF download failed: HTTP {resp.status}")
                    return None

                content_type = resp.headers.get("content-type", "").lower()
                if "pdf" not in content_type and "octet-stream" not in content_type:
                    print(f"⚠️ Unexpected content-type: {content_type}")

                data = await resp.read()
                if not data:
                    print("❌ Empty PDF response")
                    return None

                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(data)

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return file_path

        return None

    except Exception as e:
        print(f"❌ PDF download exception: {e}")
        return None


def pdf_download_sync(url: str, name: str, chunk_size=1024 * 256) -> str | None:
    os.makedirs("downloads", exist_ok=True)
    safe_name = safe_filename(name)
    file_path = os.path.join("downloads", f"{safe_name}.pdf")

    try:
        r = requests.get(url, allow_redirects=True, stream=True, timeout=60)
        if r.status_code != 200:
            print(f"❌ PDF sync download failed: HTTP {r.status_code}")
            return None

        with open(file_path, "wb") as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    fd.write(chunk)

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return file_path

        return None

    except Exception as e:
        print(f"❌ PDF sync exception: {e}")
        return None
   

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
import os
import math
import asyncio
import aiohttp
import aiofiles
from tqdm import tqdm
import os
import subprocess
import logging

import logging
from pathlib import Path
import os
import subprocess
import logging
from pathlib import Path

import subprocess
def download_raw_file(url: str, filename: str) -> str | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        "Referer": "https://akstechnicalclasses.classx.co.in/",
        "Origin": "https://akstechnicalclasses.classx.co.in",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    os.makedirs("downloads", exist_ok=True)
    safe_name = safe_filename(filename)
    output_template = f"downloads/{safe_name}.%(ext)s"

    header_args = " ".join([f'--add-header "{k}: {v}"' for k, v in headers.items()])

    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        cmd = (
            f'yt-dlp -f best --no-check-certificate '
            f'{header_args} '
            f'--external-downloader aria2c '
            f'--downloader-args "aria2c:-x8 -j8 -s8 -k1M" '
            f'--retries 5 --fragment-retries 5 '
            f'-o "{output_template}" '
            f'"{url}"'
        )

        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

            # find real downloaded file
            for ext in ["mp4", "mkv", "webm", "ts"]:
                fp = f"downloads/{safe_name}.{ext}"
                if os.path.exists(fp) and os.path.getsize(fp) > 0:
                    return fp

        except subprocess.CalledProcessError as exc:
            print(f"⚠️ raw download retry {retry_count + 1}: {exc}")

        retry_count += 1

    return None
import time
from pathlib import Path

def decrypt_and_merge_video(mpd_url, keys_string, output_path, output_name, quality="720"):
    try:
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        cmd1 = f'yt-dlp -f "bv[height<={quality}]+ba/b" -o "{output_path}/file.%(ext)s" --allow-unplayable-format --no-check-certificate --external-downloader aria2c "{mpd_url}"'
        print(f"Running command: {cmd1}")
        os.system(cmd1)
        
        avDir = list(output_path.iterdir())
        print(f"Downloaded files: {avDir}")
        print("Decrypting")

        video_decrypted = False
        audio_decrypted = False

        for data in avDir:
            if data.suffix == ".mp4" and not video_decrypted:
                cmd2 = f'mp4decrypt {keys_string} --show-progress "{data}" "{output_path}/video.mp4"'
                print(f"Running command: {cmd2}")
                os.system(cmd2)
                if (output_path / "video.mp4").exists():
                    video_decrypted = True
                data.unlink()
            elif data.suffix == ".m4a" and not audio_decrypted:
                cmd3 = f'mp4decrypt {keys_string} --show-progress "{data}" "{output_path}/audio.m4a"'
                print(f"Running command: {cmd3}")
                os.system(cmd3)
                if (output_path / "audio.m4a").exists():
                    audio_decrypted = True
                data.unlink()

        if not video_decrypted or not audio_decrypted:
            raise FileNotFoundError("Decryption failed: video or audio file not found.")

        cmd4 = f'ffmpeg -i "{output_path}/video.mp4" -i "{output_path}/audio.m4a" -c copy "{output_path}/{output_name}.mp4"'
        print(f"Running command: {cmd4}")
        os.system(cmd4)
        if (output_path / "video.mp4").exists():
            (output_path / "video.mp4").unlink()
        if (output_path / "audio.m4a").exists():
            (output_path / "audio.m4a").unlink()
        
        filename = output_path / f"{output_name}.mp4"

        if not filename.exists():
            raise FileNotFoundError("Merged video file not found.")

        cmd5 = f'ffmpeg -i "{filename}" 2>&1 | grep "Duration"'
        duration_info = os.popen(cmd5).read()
        print(f"Duration info: {duration_info}")

        return str(filename)

    except Exception as e:
        print(f"Error during decryption and merging: {str(e)}")
        raise


async def run_cmd(cmd):
    """Run command asynchronously and capture output"""
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise Exception(f"Command failed: {cmd}\n[stderr] {stderr.decode()}")
    return stdout.decode()


    

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
                                    chunk = await response.content.read(2 * 1024 * 1024)  # 1MB chunks
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
import asyncio
import os
import subprocess
import logging
import os
import subprocess
import logging

import os
import subprocess
import logging

import subprocess
import os
from tqdm import tqdm
import subprocess
import os

base_cmd = (
    'yt-dlp '
    '-f "b[height<=1080]/bv[height<=1080]+ba/b/bv+ba" '
    '--merge-output-format mp4 '
)


import os
import asyncio
import subprocess
import logging

import os
import subprocess
import logging

import os
import subprocess

import os
import subprocess

import os
import asyncio
import logging
import subprocess

# -----------------------------
# Helper function: sanitize & check file
# -----------------------------
import os
import asyncio
import subprocess
import logging

# -----------------------------
# Helper: sanitize/check file
# -----------------------------
def get_existing_file(name):
    try:
        if os.path.isfile(name):
            return name

        base, ext = os.path.splitext(name)
        candidates = [
            f"{name}.webm",
            f"{base}.mp4",
            f"{base}.mkv",
            f"{base}.webm",
            f"{base}.mp4.webm",
        ]
        for file in candidates:
            if os.path.isfile(file):
                return file
        return f"{base}.mp4"
    except Exception as exc:
        logging.error(f"Error checking file: {exc}")
        return name

# -----------------------------
# Async download function
# -----------------------------
async def download_video(url: str, output_name: str, quality: str = "480p"):
    """
    Download video using yt-dlp async.
    url         : video URL
    output_name : desired file name
    quality     : '144p', '240p', '360p', '480p', '720p', '1080p'
    """
    # sanitize filename
    safe_name = "".join(c for c in output_name if c.isalnum() or c in " ._-")
    if len(safe_name) > 60:
        safe_name = safe_name[:60]  # truncate
    safe_name += f"_{quality}"

    final_file = get_existing_file(f"{safe_name}.mp4")

    # yt-dlp format string for height <= requested
    height = quality.replace("p","")
    yt_format = f"b[height<={height}]/bv[height<={height}]+ba/b/bv+ba"

    cmd = f'yt-dlp -f "{yt_format}" --merge-output-format mp4 --external-downloader aria2c --external-downloader-args "-x8 -s8 -j8 -k1M" -o "{final_file}" "{url}"'

    retry_count = 0
    max_retries = 2

    while retry_count <= max_retries:
        print(f"▶️ Running: {cmd}")
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            print("✅ Download succeeded")
            break

        retry_count += 1
        print(f"⚠️ Download failed (attempt {retry_count}/{max_retries}) retrying in 5s...")
        await asyncio.sleep(5)

    # check final file
    final_file = get_existing_file(final_file)

    # FFmpeg faststart fix
    fixed_file = f"{os.path.splitext(final_file)[0]}_fixed.mp4"
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", final_file, "-c", "copy", "-movflags", "faststart", fixed_file],
            check=True
        )
        return fixed_file
    except Exception as e:
        logging.error(f"FFmpeg fix failed: {e}")
        return final_file


import os
import subprocess
import mmap

def decrypt_file(file_path: str, key: str) -> bool:
    if not file_path or not os.path.exists(file_path):
        return False

    # Safety check for empty file
    if os.path.getsize(file_path) == 0:
        print("❌ File is empty, skipping decrypt")
        return False

    if not key:
        return True

    key_bytes = key.encode()
    size = min(28, os.path.getsize(file_path))

    with open(file_path, "r+b") as f:
        with mmap.mmap(f.fileno(), length=size, access=mmap.ACCESS_WRITE) as mm:
            for i in range(size):
                mm[i] ^= key_bytes[i] if i < len(key_bytes) else i

    return True

def is_playable(file_path: str) -> bool:
    try:
        # Probe the file to check if it's playable
        subprocess.run(
            f'ffprobe -v error -i "{file_path}"',
            shell=True, check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def repair_video(file_path: str) -> str:
    # Repair the video to make it playable
    repaired_path = file_path.replace(".mkv", "_fixed.mp4")
    cmd = f'ffmpeg -y -i "{file_path}" -c copy "{repaired_path}"'
    subprocess.run(cmd, shell=True)
    return repaired_path





import os
import time
import subprocess
from pyrogram import Client
from pyrogram.types import Message
credit1 = os.environ.get(
    "credit1",
    '<a href="https://t.me/Jetha_lal_bot">𝄟⃝🐬🅹🅰🅸 🆂🅷🆁🅸 🆁🅰🅼 ⚡️ 𝄟⃝🐬 💻</a>'
)
# ====== Time formatting for ETA ======
def download_and_decrypt_video(url: str, name: str, key: str = None) -> str | None:
    safe_name = safe_filename(name)

    if "transcoded" in url and ".m3u8" in url:
        print("⚡ Handling m3u8")
        video_path = download_appx_m3u8(url, safe_name)
    else:
        video_path = download_raw_file(url, safe_name)

    if not video_path or not os.path.exists(video_path):
        print("❌ Video file download failed")
        return None

    if os.path.getsize(video_path) == 0:
        print("❌ Downloaded video is empty")
        return None

    try:
        if key:
            ok = decrypt_file(video_path, key)
            if not ok:
                print("❌ Decrypt failed")
                return None
    except Exception as e:
        print(f"⚠️ Decrypt exception: {e}")
        return None

    if not is_playable(video_path):
        repaired = repair_video(video_path)
        if repaired and os.path.exists(repaired) and os.path.getsize(repaired) > 0:
            return repaired
        return None

    return video_pathtime(sec):
    
# ====== Time formatting for ETA ======
def _fmt_time(sec):
    sec = int(sec)
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    return f"{s}s

# ====== Progress bar for uploads ======
def progress_bar(current, total, reply, start_time, name="{VIDEO}", credit="{CREDIT}"):
    if current <= 0 or total <= 0:
        return

    now = time.time()
    key = id(reply)
    last_edit = _LAST_EDIT_TIME.get(key, 0)
    if now - last_edit < 1.2:  # throttle every ~1.2 sec
        return
    _LAST_EDIT_TIME[key] = now

    diff = now - start_time
    if diff < 1:
        return

    speed = current / diff                    # bytes/sec
    percent = (current * 100) / total
    eta = (total - current) / speed if speed > 0 else 0

    done_mb = current / (1024 * 1024)
    total_mb = total / (1024 * 1024)
    speed_mb = speed / (1024 * 1024)

    # Progress bar design
    bar_len = 20
    filled = int(bar_len * percent / 100)
    bar = "█" * filled + "░" * (bar_len - filled)

    text = (
        "╭━━━━━━━━━━━━━━━━━━━━━━╮\n"
        "│ 🚀 **UPLOADING VIDEO** │\n"
        "├━━━━━━━━━━━━━━━━━━━━━━┤\n"
        f"│ 🎬 **{name[:40]}**\n"
        f"│ `{bar}` **{percent:5.1f}%**\n"
        f"│ ⬆️ **{done_mb:,.0f} / {total_mb:,.0f} MB**\n"
        f"│ ⚡ **{speed_mb:,.2f} MB/s**\n"
        f"│ ⏳ **{_fmt_time(eta)} left**\n"
        "├━━━━━━━━━━━━━━━━━━━━━━┤\n"
        f"│ 👤 **CREDIT:** `{credit1}`\n"
        "╰━━━━━━━━━━━━━━━━━━━━━━╯"
    )

    try:
        reply.edit_text(text)
    except:
        pass

# ====== Main send_vid function ======
async def  send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog, channel_id, watermark="{CREDIT}", topic_thread_id: int = None):
    try:
        temp_thumb = None  # Ensure always defined
        thumbnail = thumb

        # Thumbnail generation
        if thumb in ["/d", "no"] or not os.path.exists(thumb):
            temp_thumb = f"downloads/thumb_{os.path.basename(filename)}.jpg"
            subprocess.run(
                f'ffmpeg -i "{filename}" -ss 00:00:10 -vframes 1 -q:v 2 -y "{temp_thumb}"',
                shell=True
            )

            # Watermark if needed
            if os.path.exists(temp_thumb) and (watermark and watermark.strip() != "/d"):
                text_to_draw = watermark.strip()
                try:
                    probe_out = subprocess.check_output(
                        f'ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0:s=x "{temp_thumb}"',
                        shell=True,
                        stderr=subprocess.DEVNULL,
                    ).decode().strip()
                    img_width = int(probe_out.split('x')[0]) if 'x' in probe_out else int(probe_out)
                except Exception:
                    img_width = 1280

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

        await prog.delete(True)
        reply1 = await bot.send_message(channel_id, f" **Uploading Video:**\n<blockquote>{name}</blockquote>")
        reply = await m.reply_text(f"🖼 **Generating Thumbnail:**\n<blockquote>{name}</blockquote>")

        file_size_mb = os.path.getsize(filename) / (1024 * 1024)
        notify_split = None
        sent_message = None

        if file_size_mb < 2000:
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
                    progress_args=(reply, start_time, name, watermark)
                )
            except Exception:
                sent_message = await bot.send_document(
                    chat_id=channel_id,
                    document=filename,
                    caption=cc,
                    progress=progress_bar,
                    progress_args=(reply, start_time, name, watermark)
                )

            if os.path.exists(filename):
                os.remove(filename)
            await reply.delete(True)
            await reply1.delete(True)

        else:
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
                            progress_args=(upload_msg, time.time(), name, watermark)
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
                            progress_args=(upload_msg, time.time(), name, watermark)
                        )
                        if first_part_message is None:
                            first_part_message = msg_obj

                    await upload_msg.delete(True)
                    if os.path.exists(part):
                        os.remove(part)
            except Exception as e:
                raise Exception(f"Upload failed at part {idx + 1}: {str(e)}")

            if len(parts) > 1:
                await m.reply_text("✅ Large video successfully uploaded in multiple parts!")

            await reply.delete(True)
            await reply1.delete(True)
            if notify_split:
                await notify_split.delete(True)
            if os.path.exists(filename):
                os.remove(filename)

            sent_message = first_part_message

        if thumb in ["/d", "no"] and temp_thumb and os.path.exists(temp_thumb):
            os.remove(temp_thumb)

        return sent_message

    except Exception as err:
        raise Exception(f"send_vid failed: {err}")
