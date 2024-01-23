from interactions import Extension, slash_command, SlashContext, Button, ButtonStyle, ActionRow, component_callback, \
    ComponentContext
import src.credentials as credentials
import interactions.models.discord.components as cmp


class Buttons(Extension):

    @slash_command(name='buttons',
                   scopes=[credentials.discord_guild_id],
                   sub_cmd_name='button_info',
                   sub_cmd_description='Command to provide info on what this extension cmds are')
    async def buttonExtension(self, ctx: SlashContext):
        cmds = (
            '`button_info` - List of all the functions under the buttons group\n`button_simple` - Testing default '
            'button\n`button_many` 0 Testing many many buttons and layouts')
        await ctx.send(cmds)

    @buttonExtension.subcommand(sub_cmd_name='button_simple',
                                sub_cmd_description='Command to create a simple button')
    async def buttonSimple(self, ctx: SlashContext):
        components = [Button(
            style=ButtonStyle.GREEN,
            label="Click Me",
            emoji='🧪',
            custom_id="1"
        ), Button(
            style=ButtonStyle.RED,
            label="Click Me 2",
            emoji='🍙',
            custom_id="2"
        )]
        await ctx.send(components=components)

    @buttonExtension.subcommand(sub_cmd_name='button_many',
                                sub_cmd_description='Testing many many buttons and layouts')
    async def buttonMany(self, ctx: SlashContext):
        components: list[ActionRow] = cmp.spread_to_rows(Button(
            style=ButtonStyle.GREEN,
            label="Science",
            emoji='🧪',
            custom_id="1"
        ), Button(
            style=ButtonStyle.RED,
            label="Food",
            emoji='🍙',
            custom_id="2"
        ), Button(
            style=ButtonStyle.BLUE,
            label="Sports",
            emoji='⚾',
            custom_id="3"
        ), Button(
            style=ButtonStyle.BLURPLE,
            label="Travel",
            emoji='🚄',
            custom_id="4"
        ), Button(
            style=ButtonStyle.SECONDARY,
            label="Music",
            emoji='🎵',
            custom_id="5"
        ), Button(
            style=ButtonStyle.DANGER,
            label="Games",
            emoji='🎮',
            custom_id="6"
        ), max_in_row=4)

        await ctx.send(components=components)

    @component_callback("1")
    async def my_callback(self, ctx: ComponentContext):
        await ctx.send("You clicked it!")
