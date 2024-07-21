from interactions import *
import src.exts.points.points.points_utils as points_utils
from interactions.api.events import MessageCreate
from src.exts.points.points_ext import PointsExtension


class Earn(Extension):
    def __init__(self, bot):
        self.hello = "Hi"

    @PointsExtension.point_extension.subcommand(sub_cmd_name='total',
                                                sub_cmd_description='Retrieve total amount of points for the given user')
    @slash_option(name='user',
                  description='User points',
                  opt_type=OptionType.USER,
                  required=False)
    async def get_available_points(self, ctx: SlashContext, user: User = None):
        points = points_utils.retrieve_user_points(self.bot.conn, self.bot.db, ctx.author.display_name if user is None else user.display_name)
        await ctx.send(content=f'{points} total')

    @listen(MessageCreate)
    async def handle_msg(self, ctx: MessageCreate):
        points_utils.add_points(self.bot.conn, self.bot.db, ctx)

def setup(bot):
    Earn(bot)
