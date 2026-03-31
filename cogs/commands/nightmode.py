"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import discord 
from discord .ext import commands 
from discord import ui
import aiosqlite 
import os 
from utils .Tools import *


db_folder ='db'
db_file ='anti.db'
db_path =os .path .join (db_folder ,db_file )

class Nightmode (commands .Cog ):

    def __init__ (self ,bot ):
        self .bot =bot 
        self .bot .loop .create_task (self .initialize_db ())

    async def initialize_db (self ):
        from db._db import Database
        self .db = Database(db_path)
        db_conn = await self .db .connect()
        
        async def create_table():
            await db_conn.execute('''
                CREATE TABLE IF NOT EXISTS Nightmode (
                    guildId TEXT,
                    roleId TEXT,
                    adminPermissions INTEGER
                )
            ''')
            await db_conn.commit()
        
        await self.db.execute_with_retries(create_table)

    async def is_extra_owner (self ,user ,guild ):
        db_conn = await self.db.ensure_connection()
        async with db_conn.execute('''
            SELECT owner_id FROM extraowners WHERE guild_id = ? AND owner_id = ?
        ''',(guild .id ,user .id ))as cursor :
            extra_owner =await cursor .fetchone ()
        return extra_owner is not None 

    @commands .hybrid_group (name ="nightmode",aliases =[],help ="Manages Nightmode feature",invoke_without_command =True )
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,10 ,commands .BucketType .user )
    @commands .max_concurrency (1 ,per =commands .BucketType .default ,wait =False )
    @commands .guild_only ()
    async def nightmode (self ,ctx ):
        view = ui.LayoutView()
        container = ui.Container(accent_color=None)
        
        container.add_item(ui.TextDisplay(f"# {ctx.guild.name} Nightmode Management"))
        container.add_item(ui.Separator())
        
        main_info = (
            "Nightmode swiftly disables dangerous permissions for roles, like stripping `ADMINISTRATION` rights, "
            "while preserving original settings for seamless restoration.\n\n"
            "**Make sure to keep my ROLE above all roles you want to protect.**\n\n"
            "**Available Commands:**\n"
            f"<a:Arrowright:1376605813820489820> `{ctx.prefix}nightmode enable` - Enable nightmode\n"
            f"<a:Arrowright:1376605813820489820> `{ctx.prefix}nightmode disable` - Disable nightmode"
        )
        
        if ctx.bot.user.avatar:
            container.add_item(ui.Section(ui.TextDisplay(main_info), accessory=ui.Thumbnail(ctx.bot.user.avatar.url)))
        else:
            container.add_item(ui.TextDisplay(main_info))
        
        container.add_item(ui.Separator())
        container.add_item(ui.TextDisplay(f"**Requested by:** {ctx.author.mention}"))
        view.add_item(container)
        await ctx .send (view=view)

    @nightmode .command (name ="enable",help ="Enable nightmode")
    @commands .has_permissions (administrator =True )
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,10 ,commands .BucketType .user )
    async def enable_nightmode (self ,ctx ):
        if ctx .guild .member_count <50 :
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("# <:icon_cross:1372375094336425986> Access Denied"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay('Your Server Doesn\'t Meet My 50 Member Criteria'))
            view.add_item(container)
            return await ctx .send (view=view)

        own =ctx .author .id ==ctx .guild .owner_id 
        check =await self .is_extra_owner (ctx .author ,ctx .guild )
        if not own and not check :
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("# <:icon_cross:1372375094336425986> Access Denied"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay('Only Server Owner Or Extraowner Can Run This Command!'))
            view.add_item(container)
            return await ctx .send (view=view)

        if not own and not (
        ctx .guild .me .top_role .position <=ctx .author .top_role .position 
        ):
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("# <:icon_danger:1373170993236803688> Access Denied"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay('Only Server Owner or Extraowner Having **Higher role than me can run this command**'))
            view.add_item(container)
            return await ctx .send (view=view)

        bot_highest_role =ctx .guild .me .top_role 
        manageable_roles =[
        role for role in ctx .guild .roles 
        if role .position <bot_highest_role .position 
        and role .name !='@everyone'
        and role .permissions .administrator 
        and not role .managed 
        ]

        if not manageable_roles :
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("# No Admin Roles Found"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay('No Roles Found With Admin Permissions'))
            view.add_item(container)
            return await ctx .send (view=view)

        db_conn = await self.db.ensure_connection()
        async with db_conn.execute('SELECT guildId FROM Nightmode WHERE guildId = ?',(str (ctx .guild .id ),))as cursor :
            if await cursor .fetchone ():
                view = ui.LayoutView()
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay("# Already Enabled"))
                container.add_item(ui.Separator())
                container.add_item(ui.TextDisplay('Nightmode is already enabled.'))
                view.add_item(container)
                return await ctx .send (view=view)

        async with db_conn.cursor ()as cursor :
            for role in manageable_roles :
                admin_permissions =discord .Permissions (administrator =True )
                if role .permissions .administrator :
                    permissions =role .permissions 
                    permissions .administrator =False 

                    await role .edit (permissions =permissions ,reason ='Nightmode ENABLED')

                    await cursor .execute ('''
                    INSERT OR REPLACE INTO Nightmode (guildId, roleId, adminPermissions)
                    VALUES (?, ?, ?)
                    ''',(str (ctx .guild .id ),str (role .id ),int (admin_permissions .value )))
            await db_conn.commit ()

        view = ui.LayoutView()
        container = ui.Container(accent_color=None)
        container.add_item(ui.TextDisplay("# <:icon_tick:1372375089668161597> Success"))
        container.add_item(ui.Separator())
        
        success_info = (
            f"Nightmode enabled! Dangerous Permissions Disabled For **{len(manageable_roles)}** Manageable Roles.\n\n"
            "**Protected Roles:**\n" + 
            "\n".join([f"<:enable_yes:1372375008441143417> {role.mention}" for role in manageable_roles[:5]]) +
            (f"\n...and {len(manageable_roles) - 5} more" if len(manageable_roles) > 5 else "")
        )
        
        container.add_item(ui.TextDisplay(success_info))
        container.add_item(ui.Separator())
        container.add_item(ui.TextDisplay(f"**Executor:** {ctx.author.mention}"))
        view.add_item(container)
        await ctx .send (view=view)

    @nightmode .command (name ="disable",help ="Disable nightmode")
    @commands .has_permissions (administrator =True )
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,10 ,commands .BucketType .user )
    async def disable_nightmode (self ,ctx ):
        if ctx .guild .member_count <50 :
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("# <:icon_danger:1373170993236803688> Access Denied"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay('Your Server Doesn\'t Meet My 50 Member Criteria'))
            view.add_item(container)
            return await ctx .send (view=view)

        own =ctx .author .id ==ctx .guild .owner_id 
        check =await self .is_extra_owner (ctx .author ,ctx .guild )
        if not own and not check :
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("# <:icon_danger:1373170993236803688> Access Denied"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay('Only Server Owner Or Extraowner Can Run This Command!'))
            view.add_item(container)
            return await ctx .send (view=view)

        if not own and not (
        ctx .guild .me .top_role .position <=ctx .author .top_role .position 
        ):
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("# <:icon_danger:1373170993236803688> Access Denied"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay('Only Server Owner or Extraowner Having **Higher role than me can run this command**'))
            view.add_item(container)
            return await ctx .send (view=view)

        db_conn = await self.db.ensure_connection()
        async with db_conn.execute ('SELECT roleId, adminPermissions FROM Nightmode WHERE guildId = ?',(str (ctx .guild .id ),))as cursor :
            stored_roles =await cursor .fetchall ()

        if not stored_roles :
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("# Not Enabled"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay('Nightmode is not enabled.'))
            view.add_item(container)
            return await ctx .send (view=view)

        restored_roles = []
        async with db_conn.cursor ()as cursor :
            for role_id ,admin_permissions in stored_roles :
                role =ctx .guild .get_role (int (role_id ))
                if role :
                    permissions =discord .Permissions (administrator =bool (admin_permissions ))
                    await role .edit (permissions =permissions ,reason ='Nightmode DISABLED')
                    restored_roles.append(role)

                    await cursor .execute ('DELETE FROM Nightmode WHERE guildId = ? AND roleId = ?',(str (ctx .guild .id ),role_id ))
            await db_conn.commit ()

        view = ui.LayoutView()
        container = ui.Container(accent_color=None)
        container.add_item(ui.TextDisplay("# <:icon_tick:1372375089668161597> Success"))
        container.add_item(ui.Separator())
        
        success_info = (
            f"Nightmode disabled! Restored Permissions For **{len(restored_roles)}** Manageable Roles.\n\n"
            "**Restored Roles:**\n" + 
            "\n".join([f"<:enable_yes:1372375008441143417> {role.mention}" for role in restored_roles[:5]]) +
            (f"\n...and {len(restored_roles) - 5} more" if len(restored_roles) > 5 else "")
        )
        
        container.add_item(ui.TextDisplay(success_info))
        container.add_item(ui.Separator())
        container.add_item(ui.TextDisplay(f"**Executor:** {ctx.author.mention}"))
        view.add_item(container)
        await ctx .send (view=view)


"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
