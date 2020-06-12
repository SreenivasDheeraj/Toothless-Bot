#######################################################################################################################################
##Toothless
import asyncio
import functools
import itertools
import math
import random
import asyncpg

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions , Bot
from itertools import cycle

###########################################-----Bot Initialisation-----#######################################################

bot = commands.Bot(command_prefix = "")
###########################################-----Events-----####################################################################

async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database = "Discord_test", user ="postgres", password = "Dheeru@1612")

import os
for cog in os.listdir(os.path.abspath("Cogs")):
    if cog.endswith(".py"):
        try:
            cog = f"Cogs.{cog.replace('.py','')}"
            bot.load_extension(cog)
            print("Loaded ",cog)
        
        except Exception as e:
            print(f"{cog} cannot be loaded")
            raise e

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle , activity = discord.Game("Havana"))
    print("Bot is ready")
    change_status.start() #background task

@bot.event
async def on_member_remover(member):
    print(f'{member} has left the server')

@bot.event
async def on_member_join(member):
    print(f'{member} has joined server')

@bot.event
async def on_command_error(ctx, error):
    if(isinstance(error, commands.CommandNotFound)):
        await ctx.send("Invalid command used")
    if(isinstance(error, commands.MissingRequiredArgument)):
        await ctx.send("Please pass arguments")

##########################################-----ping -----#######################################################

@bot.command( name = "ping", pass_context = True) 
async def ping(context):
    await context.send(f"Pong! {round(bot.latency*1000)}ms")

###########################################-----8 ball-----#####################################################

@bot.command(name = '8ball', pass_context = True , aliases = ["test","_ball"])
async def eight_ball(context,*,qustion):
    # Imports
    import random

    print("Trigerred 8ball Reponse to", context)
    possible_responses=['As I see it, yes',
    'Ask again later',
    'Better not tell you now',
    'Cannot predict now',
    'Concentrate and ask again',
    'Don’t count on it',
    'It is certain',
    'It is decidedly so',
    'Most likely',
    'My reply is no',
    'My sources say no',
    'Outlook not so good',
    'Outlook good',
    'Reply hazy, try again',
    'Signs point to yes',
    'Very doubtful',
    'Without a doubt',
    'Yes',
    'Yes – definitely',
    "You may rely on it"]
    await context.channel.send(random.choice(possible_responses) + context.message.author.mention)
    return

############################################-------Clear Messages------#######################################################

@bot.command(name = "clear", pass_context = True )
@commands.has_permissions(manage_messages = True)
async def clear(context, amount = 5 ):
    await context.channel.purge( limit=amount)
    print(f"Cleared {amount} meassages")   

##########################################-----Kick-----#################################################################

@bot.command( name = 'kick', pass_context = True )
@has_permissions( kick_members = True )
async def kick( context , user:discord.Member , * , reasons = None ):
    try:
        if reasons == None:
            reasons = "no reason :person_shrugging:"
        await user.kick(reason = reasons)
        embed = discord.Embed(title = "User Kicked!", description = ("**"+user.mention+"** was kicked by **"+str(context.message.author.mention)+"** because "+reasons).format(user, context.message.author), color=0xff00f6)
        await context.send(embed = embed)
        await user.send(embed = embed)
    except discord.Forbidden:
        await context.send("Nice try but you do not have permission qt :stuck_out_tongue_winking_eye:"+context.message.author.mention)
    
    return
############################################-----Ban a user--- --#######################################################

@bot.command(name = 'ban',pass_context=True)
@has_permissions(ban_members = True)
async def ban(context , user:discord.Member , * , reasons=None ):
    if reasons == None:
        reasons = "no reason :person_shrugging:"
    await user.ban(reason = reasons)
    embed=discord.Embed(title="User banned!", description=("**"+user.mention+"** was banned by **"+str(context.message.author.mention)+"** because "+reasons).format(user, context.message.author), color=0xff00f6)
    await context.send( embed = embed )
    await user.send( embed = embed )

############################################-----unban a user-----####################################################

