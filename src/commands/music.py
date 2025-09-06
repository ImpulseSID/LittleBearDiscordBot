import random
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional, Dict
from utils.player import Track, GuildPlayer
from config import FFMPEG_BEFORE_OPTS, FFMPEG_OPTIONS
from utils.yt_dlp_handler import extract_info


class Music(commands.Cog):

    @app_commands.command(name="playlist", description="Play and queue all tracks from a YouTube playlist URL (true lazy loading)")
    async def playlist(self, interaction: discord.Interaction, url: str):
        print(f"[Music.playlist] Called by user: {interaction.user} with url: {url}")
        if not interaction.guild:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return
        player = self.get_player(interaction.guild)
        user_vc = getattr(getattr(interaction.user, "voice", None), "channel", None)
        print(f"[Music.playlist] user_vc: {user_vc}")
        if not player.voice or not player.voice.is_connected():
            if user_vc:
                await player.join(user_vc)
            else:
                await interaction.response.send_message("You must be in a voice channel or specify one.", ephemeral=True)
                return
        await interaction.response.defer()
        from utils.yt_dlp_handler import extract_playlist
        try:
            tracks = await extract_playlist(url)
            print(f"[Music.playlist] Extracted {len(tracks)} tracks from playlist.")
        except Exception as e:
            await interaction.followup.send(f"Failed to extract playlist: {e}")
            print(f"[Music.playlist] Exception extracting playlist: {e}")
            if player.voice and player.voice.is_connected():
                await player.voice.disconnect(force=True)
            return
        if not tracks or len(tracks) == 0:
            await interaction.followup.send("No tracks found in playlist.")
            print("[Music.playlist] No tracks found in playlist.")
            if player.voice and player.voice.is_connected():
                await player.voice.disconnect(force=True)
            return
        # Only queue the first track, store the rest for lazy loading
        first_track_info = None
        rest_urls = []
        for idx, info in enumerate(tracks):
            if info.get("url") and info.get("title"):
                if not first_track_info:
                    first_track_info = info
                else:
                    rest_urls.append(info["webpage_url"])
        if not first_track_info:
            await interaction.followup.send("No playable tracks found in playlist.")
            print("[Music.playlist] No playable tracks after filtering.")
            if player.voice and player.voice.is_connected():
                await player.voice.disconnect(force=True)
            return
        track = Track(
            title=first_track_info["title"],
            stream_url=first_track_info["url"],
            webpage_url=first_track_info["webpage_url"],
            duration=first_track_info.get("duration"),
            requester_id=interaction.user.id,
        )
        await player.add(track)
        player.lazy_playlist_urls = rest_urls
        player.lazy_playlist_requester = interaction.user.id
        if player.current is None and (not player.voice or not player.voice.is_playing()):
            player.play_next.set()
        msg = f"Queued: [{track.title}]({track.webpage_url}) from playlist. Remaining tracks will load as each finishes."
        await interaction.followup.send(msg)
        print(f"[Music.playlist] {msg}")
    def __init__(self, bot: commands.Bot):
        print("[Music.__init__] Initializing Music cog.")
        self.bot = bot
        self.players: Dict[int, GuildPlayer] = {}

    def get_player(self, guild: discord.Guild) -> GuildPlayer:
        print(f"[Music.get_player] Called for guild: {guild.id}")
        player = self.players.get(guild.id)
        if not player:
            print(f"[Music.get_player] Creating new GuildPlayer for guild: {guild.id}")
            player = GuildPlayer(self.bot, guild.id)
            self.players[guild.id] = player
        return player

    @app_commands.command(name="queueadd", description="Add a track to the queue by URL without interrupting playback")
    async def queueadd(self, interaction: discord.Interaction, url: str):
        print(f"[Music.queueadd] Called by user: {interaction.user} with url: {url}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.queueadd] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        user_vc = getattr(getattr(interaction.user, "voice", None), "channel", None)
        print(f"[Music.queueadd] user_vc: {user_vc}")
        if not player.voice or not player.voice.is_connected():
            if not user_vc:
                await interaction.response.send_message("Join a voice channel first or use /join.")
                print("[Music.queueadd] User not in a voice channel.")
                return
            try:
                await player.join(user_vc)
            except Exception as e:
                await interaction.response.send_message(f"Failed to join VC: {e}")
                print(f"[Music.queueadd] Exception joining VC: {e}")
                return
        await interaction.response.defer()
        try:
            info = await extract_info(url)
            print(f"[Music.queueadd] Extracted info: {info}")
        except Exception as e:
            await interaction.followup.send(f"Failed to extract info: {e}")
            print(f"[Music.queueadd] Exception extracting info: {e}")
            return
        track = Track(
            title=info["title"],
            stream_url=info["url"],
            webpage_url=info["webpage_url"],
            duration=info.get("duration"),
            requester_id=interaction.user.id,
        )
        await player.add(track)
        await interaction.followup.send(f"Queued: [{track.title}]({track.webpage_url})")
        print(f"[Music.queueadd] Queued: {track.title}")

    @app_commands.command(name="join", description="Join a voice channel")
    async def join(self, interaction: discord.Interaction, channel: Optional[discord.VoiceChannel] = None):
        print(f"[Music.join] Called by user: {interaction.user} in guild: {getattr(interaction.guild, 'id', None)}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.join] Not in a guild.")
            return

        await interaction.response.defer()

        user_vc = getattr(getattr(interaction.user, "voice", None), "channel", None)
        print(f"[Music.join] user_vc: {user_vc}, channel param: {channel}")
        target = channel or user_vc
        if not target:
            await interaction.followup.send("Join a voice channel or specify one.")
            print("[Music.join] No target channel found.")
            return
        player = self.get_player(interaction.guild)
        try:
            await player.join(target)
            await interaction.followup.send(f"Joined {target.name}")
            print(f"[Music.join] Joined {target.name}")
        except Exception as e:
            await interaction.followup.send(f"Failed to join: {e}")
            print(f"[Music.join] Exception: {e}")

    @app_commands.command(name="play", description="Play a track by URL or add to queue")
    async def play(self, interaction: discord.Interaction, url: str):
        print(f"[Music.play] Called by user: {interaction.user} with url: {url}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.play] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        user_vc = getattr(getattr(interaction.user, "voice", None), "channel", None)
        print(f"[Music.play] user_vc: {user_vc}")
        if not player.voice or not player.voice.is_connected():
            if not user_vc:
                await interaction.response.send_message("Join a voice channel first or use /join.")
                print("[Music.play] User not in a voice channel.")
                return
            try:
                await player.join(user_vc)
            except Exception as e:
                await interaction.response.send_message(f"Failed to join VC: {e}")
                print(f"[Music.play] Exception joining VC: {e}")
                return
        await interaction.response.defer()
        try:
            info = await extract_info(url)
            print(f"[Music.play] Extracted info: {info}")
        except Exception as e:
            await interaction.followup.send(f"Failed to extract info: {e}")
            print(f"[Music.play] Exception extracting info: {e}")
            return
        track = Track(
            title=info["title"],
            stream_url=info["url"],
            webpage_url=info["webpage_url"],
            duration=info.get("duration"),
            requester_id=interaction.user.id,
        )
        await player.add(track)
        if player.current is None and (not player.voice or not player.voice.is_playing()):
            player.play_next.set()
        await interaction.followup.send(f"Queued: [{track.title}]({track.webpage_url})")
        print(f"[Music.play] Queued: {track.title}")

    @app_commands.command(name="skip", description="Skip current track")
    async def skip(self, interaction: discord.Interaction):
        print(f"[Music.skip] Called by user: {interaction.user}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.skip] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        ok = await player.skip()
        await interaction.response.send_message("Skipped" if ok else "Nothing playing")
        print(f"[Music.skip] Result: {'Skipped' if ok else 'Nothing playing'}")

    @app_commands.command(name="pause", description="Pause playback")
    async def pause(self, interaction: discord.Interaction):
        print(f"[Music.pause] Called by user: {interaction.user}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.pause] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        ok = await player.pause()
        await interaction.response.send_message("Paused" if ok else "Nothing playing")
        print(f"[Music.pause] Result: {'Paused' if ok else 'Nothing playing'}")

    @app_commands.command(name="resume", description="Resume playback")
    async def resume(self, interaction: discord.Interaction):
        print(f"[Music.resume] Called by user: {interaction.user}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.resume] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        ok = await player.resume()
        await interaction.response.send_message("Resumed" if ok else "Nothing to resume")
        print(f"[Music.resume] Result: {'Resumed' if ok else 'Nothing to resume'}")

    @app_commands.command(name="stop", description="Stop and clear the queue")
    async def stop(self, interaction: discord.Interaction):
        print(f"[Music.stop] Called by user: {interaction.user}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.stop] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        await player.stop()
        await interaction.response.send_message("Stopped")
        print("[Music.stop] Stopped and cleared queue.")

    @app_commands.command(name="queue", description="Show the queue")
    async def queue(self, interaction: discord.Interaction):
        print(f"[Music.queue] Called by user: {interaction.user}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.queue] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        items = list(player.queue)
        print(f"[Music.queue] Queue items: {items}")
        if not items:
            await interaction.response.send_message("Queue is empty")
            print("[Music.queue] Queue is empty.")
            return
        lines = []
        for i, t in enumerate(items, start=1):
            lines.append(f"{i}. {t.title}")
        await interaction.response.send_message("\n".join(lines))
        print(f"[Music.queue] Sent queue list.")

    @app_commands.command(name="nowplaying", description="Show current track")
    async def nowplaying(self, interaction: discord.Interaction):
        print(f"[Music.nowplaying] Called by user: {interaction.user}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.nowplaying] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        if not player.current:
            await interaction.response.send_message("Nothing playing")
            print("[Music.nowplaying] Nothing playing.")
            return
        t = player.current
        await interaction.response.send_message(f"Now Playing: [{t.title}]({t.webpage_url})")
        print(f"[Music.nowplaying] Now playing: {t.title}")

    @app_commands.command(name="shuffle", description="Shuffle the queue")
    async def shuffle(self, interaction: discord.Interaction):
        print(f"[Music.shuffle] Called by user: {interaction.user}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.shuffle] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        q = list(player.queue)
        print(f"[Music.shuffle] Queue before shuffle: {q}")
        if len(q) < 2:
            await interaction.response.send_message("Not enough items to shuffle")
            print("[Music.shuffle] Not enough items to shuffle.")
            return
        random.shuffle(q)
        player.queue.clear()
        player.queue.extend(q)
        await interaction.response.send_message("Shuffled queue")
        print(f"[Music.shuffle] Queue after shuffle: {q}")

    @app_commands.command(name="clear", description="Clear the queue")
    async def clear(self, interaction: discord.Interaction):
        print(f"[Music.clear] Called by user: {interaction.user}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.clear] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        player.queue.clear()
        await interaction.response.send_message("Cleared queue")
        print("[Music.clear] Cleared queue.")

    @app_commands.command(name="remove", description="Remove item from queue by index (1-based)")
    async def remove(self, interaction: discord.Interaction, index: int):
        print(f"[Music.remove] Called by user: {interaction.user} with index: {index}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.remove] Not in a guild.")
            return
        if index < 1:
            await interaction.response.send_message("Index must be >= 1")
            print("[Music.remove] Index < 1.")
            return
        player = self.get_player(interaction.guild)
        if index > len(player.queue):
            await interaction.response.send_message("No such index")
            print("[Music.remove] No such index.")
            return
        q = list(player.queue)
        removed = q.pop(index - 1)
        player.queue.clear()
        player.queue.extend(q)
        await interaction.response.send_message(f"Removed: {removed.title}")
        print(f"[Music.remove] Removed: {removed.title}")

    @app_commands.command(name="leave", description="Leave the voice channel")
    async def leave(self, interaction: discord.Interaction):
        print(f"[Music.leave] Called by user: {interaction.user}")
        if not interaction.guild:
            await interaction.response.send_message("Guild only.")
            print("[Music.leave] Not in a guild.")
            return
        player = self.get_player(interaction.guild)
        if player.voice and player.voice.is_connected():
            await player.stop()
            await player.voice.disconnect(force=True)
            await interaction.response.send_message("Left voice channel")
            print("[Music.leave] Left voice channel.")
        else:
            await interaction.response.send_message("Not connected")
            print("[Music.leave] Not connected.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))

