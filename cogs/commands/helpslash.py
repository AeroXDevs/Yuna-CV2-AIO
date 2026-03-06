"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import discord 
from discord .ext import commands 
from discord import app_commands ,Interaction 
from difflib import get_close_matches 
from contextlib import suppress 
from core import Context 
from core .Yuna import Yuna 
from core .Cog import Cog 
from utils .Tools import getConfig 
from itertools import chain 
import json 
from utils import Paginator ,DescriptionEmbedPaginator ,FieldPagePaginator ,TextPaginator 
import asyncio 
from utils .config import serverLink, invite_link, website_link, support_link 
from utils .Tools import *
from discord import ui
from utils.logger import logger

color =0x000000 
client =Yuna ()

class HelpLayout(ui.LayoutView):
    def __init__(self, help_cog, ctx, server_prefix=None):
        super().__init__(timeout=300.0)
        self.help_cog = help_cog
        self.ctx = ctx
        self.current_page = "main"
        self.server_prefix = server_prefix or getattr(ctx, 'prefix', '!')

        self.total_commands = len(set(self.ctx.bot.walk_commands()))

        self.filtered_mapping = self.create_Yuna_mapping()

        self.container = ui.Container(accent_color=None)


        self.setup_main_content()

        self.add_item(self.container)

    def create_Yuna_mapping(self):
        """Create a filtered mapping that only includes cogs from cogs/Yuna directories"""
        main_menu_classes = {
            '_general', '_voice', '_welcome', 'ticket', '__sticky'
        }

        extra_menu_classes = {
            '_automod', '_antinuke', '_extra', '_fun', '_moderation', '_giveaway',
            '_leveling', '_ai', '_server', 'RoleplayHelp', 'VerificationHelp',
            '_tracking', '_logging', '_counting', '_Backup', '_crew', '_ignore'
        }

        all_allowed_classes = main_menu_classes | extra_menu_classes
        Yuna_mapping = {}

        for cog in self.ctx.bot.cogs.values():
            if cog and hasattr(cog, '__class__'):
                cog_class_name = cog.__class__.__name__
                if cog_class_name in all_allowed_classes and hasattr(cog, 'help_custom'):
                    Yuna_mapping[cog] = cog.get_commands()

        return Yuna_mapping

    def create_select_options(self, menu_type):
        """No select options - empty"""
        return []

    def setup_main_content(self):
        """Set up the main help content following stats.py pattern"""
        self.container.clear_items()

        prefix = getattr(self.ctx, 'prefix', '/')
        display_prefix = prefix
        if prefix.strip().startswith('<@'):
            display_prefix = f"@{self.ctx.me.display_name} "

        self.container.add_item(
            ui.TextDisplay("# Help Menu")
        )

        self.container.add_item(
            ui.TextDisplay(
                f"<:dot:1479361908766281812> **Type `{display_prefix}help` to get more info**\n"
                f"<:dot:1479361908766281812> **Total Commands available: `{self.total_commands}`**\n"
                f"<:dot:1479361908766281812> [Invite]({invite_link}) | [Website]({website_link}) | [Support]({support_link})"
            )
        )

        self.container.add_item(ui.Separator())

        new_content = (
            f"<a:ButterflyWhite:1479361913812025386> Hey [{self.ctx.author.display_name}]({self.ctx.author.avatar.url if self.ctx.author.avatar else 'https://discord.com'})!\n"
            f"I'm **Yuna**, your friendly companion.\n\n"
            f"   <:arrow:1479361920254345391> Prefix for this server: **{self.server_prefix}**\n"
            f"   <:arrow:1479361920254345391> Pick from the menu to continue!"
        )

        self.container.add_item(ui.TextDisplay(new_content))

        self.container.add_item(ui.Separator())
        
        self.main_categories_select = ui.ActionRow(
            ui.Select(
                placeholder="Main Categories",
                options=[
                    discord.SelectOption(
                        label="Home",
                        value="home"
                    ),
                    discord.SelectOption(
                        label="Welcomer",
                        value="welcomer"
                    ),
                    discord.SelectOption(
                        label="Security",
                        value="security"
                    ),
                    discord.SelectOption(
                        label="AI",
                        value="ai"
                    ),
                    discord.SelectOption(
                        label="Automod",
                        value="automod"
                    ),
                    discord.SelectOption(
                        label="Backup",
                        value="backup"
                    ),
                    discord.SelectOption(
                        label="Counting",
                        value="counting"
                    ),
                    discord.SelectOption(
                        label="Utility",
                        value="utility"
                    ),
                    discord.SelectOption(
                        label="Fun",
                        value="fun"
                    ),
                    discord.SelectOption(
                        label="Giveaway",
                        value="giveaway"
                    ),
                    discord.SelectOption(
                        label="Tickets",
                        value="tickets"
                    ),
                    discord.SelectOption(
                        label="Leveling",
                        value="leveling"
                    ),
                    discord.SelectOption(
                        label="Bot GuildProfile",
                        value="guildprofile"
                    ),
                    discord.SelectOption(
                        label="Crypto",
                        value="crypto"
                    )
                ]
            )
        )
        self.main_categories_select.children[0].callback = self.main_category_callback
        self.container.add_item(self.main_categories_select)
        
        self.extra_categories_select = ui.ActionRow(
            ui.Select(
                placeholder="Extra Categories",
                options=[
                    discord.SelectOption(
                        label="Home",
                        value="home"
                    ),
                    discord.SelectOption(
                        label="Voice",
                        value="voice"
                    ),
                    discord.SelectOption(
                        label="Ignore",
                        value="ignore"
                    ),
                    discord.SelectOption(
                        label="StickyNotes",
                        value="stickynotes"
                    ),
                    discord.SelectOption(
                        label="General",
                        value="general"
                    ),
                    discord.SelectOption(
                        label="Tracking",
                        value="tracking"
                    ),
                    discord.SelectOption(
                        label="Server",
                        value="server"
                    ),
                    discord.SelectOption(
                        label="Roleplay",
                        value="roleplay"
                    ),
                    discord.SelectOption(
                        label="Profile Pictures",
                        value="pfps"
                    ),
                    discord.SelectOption(
                        label="ToDo",
                        value="todo"
                    )
                ]
            )
        )
        self.extra_categories_select.children[0].callback = self.extra_category_callback
        self.container.add_item(self.extra_categories_select)

    async def select_callback(self, interaction: discord.Interaction):
        """No select menu - does nothing"""
        pass

    async def main_category_callback(self, interaction: discord.Interaction):
        """Handle main category selection (following stats.py pattern)"""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You cannot interact with this menu.", ephemeral=True)
            return

        choice = getattr(interaction, 'data', {}).get('values', ['home'])[0] if hasattr(interaction, 'data') and interaction.data else 'home'

        if choice == "home":
            self.setup_main_content()
            await interaction.response.edit_message(view=self)
        elif choice == "welcomer":
            await self.show_welcomer_content(interaction)
        elif choice == "security":
            await self.show_security_content(interaction)
        elif choice == "ai":
            await self.show_ai_content(interaction)
        elif choice == "automod":
            await self.show_automod_content(interaction)
        elif choice == "backup":
            await self.show_backup_content(interaction)
        elif choice == "counting":
            await self.show_counting_content(interaction)
        elif choice == "utility":
            await self.show_utility_content(interaction)
        elif choice == "fun":
            await self.show_fun_content(interaction)
        elif choice == "giveaway":
            await self.show_giveaway_content(interaction)
        elif choice == "tickets":
            await self.show_tickets_content(interaction)
        elif choice == "leveling":
            await self.show_leveling_content(interaction)
        elif choice == "guildprofile":
            await self.show_guildprofile_content(interaction)
        elif choice == "crypto":
            await self.show_crypto_content(interaction)
        else:
            await interaction.response.send_message("Category not found.", ephemeral=True)

    async def extra_category_callback(self, interaction: discord.Interaction):
        """Handle extra category selection"""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You cannot interact with this menu.", ephemeral=True)
            return

        choice = getattr(interaction, 'data', {}).get('values', ['home'])[0] if hasattr(interaction, 'data') and interaction.data else 'home'

        if choice == "home":
            self.setup_main_content()
            await interaction.response.edit_message(view=self)
        elif choice == "voice":
            await self.show_voice_content(interaction)
        elif choice == "ignore":
            await self.show_ignore_content(interaction)
        elif choice == "stickynotes":
            await self.show_stickynotes_content(interaction)
        elif choice == "general":
            await self.show_general_content(interaction)
        elif choice == "tracking":
            await self.show_tracking_content(interaction)
        elif choice == "server":
            await self.show_server_content(interaction)
        elif choice == "roleplay":
            await self.show_roleplay_content(interaction)
        elif choice == "pfps":
            await self.show_pfps_content(interaction)
        elif choice == "todo":
            await self.show_todo_content(interaction)
        else:
            await interaction.response.send_message("Category not found.", ephemeral=True)

    async def show_security_content(self, interaction: discord.Interaction):
        """Show the security category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Security Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`antinuke`, `antinuke enable`, `antinuke disable`, `whitelist`, `whitelist @user`, `unwhitelist`, `whitelisted`, `whitelist reset`, `extraowner`, `extraowner set`, `extraowner view`, `extraowner reset`, `nightmode`, `nightmode enable`, `nightmode disable`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_security_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading security content.", ephemeral=True)
                except:
                    pass

    async def show_ai_content(self, interaction: discord.Interaction):
        """Show the AI category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# AI Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`ai activate`, `ai deactivate`, `ai conversation-clear`, `ai personality`, `ai conversation-stats`, `ai ask`, `ai database-clear`, `ai roleplay-enable`, `ai roleplay-disable`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_ai_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading AI content.", ephemeral=True)
                except:
                    pass

    async def show_automod_content(self, interaction: discord.Interaction):
        """Show the automod category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Automod Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`automod`, `automod enable`, `automod disable`, `automod punishment`, `automod config`, `automod logging`, `automod ignore`, `automod ignore channel`, `automod ignore role`, `automod ignore show`, `automod ignore reset`, `automod unignore`, `automod unignore channel`, `automod unignore role`, `blacklistword`, `blacklistword add <word>`, `blacklistword remove <word>`, `blacklistword reset`, `blacklistword config`, `blacklistword bypass add <user/role>`, `blacklistword bypass remove <user/role>`, `blacklistword bypass show`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_automod_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading automod content.", ephemeral=True)
                except:
                    pass

    async def show_backup_content(self, interaction: discord.Interaction):
        """Show the backup category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Backup Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`backup`, `backup create`, `backup list`, `backup delete`, `backup info`, `backup transfer`, `backup preview`, `backup export`, `backup import`, `backup verify`, `backup stats`, `backup load`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_backup_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading backup content.", ephemeral=True)
                except:
                    pass

    async def show_counting_content(self, interaction: discord.Interaction):
        """Show the counting category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Counting Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`counting config`, `counting enable`, `counting disable`, `counting channel`, `counting reset`, `counting leaderboard`, `counting global`, `counting stats`, `counting achievements`, `counting info`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_counting_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading counting content.", ephemeral=True)
                except:
                    pass


    async def show_utility_content(self, interaction: discord.Interaction):
        """Show the utility category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Utility Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`serverinfo`, `userinfo`, `roleinfo`, `channelinfo`, `members`, `roles`, `emojis`, `stickers`, `invites`, `bans`, `permissions`, `whois`, `lookup`, `uptime`, `stats`, `ping`, `help`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_utility_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading utility content.", ephemeral=True)
                except:
                    pass

    async def show_fun_content(self, interaction: discord.Interaction):
        """Show the fun category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Fun Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`compliment`, `translate`, `howgay`, `lesbian`, `cute`, `intelligence`, `horny`, `gif`, `iplookup`, `weather`, `spank`, `8ball`, `truth`, `dare`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_fun_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading fun content.", ephemeral=True)
                except:
                    pass

    async def show_giveaway_content(self, interaction: discord.Interaction):
        """Show the giveaway category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Giveaway Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`gstart`, `gend`, `greroll`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_giveaway_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading giveaway content.", ephemeral=True)
                except:
                    pass

    async def show_tickets_content(self, interaction: discord.Interaction):
        """Show the tickets category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Tickets Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`ticket`, `ticket setup`, `ticket reset`, `ticket close`, `ticket transcript`, `ticket add`, `ticket remove`, `ticket rename`, `ticket category-add`, `ticket category-remove`, `ticket category-list`, `ticket category-default`, `ticket panel-send`, `ticket claim`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_tickets_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading tickets content.", ephemeral=True)
                except:
                    pass

    async def show_leveling_content(self, interaction: discord.Interaction):
        """Show the leveling category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Leveling Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`level`, `rank`, `leaderboard`, `setlevel`, `addxp`, `removexp`, `levelconfig`, `levelroles`, `levelroles add`, `levelroles remove`, `levelroles list`, `levelcard`, `levelrewards`, `levelmultiplier`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_leveling_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading leveling content.", ephemeral=True)
                except:
                    pass

    async def show_welcomer_content(self, interaction: discord.Interaction):
        """Show the welcomer category content"""
        try:
            self.container.clear_items()

            self.container.add_item(
                ui.TextDisplay("# Welcome Commands")
            )

            self.container.add_item(ui.Separator())

            commands_text = "`greet setup`, `greet reset`, `greet channel`, `greet edit`, `greet test`, `greet config`, `greet autodelete`, `greet`"
            self.container.add_item(
                ui.TextDisplay(commands_text)
            )

            self.container.add_item(ui.Separator())
            
            self.container.add_item(self.main_categories_select)
            
            self.container.add_item(self.extra_categories_select)

            if not interaction.response.is_done():

            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)

        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_welcomer_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message(
                        "An error occurred while loading welcomer content.", ephemeral=True
                    )
                except:
                    pass

    async def show_voice_content(self, interaction: discord.Interaction):
        """Show the voice category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Voice Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`voice`, `voice kick`, `voice kickall`, `voice mute`, `voice muteall`, `voice unmute`, `voice unmuteall`, `voice deafen`, `voice deafenall`, `voice undeafen`, `voice undeafenall`, `voice move`, `voice moveall`, `voice pull`, `voice pullall`, `voice lock`, `voice unlock`, `voice private`, `voice unprivate`, `vcrole add`, `vcrole remove`, `vcrole config`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_voice_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading voice content.", ephemeral=True)
                except:
                    pass

    async def show_ignore_content(self, interaction: discord.Interaction):
        """Show the ignore category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Ignore Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`ignore`, `ignore command add`, `ignore command remove`, `ignore command show`, `ignore channel add`, `ignore channel remove`, `ignore channel show`, `ignore user add`, `ignore user remove`, `ignore user show`, `ignore bypass add`, `ignore bypass show`, `ignore bypass remove`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_ignore_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading ignore content.", ephemeral=True)
                except:
                    pass

    async def show_stickynotes_content(self, interaction: discord.Interaction):
        """Show the stickynotes category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# StickyNotes Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`sticky setup`, `sticky remove`, `sticky list`, `sticky toggle`, `sticky edit`, `sticky config`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_stickynotes_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading stickynotes content.", ephemeral=True)
                except:
                    pass

    async def show_general_content(self, interaction: discord.Interaction):
        """Show the general category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# General Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`status`, `afk`, `avatar`, `banner`, `servericon`, `membercount`, `poll`, `hack`, `token`, `users`, `wizz`, `urban`, `rickroll`, `hash`, `snipe`, `editsnipe`, `list inrole`, `list emojis`, `list bots`, `list admins`, `list invoice`, `list mods`, `list early`, `list activedeveloper`, `list createpos`, `list roles`, `calc`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_general_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading general content.", ephemeral=True)
                except:
                    pass

    async def show_serververify_content(self, interaction: discord.Interaction):
        """Show the serververify category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Server Verification Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`verification setup`, `verification status`, `verification enable`, `verification disable`, `verification logs`, `verification reset`, `verification verify`, `verification fix`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_serververify_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading serververify content.", ephemeral=True)
                except:
                    pass

    async def show_tracking_content(self, interaction: discord.Interaction):
        """Show the tracking category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Tracking Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`tracking`, `tracking enable`, `tracking disable`, `tracking status`, `tracking setup`, `tracking wipe`, `tracking export`, `tracking import`, `tracking messages`, `tracking invites`, `tracking leaderboard`, `tracking messagelb`, `tracking dailylb`, `tracking invitelb`, `tracking addmessages`, `tracking resetmessages`, `tracking addinvites`, `tracking resetinvites`, `tracking setlogchannel`, `tracking myinvites`, `tracking resetall`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_tracking_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading tracking content.", ephemeral=True)
                except:
                    pass

    async def show_server_content(self, interaction: discord.Interaction):
        """Show the server category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Server Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`setup`, `setup create <name>`, `setup delete <name>`, `setup list`, `setup girl`, `setup friend`, `setup vip`, `setup guest`, `setup config`, `setup reset`, `girl`, `friend`, `vip`, `guest`, `autorole bots add`, `autorole bots remove`, `autorole bots`, `autorole config`, `autorole humans add`, `autorole humans remove`, `autorole humans`, `autorole reset all`, `autorole reset bots`, `autorole reset humans`, `autorole`, `autoresponder`, `autoresponder create`, `autoresponder delete`, `autoresponder edit`, `autoresponder config`, `react`, `react add`, `react remove`, `react list`, `react reset`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_server_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading server content.", ephemeral=True)
                except:
                    pass

    async def show_roleplay_content(self, interaction: discord.Interaction):
        """Show the roleplay category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Roleplay Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`hug`, `kiss`, `cuddle`, `pat`, `slap`, `tickle`, `poke`, `wave`, `dance`, `cry`, `laugh`, `smile`, `blush`, `wink`, `thumbsup`, `clap`, `bow`, `salute`, `facepalm`, `shrug`, `sleep`, `eat`, `drink`, `run`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_roleplay_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading roleplay content.", ephemeral=True)
                except:
                    pass

    async def show_guildprofile_content(self, interaction: discord.Interaction):
        """Show the bot guildprofile category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Bot GuildProfile Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`setguildbio`, `setguildavatar`, `setguildbanner`, `setguildname`, `setguildclear`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_guildprofile_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading guildprofile content.", ephemeral=True)
                except:
                    pass

    async def show_pfps_content(self, interaction: discord.Interaction):
        """Show the profile pictures category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Profile Pictures Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`pfp female`, `pfp male`, `pfp matching`, `pfp anime`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_pfps_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading pfps content.", ephemeral=True)
                except:
                    pass

    async def show_todo_content(self, interaction: discord.Interaction):
        """Show the todo category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# ToDo Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`todo list`, `todo clear`, `todo add`, `todo remove`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_todo_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading todo content.", ephemeral=True)
                except:
                    pass

    async def show_crypto_content(self, interaction: discord.Interaction):
        """Show the crypto category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# Crypto Commands"))
            self.container.add_item(ui.Separator())
            commands_text = "`crypto balance`, `crypto convert`, `crypto transaction`, `crypto news`, `crypto price`, `crypto gainers`, `crypto losers`"
            self.container.add_item(ui.TextDisplay(commands_text))
            self.container.add_item(ui.Separator())
            self.container.add_item(self.main_categories_select)
            self.container.add_item(self.extra_categories_select)
            if not interaction.response.is_done():
                await interaction.response.edit_message(view=self)
            else:
                await interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_crypto_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading crypto content.", ephemeral=True)
                except:
                    pass


