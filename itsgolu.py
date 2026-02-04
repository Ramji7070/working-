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
    Ultra-fast m3u8 download using ffmpeg with:
    - Multiple threads
    - Parallel segment requests
    - Retry on failure
    - Faststart for mobile/telegram compatibility
    """
    os.makedirs("downloads", exist_ok=True)
    output = f"downloads/{name}.mp4"

    headers = (
        "User-Agent: Mozilla/5.0 (Linux; Android 13)\r\n"
        "Referer: https://player.akamai.net.in/\r\n"
        "Origin: https://akstechnicalclasses.classx.co.in\r\n"
        "Accept: */*\r\n"
    )

    # FFmpeg command
    cmd = [
        "ffmpeg",
        "-y",
        "-threads", "16",                   # multi-threaded
        "-http_persistent", "1",            # persistent HTTP connection
        "-multiple_requests", "1",           # parallel segment download
        "-reconnect", "1",                   # auto reconnect
        "-reconnect_at_eof", "1",
        "-reconnect_streamed", "1",
        "-reconnect_delay_max", "5",
        "-headers", headers,
        "-i", url,
        "-c:v", "copy",
        "-c:a", "aac",
        "-bsf:a", "aac_adtstoasc",
        "-movflags", "+faststart",          # for smooth streaming
        output
    ]

    print(f"⚡ Ultra-fast FFmpeg download started: {name}")

    try:
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3600)
        if process.returncode == 0 and os.path.exists(output):
            print("✅ Download completed successfully:", output)
            return output
        else:
            print("❌ FFmpeg failed, retrying once...")
            print(process.stderr.decode())

            # Retry once more
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3600)
            if process.returncode == 0 and os.path.exists(output):
                print("✅ Download succeeded on retry:", output)
                return output
            else:
                print("❌ Retry failed:\n", process.stderr.decode())
                return None

    except subprocess.TimeoutExpired:
        print("❌ FFmpeg timed out!")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
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

def duration(filename: str) -> float:
    """
    Get video duration in seconds using ffprobe.
    Returns 0.0 if duration cannot be determined.
    """
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                filename
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        output = result.stdout.decode().strip()
        return float(output) if output else 0.0
    except Exception as e:
        print(f"⚠️ ffprobe error for {filename}: {e}")
        return 0.0




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
import os
import mmap
import subprocess

def repair_mp4(input_file: str) -> bool:
    """
    Repair MP4 file to make it streamable (faststart).
    Returns True if successful.
    """
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return False

    fixed = input_file.replace(".mp4", "_fixed.mp4")
    try:
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_file,
            "-map", "0",
            "-c", "copy",
            "-movflags", "+faststart",
            fixed
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"❌ FFmpeg repair failed:\n{result.stderr.decode()}")
            return False

        # Replace original file
        os.replace(fixed, input_file)
        print(f"✅ MP4 repaired successfully: {input_file}")
        return True

    except Exception as e:
        print(f"❌ Exception during repair_mp4: {e}")
        return False


def decrypt_file_fixed(file_path: str, key: str) -> bool:
    """
    XOR decrypt first 2KB of file (safe for headers)
    Returns True if successful
    """
    if not file_path or not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    if not key:
        return True  # nothing to decrypt

    try:
        key_bytes = key.encode()
        file_size = os.path.getsize(file_path)
        decrypt_size = min(1024*2, file_size)  # first 2KB only

        with open(file_path, "r+b") as f:
            with mmap.mmap(f.fileno(), decrypt_size, access=mmap.ACCESS_WRITE) as mm:
                for i in range(decrypt_size):
                    mm[i] ^= key_bytes[i % len(key_bytes)]

        print(f"✅ File decrypted successfully: {file_path}")
        return True

    except Exception as e:
        print(f"❌ Exception during decrypt_file_fixed: {e}")
        return False

# ==============================
# RAW FILE DOWNLOAD
# ==============================
import os
import math
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def download_raw_file_fast(url: str, filename: str, threads: int = 8) -> str | None:
    """
    Ultra-fast multi-threaded download with resume support
    """
    os.makedirs("downloads", exist_ok=True)
    file_path = f"downloads/{filename}.mkv"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        "Referer": "https://akstechnicalclasses.classx.co.in/",
        "Origin": "https://akstechnicalclasses.classx.co.in"
    }

    # Check if server supports Range requests
    r = requests.head(url, headers=headers, allow_redirects=True)
    if r.status_code != 200:
        print(f"❌ Server returned {r.status_code}")
        return None
    total_size = int(r.headers.get("content-length", 0))
    if total_size == 0:
        print("❌ Could not get content length")
        return None

    # If file exists, resume
    if os.path.exists(file_path):
        existing_size = os.path.getsize(file_path)
        if existing_size >= total_size:
            print("✅ File already downloaded")
            return file_path
    else:
        existing_size = 0

    # Split ranges for threads
    ranges = []
    part_size = math.ceil((total_size - existing_size) / threads)
    for i in range(threads):
        start = existing_size + i * part_size
        end = min(start + part_size - 1, total_size - 1)
        if start <= end:
            ranges.append((start, end))

    def download_range(start_end):
        start, end = start_end
        hdrs = headers.copy()
        hdrs["Range"] = f"bytes={start}-{end}"
        try:
            r = requests.get(url, headers=hdrs, stream=True, timeout=(10, 180))
            if r.status_code not in (200, 206):
                return None
            data = r.content
            with open(file_path, "r+b" if os.path.exists(file_path) else "wb") as f:
                f.seek(start)
                f.write(data)
            return len(data)
        except:
            return None

    # Make file with total size first
    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.truncate(total_size)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(tqdm(executor.map(download_range, ranges),
                            total=len(ranges),
                            desc=filename,
                            ncols=80))

    if sum([r or 0 for r in results]) >= total_size - existing_size:
        print("✅ Download complete:", file_path)
        return file_path
    else:
        print("⚠️ Download incomplete")
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
    


async def download_video(url, cmd, name):
    """
    Async download handler with retries and special cases.
    """
    # Special cases first
    if "transcoded" in url and ".m3u8" in url:
        print("⚡ Handling transcoded m3u8 stream")
        return download_appx_m3u8(url, name)
async def download_video(url, cmd, name):
    """
    Ultra-fast download handler with retries and special cases.
    """
    # --- Special cases ---
    if "transcoded" in url and ".m3u8" in url:
        print("⚡ Handling transcoded m3u8 stream")
        return download_appx_m3u8(url, name)
    
    

    # --- Normal case with retries ---
    retry_count = 0
    max_retries = 3  # Increased retries
    while retry_count < max_retries:
        # Add aria2c optimized for ultra-fast
        download_cmd = (
            f'{cmd} -R 25 --fragment-retries 25 '
            f'--external-downloader aria2c '
            f'--downloader-args "aria2c: -x 16 -j 32 -s 32 -k 1M"'
        )
        print(f"▶️ Running command: {download_cmd}")
        import logging
        logging.info(download_cmd)

        k = subprocess.run(download_cmd, shell=True)
        if k.returncode == 0:
            print("✅ Download succeeded")
            break

        retry_count += 1
        print(f"⚠️ Download failed (attempt {retry_count}/{max_retries}), retrying in 3s...")
        await asyncio.sleep(3)

    # --- Check output files ---
    try:
        if os.path.isfile(name):
            return name
        base = os.path.splitext(name)[0]
        for ext in [".webm", ".mkv", ".mp4", ".mp4.webm"]:
            fcheck = base + ext
            if os.path.isfile(fcheck):
                return fcheck
        return base + ".mp4"
    except Exception as exc:
        logging.error(f"Error checking file: {exc}")
        return name


async def download_and_decrypt_video(url: str, name: str, key: str = None) -> str | None:
    file_path = None

    # Handle special links first
    if ".m3u8" in url and "appx" in url:
        file_path = download_appx_m3u8(url, name)
    elif "appx" in url and ".zip" in url:
        from zip_handler import process_zip_to_video
        file_path = process_zip_to_video(url, name)
    else:
        # Fast raw download
        file_path = await download_raw_file_fast(url, f"{name}")

    if not file_path or not os.path.exists(file_path):
        print("❌ Download failed")
        return None

    # Decrypt
    decrypt_file_fixed(file_path, key)

    # Repair only if it's .mp4
    if file_path.endswith(".mp4"):
        repair_mp4(file_path)

    return file_path

import os
import time
import subprocess
from pyrogram import Client
from pyrogram.types import Message

async def send_vid(
    bot: Client,
    m: Message,
    cc,
    filename,
    thumb,
    name,
    prog,
    channel_id,
    watermark="{CREDIT}",
    topic_thread_id: int = None
):
    try:
        temp_thumb = None
        thumbnail = thumb

        # ------------------------------
        # Thumbnail Generation + Watermark
        # ------------------------------
        if thumb in ["/d", "no"] or not os.path.exists(thumb):
            temp_thumb = f"downloads/thumb_{os.path.basename(filename)}.jpg"
            subprocess.run(
                f'ffmpeg -i "{filename}" -ss 00:00:10 -vframes 1 -q:v 2 -y "{temp_thumb}"',
                shell=True
            )

            if os.path.exists(temp_thumb) and (watermark and watermark.strip() != "/d"):
                text_to_draw = watermark.strip()
                try:
                    probe_out = subprocess.check_output(
                        f'ffprobe -v error -select_streams v:0 -show_entries stream=width '
                        f'-of csv=p=0:s=x "{temp_thumb}"',
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

        # ------------------------------
        # Progress Messages
        # ------------------------------
        await prog.delete(True)
        reply1 = await bot.send_message(channel_id, f" **Uploading Video:**\n<blockquote>{name}</blockquote>")
        reply = await m.reply_text(f"🖼 **Generating Thumbnail:**\n<blockquote>{name}</blockquote>")

        file_size_mb = os.path.getsize(filename) / (1024 * 1024)
        notify_split = None
        sent_message = None

        # ------------------------------
        # Case A: File < 2GB
        # ------------------------------
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

            if os.path.exists(filename):
                os.remove(filename)
            await reply.delete(True)
            await reply1.delete(True)

        # ------------------------------
        # Case B: File ≥ 2GB → Split
        # ------------------------------
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

            if len(parts) > 1:
                await m.reply_text("✅ Large video successfully uploaded in multiple parts!")

            await reply.delete(True)
            await reply1.delete(True)
            if notify_split:
                await notify_split.delete(True)
            if os.path.exists(filename):
                os.remove(filename)

            sent_message = first_part_message

        # ------------------------------
        # Cleanup Thumbnail
        # ------------------------------
        if thumb in ["/d", "no"] and temp_thumb and os.path.exists(temp_thumb):
            os.remove(temp_thumb)

        return sent_message

    except Exception as err:
        raise Exception(f"send_vid failed: {err}")
