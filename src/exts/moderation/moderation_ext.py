import interactions
from interactions import Extension, slash_command, SlashContext, OptionType, slash_option, AutocompleteContext, Member, \
    Role, Task, DateTrigger, Guild, Client, User, Timestamp
import src.credentials as credentials
from datetime import datetime, timedelta


class ModerationExtension(Extension):

    @slash_command(name="moderation",
                   scopes=[credentials.discord_guild_id],
                   default_member_permissions=interactions.Permissions.ADMINISTRATOR,
                   sub_cmd_name='mod_info',
                   sub_cmd_description='Command to auto suggest a bunch of hypixel item choices')
    async def mod_extension(self, ctx: SlashContext):
        cmds = (
            '`mod_info` - List of all the functions under the mods group\n`ban` - Ban players for a period of time')
        await ctx.send(cmds)

    '''
        All Below are the components of the ban function. 
        1st is to switch roles of the user
        2nd is to trigger a task - no arguments can be passed in
    '''

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
