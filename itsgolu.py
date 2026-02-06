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
    """
    Fast m3u8 video download using ffmpeg (sync version).
    Optimized for Heroku: reduced threads and added retries/error handling.
    """
    os.makedirs("downloads", exist_ok=True)
    output = f"downloads/{name}.mp4"

    headers = (
        "User-Agent: Mozilla/5.0 (Linux; Android 13)\r\n"
        "Referer: https://player.akamai.net.in/\r\n"
        "Origin: https://akstechnicalclasses.classx.co.in\r\n"
    )

    # Retry logic
    retry_count = 0
    max_retries = 3
    download_success = False
    while retry_count < max_retries:
        cmd = [
            "ffmpeg",
            "-y",
            "-threads", "1",  # Reduced from 2 for Heroku resource constraints
            "-bufsize", "4M",  # Reduced buffer for stability
            "-stats_period", "5",
            "-loglevel", "error",
            "-headers", headers,
            "-multiple_requests", "1",  # Keep for parallel segments if supported
            "-i", url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            output
        ]

        print(f"▶️ Downloading m3u8 (attempt {retry_count + 1}): {' '.join(cmd)}")
        logging.info(' '.join(cmd))
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print("✅ Download succeeded")
            download_success = True
            break
        except subprocess.CalledProcessError as exc:
            retry_count += 1
            print(f"⚠️ Download retry {retry_count}/{max_retries} failed: {exc}")
            if retry_count == max_retries:
                print("❌ All download retries failed.")
                return None

    if not download_success:
        return None

    # Verify file exists and has content
    if os.path.exists(output) and os.path.getsize(output) > 0:
        print(f"✅ Fast download complete: {output}")
        return output
    else:
        print(f"❌ Download failed or file is empty: {output}")
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
import os
import math
import asyncio
import aiohttp
import aiofiles
from tqdm import tqdm
import os
import subprocess
import logging

