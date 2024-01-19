from interactions import *
from src.exts.moderation.moderation_ext import ModerationExtension
from datetime import datetime, timedelta
import src.credentials as credentials

'''
This action will switch the user to a muted role. Currently that is @ShadowBanned role.
Though, technically the method allows for switching to another role for a timed period
'''


class Mute(Extension):

    def __init__(self, bot):
        self.seconds: dict = None
        self.ban_tracker: dict = None
        self.roles: list = None
        self.banned_role: str = 'ShadowBanned'
        self.unbanned_role: str = 'Normal'

    async def async_start(self):
        self.ban_tracker = {}
        self.seconds = {
            '15s': 15,
            '1min': 60,
            '1d': 86400,
            '2d': 172800,
            '3d': 259200,
            '4d': 345600,
            '5d': 432000,
            '6d': 518400,
            '1w': 604800,
            '2w': 1209600,
            '3w': 1814400,
            '1m': 2419200,
            '2m': 4828400,
            '3m': 7257600
        }
        self.roles = (await self.client.fetch_guild(credentials.discord_guild_id)).roles

    @ModerationExtension.mod_extension.subcommand(sub_cmd_name='mute',
                                                  sub_cmd_description='Ban players for a period of time')
    @slash_option(name='user',
                  description='The user to be banned',
                  opt_type=OptionType.USER,
                  required=True)
    @slash_option(name='time',
                  description='Duration to be banned',
                  opt_type=OptionType.STRING,
                  required=True,
                  autocomplete=True)
    async def mute(self, ctx: SlashContext, user: OptionType.USER, time: str):
        usr: Member = user
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=self.seconds[time])
        self.ban_tracker[str(usr.id)] = {
            'user': usr,
            'start_time': start_time,
            'end_time': end_time
        }
        await self.remove_user_roles(user=usr)
        await self.add_user_role(user=usr, role_name=self.banned_role)

        Task(callback=self.unban, trigger=DateTrigger(end_time)).start()

        await ctx.send(f'User Id: {usr.id} with roles: {usr.roles}')

    @mute.autocomplete('time')
    async def autocomplete(self, ctx: AutocompleteContext):
        user_input = ctx.input_text
        durations = ['15s', '1m', '1d', '2d', '3d', '4d', '5d', '6d', '7d', '1w', '2w', '3w', '4w', '1m', '2m', '3m']

        filtered_choices = [entry for entry in durations if entry.startswith(user_input)][:25]

        await ctx.send(choices=filtered_choices)

    async def unban(self):
        current_time = datetime.now()
        for user_id, data in self.ban_tracker.items():
            if data['end_time'] < current_time:
                channel = await self.client.fetch_channel('1117168088148873318')
                user: Member = data['user']
                await self.remove_user_roles(user=user)
                await self.add_user_role(user=user, role_name=self.unbanned_role)
                del self.ban_tracker[user_id]
                print('Successfully unbanned!')

    async def remove_user_roles(self, user: Member):
        current_roles = user.roles
        await user.remove_roles(roles=current_roles)

    async def add_user_role(self, user: Member, role_name: str):
        new_role = next((r for r in self.roles if r.name == role_name), None)
        await user.add_role(role=new_role)


def setup(bot):
    Mute(bot)