from interactions import *
from src.exts.moderation.moderation_ext import ModerationExtension


class SwitchRoles(Extension):

    # Bot must have the right intent and permissions. Higher permissions than member that is chosen
    @ModerationExtension.mod_extension.subcommand(sub_cmd_name='switch_roles',
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


def setup(bot):
    SwitchRoles(bot)
