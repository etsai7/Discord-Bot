from interactions import *
from src.exts.moderation.moderation_ext import ModerationExtension
from src.exts.tasks.moderation_tasks import ModerationTasks
from datetime import datetime, timedelta


class Ban(Extension):
    @ModerationExtension.mod_extension.subcommand(sub_cmd_name='ban',
                                                  sub_cmd_description='Actually banning someone')
    @slash_option(name='user',
                  description='The user to be banned',
                  opt_type=OptionType.USER,
                  required=True)
    @slash_option(name='time',
                  description='Duration of ban',
                  opt_type=OptionType.INTEGER,
                  required=True)
    @slash_option(name='units',
                  description='Time Unit',
                  choices=[SlashCommandChoice(name='seconds', value=1),
                           SlashCommandChoice(name='minutes', value=60),
                           SlashCommandChoice(name='hours', value=3600),
                           SlashCommandChoice(name='days', value=86400)],
                  opt_type=OptionType.INTEGER,
                  required=True)
    async def ban_user(self, ctx: SlashContext, user: User, time: int, units: int):
        # await user.edit(communication_disabled_until=Timestamp(datetime.now()))
        await ctx.guild.ban(user=user, reason='testing')
        await ctx.send('Banned!!')

        current_datetime = datetime.now()
        try:
            new_datetime = current_datetime + timedelta(seconds=time*units)
        except:
            new_datetime = current_datetime + timedelta(seconds=86400)
            print("Duration too long, defaulting to 1 year")

        task = Task(ModerationTasks(self.bot, ctx, user).unban, DateTrigger(new_datetime))
        task.start()
        unix_time = int(datetime.timestamp(new_datetime))
        await ctx.send(f"<t:{unix_time}:R>")



def setup(bot):
    Ban(bot)
