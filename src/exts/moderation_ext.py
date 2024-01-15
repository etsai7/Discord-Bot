import interactions
from interactions import Extension, slash_command, SlashContext, OptionType, slash_option, AutocompleteContext, Member, \
    Role, Task, DateTrigger, Guild, Client
import src.credentials as credentials
from datetime import datetime, timedelta


class ModerationExtension(Extension):
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

    @slash_command(name="mod",
                   scopes=[credentials.discord_guild_id],
                   default_member_permissions=interactions.Permissions.ADMINISTRATOR,
                   sub_cmd_name='mod_info',
                   sub_cmd_description='Command to auto suggest a bunch of hypixel item choices')
    async def mod_extension(self, ctx: SlashContext):
        cmds = (
            '`mod_info` - List of all the functions under the mods group\n`ban` - Ban players for a period of time')
        await ctx.send(cmds)

    @mod_extension.subcommand(sub_cmd_name='ban',
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
    async def ban(self, ctx: SlashContext, user: OptionType.USER, time: str):
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

    @ban.autocomplete('time')
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

    '''
        All Below are the components of the ban function. 
        1st is to switch roles of the user
        2nd is to trigger a task - no arguments can be passed in
    '''

    # Bot must have the right intent and permissions. Higher permissions than member that is chosen
    @mod_extension.subcommand(sub_cmd_name='switch_roles',
                              sub_cmd_description='Change the role of the user',
                              )
    @slash_option(name='user',
                  description='The user to be banned',
                  opt_type=OptionType.USER,
                  required=True)
    @slash_option(name='role',
                  description='Role to switch to',
                  opt_type=OptionType.ROLE,
                  required=True)
    async def switch_role(self, ctx: SlashContext, user: Member, role: Role):
        try:
            print(f'Current Roles: {user.roles}')
            await user.remove_roles(roles=user.roles, reason='Removing all roles for new role')
            await user.add_role(role)
            print(f'New Rules: {user.roles}')
            await ctx.send('Role Switched!')
        except:
            await ctx.send('Something went wrong! Role failed to switch')

    @mod_extension.subcommand(sub_cmd_name='start_timer',
                              sub_cmd_description='Start a Timer',
                              )
    @slash_option(name='time',
                  description='Duration to be banned',
                  opt_type=OptionType.STRING,
                  required=True,
                  autocomplete=True)
    async def trigger_delay(self, ctx: SlashContext, time: str):
        seconds = {
            '15s': 15,
            '1m': 60,
            '1d': 86400
        }
        current_datetime = datetime.now()
        new_datetime = current_datetime + timedelta(seconds=seconds.get(time, 0))
        task = Task(self.start_timer, DateTrigger(new_datetime))
        task.start()
        await ctx.send(f'Timer started at {current_datetime}. Timer Expiring at {new_datetime}')

    @trigger_delay.autocomplete('time')
    async def autocomplete(self, ctx: AutocompleteContext):
        user_input = ctx.input_text
        durations = ['15s', '1m', '1d']

        filtered_choices = [entry for entry in durations if entry.startswith(user_input)][:25]

        await ctx.send(choices=filtered_choices)

    async def start_timer(self):
        channel = await self.client.fetch_channel(credentials.channel_id_testing)
        await channel.send('Timer Expired!')
