import asyncio
from typing import Optional, Dict, Any
import yt_dlp

from config import YDL_FORMAT, YDL_DEFAULT_SEARCH, YDL_NPLAYLIST


def _extract_sync(query: str) -> Dict[str, Any]:
    ydl_opts = {
        "format": YDL_FORMAT,
        "noplaylist": YDL_NPLAYLIST,
        "quiet": True,
        "default_search": YDL_DEFAULT_SEARCH,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            info = info["entries"][0]
        url = info.get("url")
        title = info.get("title") or "Unknown"
        webpage_url = info.get("webpage_url") or query
        duration = info.get("duration")
        return {"url": url, "title": title, "webpage_url": webpage_url, "duration": duration}

def _extract_playlist_sync(playlist_url: str) -> list:
    ydl_opts = {
        "format": YDL_FORMAT,
        "noplaylist": False,
        "quiet": True,
        "default_search": YDL_DEFAULT_SEARCH,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        entries = info["entries"] if "entries" in info else []
        tracks = []
        for entry in entries:
            if not entry:
                continue
            url = entry.get("url")
            title = entry.get("title") or "Unknown"
            webpage_url = entry.get("webpage_url") or playlist_url
            duration = entry.get("duration")
            tracks.append({"url": url, "title": title, "webpage_url": webpage_url, "duration": duration})
        return tracks


async def extract_info(query: str) -> Dict[str, Any]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _extract_sync, query)

async def extract_playlist(playlist_url: str) -> list:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _extract_playlist_sync, playlist_url)
