from interactions import *
from src.exts.testing.test_ext import TestExtension
from datetime import datetime, timedelta


class CountDown(Extension):
    @TestExtension.testExtension.subcommand(sub_cmd_name='countdown',
                                            sub_cmd_description='A timer for counting down to given timestamp using '
                                                                'Discord format:'
                                                                '<t:1705967891:R> ')
    @slash_option(name='minutes',
                  description='Minutes for countdown',
                  choices=[SlashCommandChoice(name='1', value=1),
                           SlashCommandChoice(name='2', value=2),
                           SlashCommandChoice(name='3', value=3),
                           SlashCommandChoice(name='4', value=4),
                           SlashCommandChoice(name='5', value=5),
                           SlashCommandChoice(name='6', value=6),
                           SlashCommandChoice(name='7', value=7),
                           SlashCommandChoice(name='8', value=8),
                           SlashCommandChoice(name='9', value=9),
                           SlashCommandChoice(name='10', value=10)],
                  opt_type=OptionType.INTEGER,
                  required=False)
    async def testCountdown(self, ctx: SlashContext, minutes: int = 5):
        future = datetime.now() + timedelta(minutes=minutes)
        unix_time = int(datetime.timestamp(future))
        await ctx.send(f"<t:{unix_time}:R>")


def setup(bot):
    CountDown(bot)