class HelpSlash (Cog ,name ="helpslash"):
    def __init__ (self ,client :Yuna ):
        self .bot =client 

    @app_commands .command (name ="help",description ="Shows help about the bot and commands")
    async def help_slash (self ,interaction :Interaction ):
        """Slash command version of help - shows main help menu"""
        try :

            if interaction .guild :
                data =await getConfig (interaction .guild .id )
                prefix =data ["prefix"]
            else :
                prefix ="/"


            await interaction .response .defer ()

            class FakeContext :
                def __init__ (self ,interaction ):
                    self .author =interaction .user 
                    self .guild =interaction .guild 
                    self .bot =interaction .client 
                    self .prefix ="/"
                    self .interaction =interaction 

            fake_ctx =FakeContext (interaction )

            view = HelpLayout(help_cog=self, ctx=fake_ctx, server_prefix=prefix)

            await interaction .edit_original_response (view =view )

        except Exception as e :
            print (f"Error in slash help command: {e}")
            if not interaction .response .is_done ():
                await interaction .response .send_message (f"An error occurred: {str(e)}",ephemeral =True )
            else :
                await interaction .followup .send (f"An error occurred: {str(e)}",ephemeral =True )

async def setup (client ):
    await client .add_cog (HelpSlash (client ))

"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""