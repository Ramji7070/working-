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

def download_appx_m3u8(url: str, name: str) -> str | None:
    """
    Fast m3u8 video download using ffmpeg (sync version)
    """
    os.makedirs("downloads", exist_ok=True)
    output = f"downloads/{name}.mp4"

    headers = (
        "User-Agent: Mozilla/5.0 (Linux; Android 13)\r\n"
        "Referer: https://player.akamai.net.in/\r\n"
        "Origin: https://akstechnicalclasses.classx.co.in\r\n"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-threads", "2",
        "-bufsize", "8M",
        "-stats_period", "5",
         "-loglevel", "error",
              # multiple threads for faster processing
        "-headers", headers,
        "-multiple_requests", "1",    # parallel segment requests (ffmpeg ≥ 5.1)
        "-i", url,
        "-c", "copy",
                   # bigger buffer for smoother download
        "-bsf:a", "aac_adtstoasc",
        output
    ]

    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if process.returncode == 0 and os.path.exists(output):
        print("✅ Fast download complete:", output)
        return output
    else:
        print("❌ ffmpeg error:", process.stderr.decode())
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
        download_youtube(url, name=os.path.basename(url))
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
# ==============================
# FILE DECRYPT FUNCTION
# ==============================

# ==============================
# RAW FILE DOWNLOAD
# ==============================
import os
import math
import asyncio
import aiohttp
import aiofiles
from tqdm import tqdm

async def download_raw_file(url: str, filename: str) -> str | None:
    """
    Ultra-fast Heroku-safe download for large MKV/MP4 files.
    ✅ Supports resume
    ✅ Parallel chunked download
    ✅ Safe for Heroku environment
    """
    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{filename}.mkv"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        "Referer": "https://akstechnicalclasses.classx.co.in/",
        "Origin": "https://akstechnicalclasses.classx.co.in",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    # Check existing file for resume
    downloaded = 0
    if os.path.exists(file_path):
        downloaded = os.path.getsize(file_path)

    async with aiohttp.ClientSession() as session:
        # Get total file size
        async with session.head(url, headers=headers) as resp:
            if resp.status != 200:
                print(f"❌ Bad status: {resp.status}")
                return None
            total_size = int(resp.headers.get("Content-Length", 0))
            if total_size == 0:
                print("❌ Content-Length missing")
                return None

        # If partially downloaded
        if downloaded > 0:
            headers["Range"] = f"bytes={downloaded}-"

        # Decide number of chunks
        max_chunks = 16
        chunk_size = math.ceil((total_size - downloaded) / max_chunks)

        # Download each chunk
        async def download_chunk(start, end, idx):
            for attempt in range(3):
                try:
                    range_header = {"Range": f"bytes={start}-{end}", **headers}
                    async with session.get(url, headers=range_header) as r:
                        if r.status not in [200, 206]:
                            continue
                        async with aiofiles.open(f"{file_path}.part{idx}", "wb") as f:
                            async for data in r.content.iter_chunked(1024*1024):
                                await f.write(data)
                    return True
                except:
                    await asyncio.sleep(1)
            return False

        # Prepare tasks
        tasks = []
        for i in range(max_chunks):
            start = downloaded + i * chunk_size
            end = min(start + chunk_size - 1, total_size - 1)
            if start > end:
                break
            tasks.append(download_chunk(start, end, i))

        # Run tasks with tqdm
        for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc=filename, ncols=80):
            await f

        # Merge chunks safely
        async with aiofiles.open(file_path, "ab") as out_f:
            for i in range(len(tasks)):
                part_file = f"{file_path}.part{i}"
                if not os.path.exists(part_file):
                    continue
                async with aiofiles.open(part_file, "rb") as part_f:
                    while True:
                        chunk = await part_f.read(1024*1024)
                        if not chunk:
                            break
                        await out_f.write(chunk)
                os.remove(part_file)

    print(f"✅ Download complete: {file_path}")
    return file_path

# DOWNLOAD + DECRYPT WRAPPER
# ==============================
import os
import mmap
import requests
from tqdm import tqdm
from base64 import b64decode




import asyncio
import os
from pathlib import Path

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

