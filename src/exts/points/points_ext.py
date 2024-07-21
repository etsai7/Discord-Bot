import interactions
from interactions import *
import src.credentials as credentials


def get_cmd_information():
    return \
        '''### `points_info` - Gets command info under moderation
### `point_summary` - User summary of points
- `user` - User to select for points
'''


class PointsExtension(Extension):

    @slash_command(name="points",
                   scopes=[credentials.discord_guild_id, credentials.discord_nonsense_guild_id],
                   default_member_permissions=interactions.Permissions.ADMINISTRATOR,
                   sub_cmd_name='points_info',
                   sub_cmd_description='Commands regarding earning and spending points')
    async def point_extension(self, ctx: SlashContext):
        info_embed = Embed(title='<a:bugcat_keyboard_smash:1201337364195311616> **Mod Commands Info** '
                                 '<a:bugcat_keyboard_smash:1201337364195311616>',
                           description=get_cmd_information(),
                           color=Color.from_rgb(52, 157, 219))
        await ctx.send(embeds=info_embed)