def download_raw_file(url: str, filename: str) -> str | None:
    """
    Ultra-fast, resume-safe raw file download for Heroku.
    Uses yt-dlp + aria2c for max speed, with retries and error handling.
    Optimized for Heroku: reduced concurrency to avoid resource exhaustion.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        "Referer": "https://akstechnicalclasses.classx.co.in/",
        "Origin": "https://akstechnicalclasses.classx.co.in",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{filename}.mkv"

    # Build header args for yt-dlp
    header_args = " ".join([f'--add-header "{k}: {v}"' for k, v in headers.items()])

    # yt-dlp + aria2c for ultra fast, with retries
    retry_count = 0
    max_retries = 3  # Increased retries for reliability
    download_success = False
    while retry_count < max_retries:
        cmd = (
            f'yt-dlp -f best -o "{file_path}" --no-check-certificate '
            f'{header_args} '
            f'--external-downloader aria2c '
            f'--downloader-args "aria2c:-x8 -j8 -s8 -k1M" '  # Balanced concurrency: higher than Heroku min but not max to keep fast yet stable
            f'--retries 5 --fragment-retries 5 '  # Added retries for robustness
            f'"{url}"'
        )
        print(f"▶️ Downloading (attempt {retry_count + 1}): {cmd}")
        logging.info(cmd)
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print("✅ Download succeeded")
            download_success = True
            break
        except subprocess.CalledProcessError as exc:
            retry_count += 1
            print(f"⚠️ Download retry {retry_count}/{max_retries} failed: {exc}")
            if retry_count == max_retries:
                print("❌ All download retries failed.")
                return None

    if not download_success:
        return None

    # Verify file exists and has content
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        print(f"✅ Download complete: {file_path}")
        return file_path
    else:
        print(f"❌ Download failed or file is empty: {file_path}")
        return None
import os
import mmap
import requests
from tqdm import tqdm
from base64 import b64decode
import asyncio
import os
from pathlib import Path
import os
import subprocess
import logging
from pathlib import Path
import os
import subprocess
import logging
from pathlib import Path

import subprocess
import time
from pathlib import Path

def decrypt_and_merge_video(
    mpd_url: str,
    keys_string: str,
    output_dir: str,
    output_name: str,
    quality: str = "720",
    max_retries: int = 3
) -> str | None:

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, max_retries + 1):
        print(f"\n🔁 Attempt {attempt}/{max_retries}")

        try:
            # =========================
            # cmd10 → DOWNLOAD
            # =========================
            cmd10 = (
                f'yt-dlp -f "bv[height<={quality}]+ba/b" '
                f'-o "{out}/input.%(ext)s" '
                f'--allow-unplayable-format --no-check-certificate '
                f'--external-downloader aria2c '
                f'--downloader-args "aria2c:-x4 -j4 -s4 -k1M" '
                f'"{mpd_url}"'
            )
            print("▶️ cmd10:", cmd10)
            if subprocess.call(cmd10, shell=True) != 0:
                raise RuntimeError("Download failed")

            # =========================
            # Detect files
            # =========================
            video_enc = next((f for f in out.iterdir() if f.suffix == ".mp4"), None)
            audio_enc = next((f for f in out.iterdir() if f.suffix == ".m4a"), None)

            if not video_enc or not audio_enc:
                raise FileNotFoundError("Video/Audio not found")

            video_dec = out / "video_dec.mp4"
            audio_dec = out / "audio_dec.m4a"

            # =========================
            # cmd11 → VIDEO DECRYPT
            # =========================
            cmd11 = f'mp4decrypt {keys_string} "{video_enc}" "{video_dec}"'
            print("🔓 cmd11:", cmd11)
            if subprocess.call(cmd11, shell=True) != 0:
                raise RuntimeError("Video decrypt failed")

            # =========================
            # cmd12 → AUDIO DECRYPT
            # =========================
            cmd12 = f'mp4decrypt {keys_string} "{audio_enc}" "{audio_dec}"'
            print("🔓 cmd12:", cmd12)
            if subprocess.call(cmd12, shell=True) != 0:
                raise RuntimeError("Audio decrypt failed")

            video_enc.unlink(missing_ok=True)
            audio_enc.unlink(missing_ok=True)

            # =========================
            # cmd13 → MERGE (FAST)
            # =========================
            final_file = out / f"{output_name}.mp4"
            cmd13 = (
                f'ffmpeg -y -loglevel error '
                f'-i "{video_dec}" -i "{audio_dec}" '
                f'-c copy -movflags +faststart "{final_file}"'
            )
            print("🎬 cmd13:", cmd13)
            if subprocess.call(cmd13, shell=True) != 0:
                raise RuntimeError("Merge failed")

            video_dec.unlink(missing_ok=True)
            audio_dec.unlink(missing_ok=True)

            if final_file.exists() and final_file.stat().st_size > 1024 * 100:
                print("✅ Video ready successfully!")
                return str(final_file)

            raise RuntimeError("Final file invalid")

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed:", e)

            # CLEANUP BEFORE RETRY
            for f in out.iterdir():
                if f.is_file() and f.name != f"{output_name}.mp4":
                    f.unlink(missing_ok=True)

            time.sleep(2)

    print("❌ All retries failed")
    return None



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


def download_video(url, base_cmd, name):
    """
    Handles all types of URLs: m3u8, YouTube, direct links
    Fast download using yt-dlp + aria2c
    Compatible with Heroku / Koyeb
    """

    # 🔹 Special m3u8 case
    if "transcoded" in url and url.endswith(".m3u8"):
        print("⚡ Handling m3u8")
        return download_appx_m3u8(url, name)

    max_retries = 2
    retry_count = 0

    # Ensure output template
    if not name.endswith(".%(ext)s"):
        output_tpl = f"{name}.%(ext)s"
    else:
        output_tpl = name

    while retry_count < max_retries:
        download_cmd = (
            f'{base_cmd} '
            f'-R 25 --fragment-retries 25 '
            f'--external-downloader aria2c '
            f'--downloader-args "aria2c:-x4 -j4 -s4 -k1M" '
            f'-o "{output_tpl}" "{url}"'
        )

        print(f"▶️ Running command:\n{download_cmd}")

        try:
            proc = subprocess.Popen(
                download_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in proc.stdout:
                print(line, end="")

            proc.wait()

            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, download_cmd)

            print("✅ Download succeeded")
            break

        except subprocess.CalledProcessError as exc:
            retry_count += 1
            print(f"⚠️ Retry {retry_count}/{max_retries} failed")

            if retry_count >= max_retries:
                print("❌ All retries failed")
                return None

    # 🔍 Find actual output file
    base = os.path.splitext(name)[0]
    possible_exts = [".mp4", ".mkv", ".webm", ".mp4.webm"]

    for ext in possible_exts:
        file_path = base + ext
        if os.path.isfile(file_path):
            return file_path

    print("❌ Download finished but no output file found")
    return None


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

def download_and_decrypt_video(url: str, name: str, key: str = None) -> str | None:
    # Download and decrypt the video
    if "transcoded" in url and ".m3u8" in url:
        print("⚡ Handling m3u8")
        return download_appx_m3u8(url, name)
    video_path = None
    for _ in range(5):  # Retry up to 5 times
        video_path = download_raw_file(url, name)
        if video_path and os.path.getsize(video_path) > 10 * 1024 * 1024:  # Ensure minimum size
            break

    if not video_path:
        return None

    try:
        if key:
            # Decrypt the file if key is provided
            decrypt_file(video_path, key)
    except Exception as e:
        print(f"⚠️ Decrypt failed: {e}")
        return None

    if not is_playable(video_path):
        # If not playable, repair the video
        return repair_video(video_path)
    else:
        # If already playable, return the original path
        return video_path




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
def _fmt_time(sec):
    sec = int(sec)
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    return f"{s}s"

# 🔥 Global cache to throttle edits for fast upload
_LAST_EDIT_TIME = {}

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