@bot.command(name = "unban", pass_context = True)
async def unban(context , * , member ):
    banned_users = await context.guild.bans()
    member_name , member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if( user.name , user.discriminator ) == ( member_name, member_discriminator ):
            await context.guild.unban(user)
            print(f"Unbanned {user.name}#{user.discriminator}")
            await context.send(f"Unbanned {user.name}#{user.discriminator}")
            return 

#############################################-----Reminders-----#################################################
'''
@bot.command(name = "remind", pass_context = True)
async def remind( ctx ):
    getTime()
    args = ctx.message.content
    args = args.split(' ')
    try:
        if('s' in args[2]):
            time = int(args[2].replace('s',' '))
            await ctx.send(f"Will remind in {str(args[2].replace('s',' '))} to {str(args[1])}")
            await asyncio.sleep(time)
            await ctx.send(ctx.message.author,f"You asked me to remind to {str(args[1])} {str(time)} seconds from {str(getTime())}")
    except:
        pass
'''
#############################################-----Background tasks-----###############################################
# must import itertools(cycle) and discord.ext (tasks)

status=cycle(["Senorita","Bad Things","Havana"])

@tasks.loop(seconds=300)
async def change_status():
    await bot.change_presence(activity = discord.Game(next(status)))

################################################------Music Plugin-----#############################################################################
# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass

class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return iter( self._queue.__iter__() )

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

 ###########################################-----Join-----#######################################################
    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Join the voice channel author is in"""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

 ###########################################-----Summon-----#######################################################
    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

 ###########################################-----Leave-----#######################################################
    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

 ###########################################-----Volume-----#######################################################
    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume : int = 30):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if ( volume < 0 or volume > 100 ):
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.current.source.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))
            
 ###########################################-----Current-----#######################################################
    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""
        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')
        await ctx.send(embed=ctx.voice_state.current.create_embed())

 ##########################################-----Pause-----#######################################################
    @commands.command(name='pause')
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""
        
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')
        else:
            await ctx.send("Not playing any music right now... ")
        '''
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f'**`{ctx.author}`**: Paused the song!')
        await ctx.message.add_reaction('⏯')
        '''

 ###########################################-----Resume-----#######################################################
    @commands.command(name='resume')
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""
        '''
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f'**`{ctx.author}`**: Resumed the song!')
        await ctx.message.add_reaction('⏯')
        '''
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')
        else:
            await ctx.send("Not playing any music right now... ")

 ###########################################-----Stop-----#######################################################
    @commands.command(name='stop')
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""
        
        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')
        else:
            await ctx.send("Not playing any music right now...")
        
 ##########################################-----Skip-----#######################################################
    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 1:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

 ###########################################-----Queue-----#######################################################
    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """
        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

 ###########################################-----Shuffle-----#######################################################
    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""
        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

 ###########################################-----Remove-----#######################################################
    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""
        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        return await ctx.message.add_reaction('✅')

 ###########################################-----Play-----#######################################################
    @commands.command(name='play')
    async def _play(self, ctx: commands.Context, *, search: str ):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
               """
        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')

 ###########################################-----My songlist-----#####################################################
    @commands.command(name='fav')
    async def _fav(self, ctx: commands.Context):
        """Shows a list of fav songs.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """
        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        list = ["Bad Things","Senorita camila shawn","Beautiful bazzi camila","Hearts on fire passenger","First man camila","Havana audio camila","Easy camila","I know hat you did last summer","Dream of you","1000 years christina","side to side","NASA song ariana"]
        for i in list:
            async with ctx.typing():
                try:
                    source = await YTDLSource.create_source(ctx, i, loop=self.bot.loop)
                except YTDLError as e:
                    await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
                else:
                    song = Song(source)

                    await ctx.voice_state.songs.put(song)
                    await ctx.send('Enqueued {}'.format(str(source)))
        return

bot.loop.run_until_complete(create_db_pool())

bot.add_cog(Music(bot))

bot.run("NzE3MzkyNzIwMTA0MjU5NjE0.XtZqLg.ChRLy7LuhArMNo2bNLenkZq2LYs")
