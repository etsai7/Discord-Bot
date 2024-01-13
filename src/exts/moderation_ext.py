from interactions import Extension, slash_command, SlashContext, OptionType, slash_option, AutocompleteContext, Member, Guild
import src.credentials as credentials


class ModerationExtension(Extension):
    @slash_command(name="mod",
                   scopes=[credentials.discord_guild_id],
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
        await ctx.send(f'User Id: {usr.id}')


    @ban.autocomplete('time')
    async def autocomplete(self, ctx: AutocompleteContext):
        user_input = ctx.input_text
        durations = ['1d', '2d', '3d', '4d', '5d', '6d', '7d', '1w', '2w', '3w', '4w', '1m', '2m', '3m']

        filtered_choices = [entry for entry in durations if entry.startswith(user_input)][:25]

        await ctx.send(choices=filtered_choices)
