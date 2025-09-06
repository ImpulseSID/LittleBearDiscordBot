import asyncio
from dataclasses import dataclass
from typing import Optional, Deque
from collections import deque
import discord
from config import FFMPEG_BEFORE_OPTS, FFMPEG_OPTIONS
from utils.yt_dlp_handler import extract_info

@dataclass
class Track:
    title: str
    stream_url: str
    webpage_url: str
    duration: Optional[int]
    requester_id: int

class GuildPlayer:
    def __init__(self, bot: discord.ext.commands.Bot, guild_id: int):
        self.bot = bot
        self.guild_id = guild_id
        self.queue = deque()
        self.current = None
        self.play_next = asyncio.Event()
        self.voice = None
        self.lock = asyncio.Lock()
        self.player_task = None
        self.lazy_playlist_urls = []
        self.lazy_playlist_requester = None

    def _after(self, error: Optional[Exception]):
        print(f"[GuildPlayer._after] Called with error: {error}")
        if error:
            print(f"[GuildPlayer._after] Error: {error}")
        self.bot.loop.call_soon_threadsafe(self.play_next.set)

    async def ensure_task(self):
        print(f"[GuildPlayer.ensure_task] Called. player_task: {self.player_task}")
        if self.player_task is None or self.player_task.done():
            print("[GuildPlayer.ensure_task] Creating new player_loop task.")
            self.player_task = self.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        print("[GuildPlayer.player_loop] Started.")
        while True:
            self.play_next.clear()
            print(f"[GuildPlayer.player_loop] Queue: {list(self.queue)}")
            if not self.queue:
                # True lazy loading: if playlist URLs remain, load the next one
                if self.lazy_playlist_urls and len(self.lazy_playlist_urls) > 0:
                    next_url = self.lazy_playlist_urls.pop(0)
                    from utils.yt_dlp_handler import extract_info
                    try:
                        info = await extract_info(next_url)
                        if not info or not info.get("url"):
                            print(f"[GuildPlayer.player_loop] Skipped unavailable/age-restricted video: {next_url}")
                            continue
                        track = Track(
                            title=info["title"],
                            stream_url=info["url"],
                            webpage_url=info["webpage_url"],
                            duration=info.get("duration"),
                            requester_id=self.lazy_playlist_requester or 0,
                        )
                        self.queue.append(track)
                        print(f"[GuildPlayer.player_loop] Lazy loaded and queued: {track.title}")
                    except Exception as e:
                        print(f"[GuildPlayer.player_loop] Failed to lazy load track: {e}")
                        continue
                else:
                    try:
                        print("[GuildPlayer.player_loop] Waiting for next track or timeout.")
                        await asyncio.wait_for(self.play_next.wait(), timeout=300)
                        print("[GuildPlayer.player_loop] play_next event set.")
                        continue
                    except asyncio.TimeoutError:
                        print("[GuildPlayer.player_loop] Timeout reached, disconnecting.")
                        if self.voice and self.voice.is_connected():
                            await self.voice.disconnect(force=True)
                        self.current = None
                        # Reset lazy playlist state
                        self.lazy_playlist_urls = []
                        self.lazy_playlist_requester = None
                        return
            self.current = self.queue.popleft()
            print(f"[GuildPlayer.player_loop] Now playing: {self.current}")
            if not self.voice or not self.voice.is_connected():
                print("[GuildPlayer.player_loop] Not connected to voice, skipping track.")
                self.current = None
                continue
            try:
                source = discord.FFmpegPCMAudio(self.current.stream_url, before_options=FFMPEG_BEFORE_OPTS, options=FFMPEG_OPTIONS)
                self.voice.play(source, after=self._after)
                print(f"[GuildPlayer.player_loop] Started playback: {self.current.title}")
            except Exception as e:
                print(f"[GuildPlayer.player_loop] Error starting playback: {e}")
            await self.play_next.wait()
            print("[GuildPlayer.player_loop] Track ended or skipped.")

    async def join(self, channel: discord.VoiceChannel):
        print(f"[GuildPlayer.join] Called with channel: {channel}")
        try:
            if self.voice and self.voice.channel == channel:
                print("[GuildPlayer.join] Already in target channel.")
                return
            if self.voice and self.voice.is_connected():
                print(f"[GuildPlayer.join] Moving to channel: {channel}")
                await self.voice.move_to(channel)
            else:
                print(f"[GuildPlayer.join] Connecting to channel: {channel}")
                self.voice = await channel.connect()
        except Exception as e:
            print(f"[GuildPlayer.join] Exception: {e}")
            raise

    async def add(self, track: Track):
        print(f"[GuildPlayer.add] Adding track: {track}")
        self.queue.append(track)
        await self.ensure_task()

    async def skip(self) -> bool:
        print("[GuildPlayer.skip] Called.")
        if self.voice and self.voice.is_playing():
            print("[GuildPlayer.skip] Stopping current track.")
            self.voice.stop()
            return True
        print("[GuildPlayer.skip] Nothing is playing.")
        return False

    async def stop(self):
        print("[GuildPlayer.stop] Called. Clearing queue and stopping playback.")
        self.queue.clear()
        if self.voice and self.voice.is_playing():
            self.voice.stop()
        self.current = None

    async def pause(self) -> bool:
        print("[GuildPlayer.pause] Called.")
        if self.voice and self.voice.is_playing():
            print("[GuildPlayer.pause] Pausing playback.")
            self.voice.pause()
            return True
        print("[GuildPlayer.pause] Nothing is playing.")
        return False

    async def resume(self) -> bool:
        print("[GuildPlayer.resume] Called.")
        if self.voice and self.voice.is_paused():
            print("[GuildPlayer.resume] Resuming playback.")
            self.voice.resume()
            return True
        print("[GuildPlayer.resume] Nothing is paused.")
        return False