async def decrypt_and_merge_video(mpd_url, keys_string, output_path, output_name, quality="720"):
    """
    Same logic as original code but Heroku-friendly & ultra-fast:
    1) Async download with yt-dlp + aria2c
    2) Flexible file detection
    3) Async decrypt
    4) Merge with ffmpeg + faststart
    """
    try:
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        # ------------------------------
        # 1) Download video+audio
        # ------------------------------
        cmd_download = (
            f'yt-dlp -f "bv[height<={quality}]+ba/b" '
            f'-o "{output_path}/file.%(ext)s" '
            f'--allow-unplayable-format --no-check-certificate '
            f'--external-downloader aria2c '
            f'--downloader-args "aria2c:-x 16 -j 32 -s 16 -k 1M" '
            f'"{mpd_url}"'
        )
        print(f"▶️ Downloading: {cmd_download}")
        await run_cmd(cmd_download)

        # ------------------------------
        # 2) Detect downloaded files
        # ------------------------------
        av_files = list(output_path.iterdir())
        print(f"📄 Downloaded files: {av_files}")

        video_decrypted = False
        audio_decrypted = False

        # ------------------------------
        # 3) Decrypt video/audio
        # ------------------------------
        for f in av_files:
            if f.suffix.lower() in [".mp4", ".mkv", ".webm"] and not video_decrypted:
                cmd_video = f'mp4decrypt {keys_string} --show-progress "{f}" "{output_path}/video.mp4"'
                print(f"🔓 Decrypting video: {cmd_video}")
                await run_cmd(cmd_video)
                if (output_path / "video.mp4").exists():
                    video_decrypted = True
                f.unlink()
            elif f.suffix.lower() in [".m4a", ".aac"] and not audio_decrypted:
                cmd_audio = f'mp4decrypt {keys_string} --show-progress "{f}" "{output_path}/audio.m4a"'
                print(f"🔓 Decrypting audio: {cmd_audio}")
                await run_cmd(cmd_audio)
                if (output_path / "audio.m4a").exists():
                    audio_decrypted = True
                f.unlink()

        if not video_decrypted or not audio_decrypted:
            raise FileNotFoundError("❌ Decryption failed: video or audio missing.")

        # ------------------------------
        # 4) Merge video+audio
        # ------------------------------
        merged_file = output_path / f"{output_name}.mp4"
        cmd_merge = (
            f'ffmpeg -y -i "{output_path}/video.mp4" -i "{output_path}/audio.m4a" '
            f'-c copy -movflags +faststart "{merged_file}"'
        )
        print(f"🎬 Merging: {cmd_merge}")
        await run_cmd(cmd_merge)

        # Cleanup decrypted temp files
        (output_path / "video.mp4").unlink(missing_ok=True)
        (output_path / "audio.m4a").unlink(missing_ok=True)

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
import os
import subprocess
import logging

async def download_video(url, cmd, name):
    """
    Heroku-compatible async download with retries & special cases.
    ✅ Ultra fast using aria2c
    ✅ Supports m3u8, zip, YouTube/GoogleVideo, direct URLs
    """
    # ------------------------------
    # 1) Special cases first
    # ------------------------------
    if "transcoded" in url and ".m3u8" in url:
        print("⚡ Handling transcoded m3u8 stream")
        return download_appx_m3u8(url, name)  # your existing function

    if "appx" in url and ".zip" in url:
        print("⚡ Handling appx zip archive")
        return process_zip_to_video(url, name)  # your existing function

    if "googlevideo.com" in url or "youtube.com" in url or "youtu.be" in url or "embed" in url:
        print("⚡ Handling YouTube/GoogleVideo link")
        return download_from_player(url, name)  # your existing function

    # ------------------------------
    # 2) Normal URL download with retries
    # ------------------------------
    retry_count = 0
    max_retries = 2

    while retry_count < max_retries:
        download_cmd = (
            f'{cmd} -R 25 --fragment-retries 25 '
            f'--external-downloader aria2c '
            f'--downloader-args "aria2c:-x 16 -j 32 -s 16 -k 1M"'
        )
        print(f"▶️ Running command: {download_cmd}")
        logging.info(download_cmd)

        # Run command asynchronously
        proc = await asyncio.create_subprocess_shell(
            download_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode == 0:
            print("✅ Download succeeded")
            break
        else:
            retry_count += 1
            print(f"⚠️ Download failed (attempt {retry_count}/{max_retries}), retrying in 5s...")
            if stderr:
                print(f"[stderr] {stderr.decode()}")
            await asyncio.sleep(5)
    else:
        print("❌ All download attempts failed")
        return None

    # ------------------------------
    # 3) Verify output files
    # ------------------------------
    try:
        if os.path.isfile(name):
            return name
        elif os.path.isfile(f"{name}.webm"):
            return f"{name}.webm"
        base = name.split(".")[0]
        if os.path.isfile(f"{base}.mkv"):
            return f"{base}.mkv"
        elif os.path.isfile(f"{base}.mp4"):
            return f"{base}.mp4"
        elif os.path.isfile(f"{base}.mp4.webm"):
            return f"{base}.mp4.webm"

        # fallback
        return base + ".mp4"
    except Exception as exc:
        logging.error(f"Error checking file: {exc}")
        return name

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
async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog, channel_id, watermark="{CREDIT}", topic_thread_id: int = None):
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
