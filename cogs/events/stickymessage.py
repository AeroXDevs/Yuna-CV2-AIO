"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import discord
import aiosqlite
import json
from discord import ui
from discord.ext import commands
from utils.logger import logger


class StickyMessageListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.setup_database())

    async def setup_database(self):
        async with aiosqlite.connect("db/stickymessages.db") as db:
            await db.execute(
                """CREATE TABLE IF NOT EXISTS sticky_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER,
                    channel_id INTEGER,
                    message_type TEXT,
                    message_content TEXT,
                    embed_data TEXT,
                    enabled INTEGER DEFAULT 1,
                    last_message_id INTEGER
                )"""
            )
            await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if not message.guild:
            return
        
        async with aiosqlite.connect("db/stickymessages.db") as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT * FROM sticky_messages 
                WHERE guild_id = ? AND channel_id = ? AND enabled = 1""",
                (message.guild.id, message.channel.id)
            )
            sticky_data = await cursor.fetchone()
            
            if not sticky_data:
                return
            
            sticky_dict = dict(sticky_data)
            
            if sticky_dict['last_message_id']:
                try:
                    old_message = await message.channel.fetch_message(sticky_dict['last_message_id'])
                    await old_message.delete()
                except:
                    pass
            
            new_sticky_message = None
            
            if sticky_dict['message_type'] == 'text' and sticky_dict['message_content']:
                new_sticky_message = await message.channel.send(sticky_dict['message_content'])
            
            elif sticky_dict['message_type'] == 'container' and sticky_dict['embed_data']:
                try:
                    data = json.loads(sticky_dict['embed_data'])
                    
                    container = ui.Container(accent_color=None)
                    container.add_item(ui.TextDisplay(f"# {data.get('title', 'Sticky Message')}"))
                    container.add_item(ui.Separator())
                    
                    if data.get('thumbnail'):
                        container.add_item(
                            ui.Section(
                                ui.TextDisplay(data.get('content', '')),
                                accessory=ui.Thumbnail(data['thumbnail'])
                            )
                        )
                    else:
                        container.add_item(ui.TextDisplay(data.get('content', '')))
                    
                    view = ui.LayoutView()
                    view.add_item(container)
                    
                    new_sticky_message = await message.channel.send(view=view)
                except Exception as e:
                    logger.error("STICKY", f"Error sending container sticky: {e}")
            
            if new_sticky_message:
                await db.execute(
                    """UPDATE sticky_messages 
                    SET last_message_id = ? 
                    WHERE guild_id = ? AND channel_id = ?""",
                    (new_sticky_message.id, message.guild.id, message.channel.id)
                )
                await db.commit()


async def setup(bot):
    await bot.add_cog(StickyMessageListener(bot))
