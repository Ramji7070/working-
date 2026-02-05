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
        "-threads", "4",              # multiple threads for faster processing
        "-headers", headers,
        "-multiple_requests", "1",    # parallel segment requests (ffmpeg ≥ 5.1)
        "-i", url,
        "-c", "copy",
        "-bufsize", "10M",            # bigger buffer for smoother download
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
# ==============================
# FILE DECRYPT FUNCTION
# ==============================
def decrypt_file(file_path: str, key: str) -> bool:
    if not file_path or not os.path.exists(file_path):
        return False

    # 👇 NEW SAFETY CHECK
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
# ==============================
# RAW FILE DOWNLOAD
# ==============================
def download_raw_file(url: str, filename: str) -> str | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        "Referer": "https://akstechnicalclasses.classx.co.in/",
        "Origin": "https://akstechnicalclasses.classx.co.in",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{filename}.mkv"

    session = create_session()
    downloaded = 0

    if os.path.exists(file_path):
        downloaded = os.path.getsize(file_path)
        headers["Range"] = f"bytes={downloaded}-"

    try:
        with session.get(url, headers=headers, stream=True, timeout=(10, 180)) as r:
            if r.status_code not in (200, 206):
                print(f"❌ Bad status: {r.status_code}")
                return None

            total = int(r.headers.get("content-length", 0)) + downloaded
            chunk_size = 256 * 1024

            with open(file_path, "ab") as f, tqdm(
                total=total,
                initial=downloaded,
                unit="B",
                unit_scale=True,
                desc=filename,
                ncols=80
            ) as bar:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

        return file_path

    except Exception as e:
        print(f"⚠️ Download interrupted (resume enabled): {e}")
        return file_path if os.path.exists(file_path) else None
# ==============================
# DOWNLOAD + DECRYPT WRAPPER
# ==============================
import os
import mmap
import requests
from tqdm import tqdm
from base64 import b64decode





async def decrypt_and_merge_video(mpd_url, keys_string, output_path, output_name, quality="720"):
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

async def download_video(url, cmd, name):
    """
    Async download handler with retries and special cases.
    """
    # Special cases first
    if "transcoded" in url and ".m3u8" in url:
        print("⚡ Handling transcoded m3u8 stream")
        return download_appx_m3u8(url, name)
    
    if "appx" in url and ".zip" in url:
        print("⚡ Handling appx zip archive")
        return process_zip_to_video(url, name)

    # GoogleVideo / YouTube filter
    if "googlevideo.com" in url or "youtube.com" in url or "youtu.be" in url or "embed" in url:
        print("⚡ Handling YouTube/GoogleVideo link")
        return download_from_player(url, name)

    # Normal case with retries
    retry_count = 0
    max_retries = 2

    while retry_count < max_retries:
        download_cmd = (
            f'{cmd} -R 25 --fragment-retries 25 '
            f'--external-downloader aria2c '
            f'--downloader-args "aria2c: -x 16 -j 32"'
        )
        print(f"▶️ Running command: {download_cmd}")
        logging.info(download_cmd)

        k = subprocess.run(download_cmd, shell=True)
        if k.returncode == 0:
            print("✅ Download succeeded")
            break

        retry_count += 1
        print(f"⚠️ Download failed (attempt {retry_count}/{max_retries}), retrying in 5s...")
        await asyncio.sleep(5)

    # Check output files
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

        return base + ".mp4"
    except Exception as exc:
        logging.error(f"Error checking file: {exc}")
        return name
def download_and_decrypt_video(url: str, name: str, key: str = None) -> str | None:
    if "transcoded" in url and ".m3u8" in url:
        print("⚡ Handling appx m3u8 stream")
        return download_appx_m3u8(url, name)
    

    if "appx" in url and ".zip" in url:
        return process_zip_to_video(url, name)
    
    if "googlevideo.com" in url or "youtube.com" in url or "youtu.be" in url or "embed" in url:
        return download_googlevideo(url, name)


    video_path = None
    for _ in range(5):  # resume attempts
        video_path = download_raw_file(url, name)
        if video_path and os.path.getsize(video_path) > 10 * 1024 * 1024:
            break

    if not video_path:
        return None

    # ✅ अगर decrypt fail भी हो तो original path return करो
    try:
        if decrypt_file(video_path, key):
            return video_path
    except Exception as e:
        print(f"⚠️ Decrypt failed: {e}")

    return video_path  # fallback

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
