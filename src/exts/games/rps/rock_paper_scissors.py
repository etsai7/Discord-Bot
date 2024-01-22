from interactions import *
from src.exts.games.games_ext import Games
from interactions.api.events import Component
import random


class RockPaperScissors(Extension):
    choices = ['rock', 'paper', 'scissor']
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSOR = 'scissor'

    def __init__(self, bot):
        self.games = {}

    @Games.game_info.subcommand(sub_cmd_name='rps',
                                sub_cmd_description='Play Rock ⛰ Paper 📃 Scissors ✂! ')
    async def rps(self, ctx: SlashContext):

        user_id = ctx.user.id
        user_name = ctx.user.display_name

        if user_id in self.games:
            embed = self.games[user_id].get("embed")
            choices = self.games[user_id].get("buttons")
            await ctx.send(embeds=embed, components=choices)
        else:

            embed = Embed(title="Let's Play Rock Paper Scissors!",
                          description='Rock, Paper, or Scissors?',
                          color=Color.from_rgb(255, 102, 255),
                          timestamp=Timestamp.now())
            choices = [Button(
                style=ButtonStyle.GREEN,
                emoji='🗿',
                custom_id=f'rock'
            ), Button(
                style=ButtonStyle.GREEN,
                emoji='📃',
                custom_id=f'paper',
            ), Button(
                style=ButtonStyle.GREEN,
                emoji='✂',
                custom_id=f'scissor',
            )]
            await ctx.send(embeds=embed, components=choices)

            self.games[user_id] = {"ctx": ctx,
                                   "buttons": choices,
                                   "username": user_name,
                                   "user_score": 0,
                                   "bot_score": 0,
                                   "tie": 0}

    @listen(Component)
    async def my_callback(self, event: Component):
        ctx = event.ctx
        user_id = ctx.user.id
        user_choice = ctx.custom_id
        user_score = self.games.get(user_id, {}).get("user_score", 0)
        bot_score = self.games.get(user_id, {}).get("bot_score", 0)
        tie = self.games.get(user_id, {}).get("tie", 0)

        bot_choice = random.choice(self.choices)
        # print(f'Event Button Id: {ctx.custom_id}')

        if bot_choice == user_choice:
            tie += 1
            self.games.get(user_id, {})["tie"] = tie
            await ctx.send(f"Looks like we both chose {bot_choice}. Its a tie!")
        elif (bot_choice == self.ROCK and user_choice == self.PAPER) or (
                bot_choice == self.PAPER and user_choice == self.SCISSOR) or (
                bot_choice == self.SCISSOR and user_choice == self.ROCK):
            user_score += 1
            self.games.get(user_id, {})["user_score"] = user_score
            await ctx.send(f"I chose {bot_choice}, you chose {user_choice}. You won!")
        else:
            bot_score += 1
            self.games.get(user_id, {})["bot_score"] = bot_score
            await ctx.send(f"I chose {bot_choice}, you chose {user_choice}. You lost!")

    @Games.game_info.subcommand(sub_cmd_name='scores',
                                sub_cmd_description='Print the scores')
    async def print_scores(self, ctx: SlashContext):
        embed = Embed(title="**ScoreBoard** 💯",
                      color=Color.from_rgb(201, 234, 252),
                      footer=EmbedFooter(text='- PartyBot™'),
                      timestamp=Timestamp.now())
        for user, info in self.games.items():
            embed.add_field(info.get("username"),
                            f"Won: {info.get('user_score')} Lost: {info.get('bot_score')} Tied: {info.get('tie')}")

        await ctx.send(embeds=embed)


def setup(bot):
    RockPaperScissors(bot)
