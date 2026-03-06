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

        prefix = getattr(self.ctx, 'prefix', '!')
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

    async def show_security_content(self, interaction: discord.Interaction):
        """Show the security category content"""
        try:
            self.container.clear_items()

            self.container.add_item(
                ui.TextDisplay("# Security Commands")
            )

            self.container.add_item(ui.Separator())

            commands_text = "`antinuke`, `antinuke enable`, `antinuke disable`, `whitelist`, `whitelist @user`, `unwhitelist`, `whitelisted`, `whitelist reset`, `extraowner`, `extraowner set`, `extraowner view`, `extraowner reset`, `nightmode`, `nightmode enable`, `nightmode disable`"
            self.container.add_item(
                ui.TextDisplay(commands_text)
            )

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
                    await interaction.response.send_message(
                        "An error occurred while loading security content.", ephemeral=True
                    )
                except:
                    pass

    async def show_ai_content(self, interaction: discord.Interaction):
        """Show the AI category content"""
        try:
            self.container.clear_items()

            self.container.add_item(
                ui.TextDisplay("# AI Commands")
            )

            self.container.add_item(ui.Separator())

            commands_text = "`ai activate`, `ai deactivate`, `ai conversation-clear`, `ai personality`, `ai conversation-stats`, `ai ask`, `ai database-clear`, `ai roleplay-enable`, `ai roleplay-disable`"
            self.container.add_item(
                ui.TextDisplay(commands_text)
            )

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
                    await interaction.response.send_message(
                        "An error occurred while loading AI content.", ephemeral=True
                    )
                except:
                    pass

    async def show_automod_content(self, interaction: discord.Interaction):
        """Show the automod category content"""
        try:
            self.container.clear_items()

            self.container.add_item(
                ui.TextDisplay("# Automod Commands")
            )

            self.container.add_item(ui.Separator())

            commands_text = "`automod`, `automod enable`, `automod disable`, `automod punishment`, `automod config`, `automod logging`, `automod ignore`, `automod ignore channel`, `automod ignore role`, `automod ignore show`, `automod ignore reset`, `automod unignore`, `automod unignore channel`, `automod unignore role`, `blacklistword`, `blacklistword add <word>`, `blacklistword remove <word>`, `blacklistword reset`, `blacklistword config`, `blacklistword bypass add <user/role>`, `blacklistword bypass remove <user/role>`, `blacklistword bypass show`"
            self.container.add_item(
                ui.TextDisplay(commands_text)
            )

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
                    await interaction.response.send_message(
                        "An error occurred while loading automod content.", ephemeral=True
                    )
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
            commands_text = "`botinfo`, `stats`, `invite`, `serverinfo`, `userinfo`, `roleinfo`, `boostcount`, `unbanall`, `joined-at`, `ping`, `github`, `vcinfo`, `channelinfo`, `badges`, `banner user`, `banner server`, `reminder start`, `reminder clear`, `permissions`, `timer`, `media`, `media setup`, `media remove`, `media config`, `media bypass`, `media bypass add`, `media bypass remove`, `media bypass show`"
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
            commands_text = "`level status`, `level channel`, `level message`, `level desc`, `level color`, `level thumbnail`, `level image`, `level clearimage`, `level xprange`, `level multiplier`, `level addreward`, `level removereward`, `level rewards`, `level setxp`, `level preview`, `level xpboost`, `level xpboost add`, `level xpboost remove`, `level xpboost list`, `level blacklist`, `level blacklist channel`, `level blacklist role`, `level unblacklist`, `level unblacklist channel`, `level unblacklist role`, `level stats`, `level leaderboard`, `level reset`, `level reset user`, `level reset all`, `level placeholders`, `level rank`"
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

    async def show_guildtag_content(self, interaction: discord.Interaction):
        """Show the guildtag category content"""
        try:
            self.container.clear_items()
            self.container.add_item(ui.TextDisplay("# GuildTag Commands"))
            self.container.add_item(ui.Separator())
            
            description = "**Manage Discord Guild Tags and reward users who adopt your server's tag!**\n\n**Main Commands:**"
            self.container.add_item(ui.TextDisplay(description))
            
            commands_text = (
                "`guildtag enable` - Enable the guild tag system\n"
                "`guildtag disable` - Disable the guild tag system\n"
                "`guildtag config` - Show current configuration\n"
                "`guildtag channel set <channel>` - Set welcome message channel\n"
                "`guildtag channel remove` - Remove welcome channel\n"
                "`guildtag role add <role>` - Add a reward role\n"
                "`guildtag role remove <role>` - Remove a reward role\n"
                "`guildtag role list` - List all reward roles\n"
                "`guildtag message <text>` - Set welcome message\n"
                "`guildtag test [user]` - Test guild tag detection\n"
                "`guildtag grant [user]` - Manually grant rewards\n"
                "`guildtag list` - List users with guild tag\n"
                "`guildtag check` - Check all members for tags"
            )
            self.container.add_item(ui.TextDisplay(commands_text))
            
            self.container.add_item(ui.Separator())
            
            aliases_text = "**Aliases:** `gt`"
            self.container.add_item(ui.TextDisplay(aliases_text))
            
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
            logger.error("HELP", f"Error in show_guildtag_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message("An error occurred while loading guildtag content.", ephemeral=True)
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

    

    def setup_category_content(self, category_name):
        """No category content - does nothing"""
        pass

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Check if the user can interact with this view"""
        return interaction.user == self.ctx.author

    async def on_timeout(self):
        """Handle timeout"""
        pass

    async def category_select_callback(self, interaction: discord.Interaction):
        """Handle category selection from dropdown."""
        try:
            if interaction.user != self.ctx.author:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "You must run this command to interact with it.", ephemeral=True
                    )
                return

            if not interaction.data or 'values' not in interaction.data:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "Invalid interaction data.", ephemeral=True
                    )
                return

            selected_category = interaction.data['values'][0]

            target_cog = None
            for cog_name, cog in self.bot.cogs.items():
                try:
                    if hasattr(cog, 'help_custom'):
                        _, label, _ = cog.help_custom()
                        if label == selected_category:
                            target_cog = cog
                            break
                except Exception:
                    continue

            if target_cog:
                await self.show_category_content(interaction, target_cog, selected_category)
            else:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        "Category not found.", ephemeral=True
                    )
        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Select menu interaction error: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message(
                        "An error occurred while processing your selection.", ephemeral=True
                    )
                except:
                    pass

    async def show_category_content(self, interaction: discord.Interaction, cog, category_name):
        """Show the content for a selected category."""
        try:
            emoji, label, description = cog.help_custom()

            commands = []
            if hasattr(cog, 'get_commands'):
                try:
                    commands = cog.get_commands()
                except Exception:
                    commands = []
            else:
                try:
                    commands = [cmd for cmd in cog.get_commands() if not cmd.hidden]
                except Exception:
                    commands = []

            self.container.clear()

            self.container.add_item(
                ui.TextDisplay(f"**{emoji} {label}**")
            )

            self.container.add_item(ui.Separator())

            if commands:
                commands_list = []
                for cmd in commands:
                    try:
                        if cmd.name.startswith('__') and cmd.name.endswith('__'):
                            continue

                        cmd_help = getattr(cmd, 'help', None) or getattr(cmd, 'description', None) or "No description available"

                        if hasattr(cmd, 'commands') and cmd.commands:
                            subcommands = [subcmd.name for subcmd in cmd.commands if not subcmd.name.startswith('__')]
                            if subcommands:
                                subcmd_text = ", ".join(subcommands[:5])  # Show first 5 subcommands
                                if len(cmd.commands) > 5:
                                    subcmd_text += f" (+{len(cmd.commands) - 5} more)"
                                commands_list.append(f"`{cmd.name}` - {subcmd_text}")
                            else:
                                commands_list.append(f"`{cmd.name}` - {cmd_help[:60]}...")
                        else:
                            if len(cmd_help) > 60:
                                cmd_help = cmd_help[:57] + "..."
                            commands_list.append(f"`{cmd.name}` - {cmd_help}")
                    except Exception:
                        continue

                commands_text = "\n".join(commands_list) if commands_list else "No commands available for this category."
            else:
                commands_text = "No commands available for this category."

            self.container.add_item(
                ui.TextDisplay(commands_text)
            )

            embed = discord.Embed(
                title="Help - Category Details",
                description="",
                color=0x000000
            )

            if not interaction.response.is_done():
                await interaction.response.edit_message(embed=embed, view=self)
            else:
                await interaction.edit_original_response(embed=embed, view=self)

        except discord.NotFound:
            pass
        except discord.InteractionResponded:
            pass
        except Exception as e:
            logger.error("HELP", f"Error in show_category_content: {e}")
            if not interaction.response.is_done():
                try:
                    await interaction.response.send_message(
                        "An error occurred while loading category content.", ephemeral=True
                    )
                except:
                    pass

class HelpCommand (commands .HelpCommand ):

  async def send_ignore_message (self ,ctx ,ignore_type :str ):

    if ignore_type =="channel":
      await ctx .reply (f"This channel is ignored.",mention_author =False )
    elif ignore_type =="command":
      await ctx .reply (f"{ctx.author.mention} This Command, Channel, or You have been ignored here.",delete_after =6 )
    elif ignore_type =="user":
      await ctx .reply (f"You are ignored.",mention_author =False )

  async def on_help_command_error (self ,ctx ,error ):
    if isinstance (error ,commands .CommandNotFound ):
      embed =discord .Embed (
      color =0x000000 ,
      description =f"No command or category named `{ctx.invoked_with}` found."
      )
      embed .set_author (name ="Command Not Found",icon_url =ctx .bot .user .avatar .url )
      embed .set_footer (text =f"Use {ctx.prefix}help to see all commands")
      await ctx .reply (embed =embed ,delete_after =10 )
    else :

      await ctx .reply ("An error occurred while processing the help command.",delete_after =10 )

  def command_not_found (self ,string :str )->str :
    return f"No command called `{string}` found."

  def create_Yuna_mapping (self ,mapping ):
    """Create a filtered mapping that only includes cogs from cogs/Yuna directories"""
    Yuna_mapping ={}


    allowed_cog_classes ={

    '_general','_voice','_welcome','ticket','__sticky','__boost',
    '_automod','_antinuke','_music','_extra','_fun','_moderation','_giveaway',

    '_leveling','_ai','_server','RoleplayHelp','VerificationHelp',
    '_tracking','_logging','_counting','_Backup','_crew','_ignore'
    }

    for cog ,commands in mapping .items ():
      if cog and hasattr (cog ,'__class__'):
        cog_class_name =cog .__class__ .__name__ 

        if cog_class_name in allowed_cog_classes and hasattr (cog ,'help_custom'):
          Yuna_mapping [cog ]=commands 

    return Yuna_mapping 

  async def send_bot_help (self ,mapping ):
    ctx =self .context 
    check_ignore =await ignore_check ().predicate (ctx )
    check_blacklist =await blacklist_check ().predicate (ctx )

    if not check_blacklist :
      return 

    if not check_ignore :
      await self .send_ignore_message (ctx ,"command")
      return 

    from utils.Tools import getConfig
    server_data = await getConfig(ctx.guild.id) if ctx.guild else {}
    server_prefix = server_data.get('prefix', getattr(ctx, 'prefix', '!'))

    view = HelpLayout(self, ctx, server_prefix)
    await ctx.send(view=view)

  async def send_command_help (self ,command ):
    ctx =self .context 
    check_ignore =await ignore_check ().predicate (ctx )
    check_blacklist =await blacklist_check ().predicate (ctx )

    if not check_blacklist :
      return 

    if not check_ignore :
      self .send_ignore_message (ctx ,"command")
      return 

    view = ui.LayoutView()
    container = ui.Container(accent_color=None)
    
    container.add_item(ui.TextDisplay(f"**{command.qualified_name.title()}**"))
    
    description = command.help or command.description or "No description available"
    container.add_item(ui.TextDisplay(f"```xml\n<[] = optional | ‹› = required\nDon't type these while using Commands>```\n>>> {description}"))
    
    if command.aliases:
      aliases_text = ", ".join(command.aliases)
      container.add_item(ui.TextDisplay(f"**Aliases:** {aliases_text}"))
    
    usage_args = command.signature if command.signature else ""
    container.add_item(ui.TextDisplay(f"**Usage:** {command.qualified_name} {usage_args}"))
    
    view.add_item(container)
    await self .context .reply (view=view ,mention_author =False )

  def get_command_signature (self ,command ):
    parent =command .full_parent_name 
    if len (command .aliases )>0 :
      aliases =' | '.join (command .aliases )
      fmt =f'[{command.name} | {aliases}]'
      if parent :
        fmt =f'{parent}'
      alias =f'[{command.name} | {aliases}]'
    else :
      alias =command .name if not parent else f'{parent} {command.name}'
    return f'{alias} {command.signature}'

  def common_command_formatting (self ,embed_like ,command ):
    embed_like .title =self .get_command_signature (command )
    if command .description :
      embed_like .description =f'{command.description}\n\n{command.help}'
    else :
      embed_like .description =command .help or 'No help found...'

  async def send_group_help (self ,group ):
    ctx =self .context 
    check_ignore =await ignore_check ().predicate (ctx )
    check_blacklist =await blacklist_check ().predicate (ctx )

    if not check_blacklist :
      return 

    if not check_ignore :
      await self .send_ignore_message (ctx ,"command")
      return 

    commands_list =[f"➜ **{self.context.prefix}{cmd.qualified_name}**" for cmd in group .commands ]
    
    if not commands_list :
      return 
    
    items_per_page =10 
    total_pages =(len (commands_list )+items_per_page -1 )//items_per_page 
    current_page =1 
    
    async def create_page_view (page :int ):
      start_index =(page -1 )*items_per_page 
      end_index =min (start_index +items_per_page ,len (commands_list ))
      page_commands =commands_list [start_index :end_index ]
      
      layout_view =ui .LayoutView (timeout =300.0 )
      container =ui .Container (accent_color =None )
      
      container .add_item (ui .TextDisplay (f"# **{group.qualified_name.title()} Commands [{len(commands_list)}]**"))
      container .add_item (ui .Separator ())
      
      commands_text ="\n".join (page_commands )
      container .add_item (ui .TextDisplay (commands_text ))
      
      if total_pages >1 :
        container .add_item (ui .Separator ())
        container .add_item (ui .TextDisplay (f"**Page {page} of {total_pages}**"))
        
        button_row =ui .ActionRow (
          ui .Button (
            label ="",
            emoji ="<:SageDoubleArrowLeft:1479361925195239584>",
            custom_id ="help_first",
            style =discord .ButtonStyle .secondary ,
            disabled =(page ==1 )
          ),
          ui .Button (
            label ="",
            emoji ="<:arrow_left:1479361931880955934>",
            custom_id ="help_back",
            style =discord .ButtonStyle .secondary ,
            disabled =(page ==1 )
          ),
          ui .Button (
            label ="",
            emoji ="<:arrow_right:1479361937614835744>",
            custom_id ="help_next",
            style =discord .ButtonStyle .secondary ,
            disabled =(page ==total_pages )
          ),
          ui .Button (
            label ="",
            emoji ="<:SageDoubleArrowRight:1479361942425567293>",
            custom_id ="help_last",
            style =discord .ButtonStyle .secondary ,
            disabled =(page ==total_pages )
          )
        )
        container .add_item (button_row )
      
      layout_view .add_item (container )
      return layout_view 
    
    initial_view =await create_page_view (current_page )
    msg =await ctx .reply (view =initial_view ,mention_author =False )
    
    if total_pages >1 :
      def check (interaction :discord .Interaction ):
        return (interaction .user .id ==ctx .author .id and 
                interaction .message and 
                interaction .message .id ==msg .id )
      
      while True :
        try :
          interaction =await self .context .bot .wait_for ('interaction',timeout =300.0 ,check =check )
          await interaction .response .defer ()
          
          custom_id =interaction .data .get ('custom_id')
          
          if custom_id =='help_first':
            current_page =1 
          elif custom_id =='help_back':
            if current_page >1 :
              current_page -=1 
          elif custom_id =='help_next':
            if current_page <total_pages :
              current_page +=1 
          elif custom_id =='help_last':
            current_page =total_pages 
          
          updated_view =await create_page_view (current_page )
          await interaction .edit_original_response (view =updated_view )
        
        except :
          try :
            expired_view =ui .LayoutView ()
            expired_container =ui .Container (accent_color =None )
            expired_container .add_item (ui .TextDisplay ("# Container Expired\nPlease use the command again"))
            expired_view .add_item (expired_container )
            await msg .edit (view =expired_view )
          except :
            pass 
          break

  async def send_cog_help (self ,cog ):
    ctx =self .context 
    check_ignore =await ignore_check ().predicate (ctx )
    check_blacklist =await blacklist_check ().predicate (ctx )

    if not check_blacklist :
      return 

    if not check_ignore :
      await self .send_ignore_message (ctx ,"command")
      return 

    entries =[(
    f"➜ `{self.context.prefix}{cmd.qualified_name}`",
    f"{cmd.description or cmd.short_doc or 'No description provided...'}\n\u200b"
    )for cmd in cog .get_commands ()]
    paginator =Paginator (source =FieldPagePaginator (
    entries =entries ,
    title =f"{cog.qualified_name.title()} ({len(cog.get_commands())})",
    description ="< > Duty | [ ] Optional\n\n",
    color =color ,
    per_page =4 ),
    ctx =self .context )
    await paginator .paginate ()

class Help (Cog ,name ="help"):

  def __init__ (self ,client :Yuna ):
    self .bot =client 
    self ._original_help_command =client .help_command 
    attributes ={
    'name':"help",
    'aliases':['h'],
    'help':'Shows help about bot, a command or a category'
    }
    client .help_command =HelpCommand (command_attrs =attributes )
    client .help_command .cog =self 

  async def cog_unload (self ):
    self .help_command =self ._original_help_command 



"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""