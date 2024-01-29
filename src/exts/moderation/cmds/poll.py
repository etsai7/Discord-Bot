from interactions import *
from src.exts.moderation.moderation_ext import ModerationExtension as ME


class Poll(Extension):
    @ME.mod_extension.subcommand(sub_cmd_name='poll',
                                 sub_cmd_description='Create a poll for others to react')
    @slash_option(name='question',
                  description='Your question to everyone',
                  opt_type=OptionType.STRING,
                  required=True)
    @slash_option(name='choices',
                  description='Choices separated by "|" for each <emoji>~<choice>. Custom emoji is '
                              'optional. 🔮~A|🎃~B|C. Limit 10',
                  opt_type=OptionType.STRING,
                  required=True)
    async def poll(self, ctx: SlashContext, question: str, choices: str):
        default_emojis = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:',
                          ':nine:', ':keycap_ten:']
        emojis_index = 0
        poll_choices = {}  # Key: Emoji, Value: Choice String

        # Map out the user input into a dictionary. Limiting it to 11 choices
        for choice in choices.split("|")[:11]:
            c = choice.split('~')
            # Handles if user doesn't provide an emoji
            if len(c) == 1:
                poll_choices[default_emojis[emojis_index]] = c[0]
                emojis_index += 1
            else:
                poll_choices[c[0].strip()] = c[1]

        # Build the printout of poll choices for the embed
        embed_choices = ''
        for emoji, val in poll_choices.items():
            embed_choices += f'{emoji} {val}\n'

        poll_embed = Embed(title=f'**{question}**',
                           description=embed_choices,
                           color=Color.from_rgb(98, 242, 175))
        message = await ctx.send(embeds=poll_embed)

        # After sending the msg, add a default react for each of the choices
        for emoji in poll_choices.keys():
            await message.add_reaction(emoji=f'{emoji}')


def setup(bot):
    Poll(bot)
