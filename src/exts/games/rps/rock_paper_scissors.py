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
                                sub_cmd_description='Play Rock 🪨 Paper 📃 Scissors ✂! ')
    async def rps(self, ctx: SlashContext):
        await ctx.send(embeds=self.build_game_embed(),
                       components=self.build_buttons())

    def build_game_embed(self) -> Embed:
        embed = Embed(title="Let's Play Rock Paper Scissors!",
                      description='Rock, Paper, or Scissors?',
                      color=Color.from_rgb(255, 102, 255),
                      timestamp=Timestamp.now())
        return embed

    def build_buttons(self) -> list[Button]:
        return [Button(
            style=ButtonStyle.GREEN,
            emoji='🪨',
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

    def add_new_player(self, user_id: str, user_name: str):
        self.games[user_id] = {"username": user_name,
                               "net_score": 0,
                               "user_score": 0,
                               "bot_score": 0,
                               "tie": 0}

    @listen(Component)
    async def my_callback(self, event: Component):
        ctx = event.ctx
        user_id = str(ctx.user.id)
        user_choice = ctx.custom_id
        user_name = ctx.user.display_name

        if user_id not in self.games:
            self.add_new_player(user_id, user_name)

        user_score = self.games.get(user_id, {}).get("user_score", 0)
        bot_score = self.games.get(user_id, {}).get("bot_score", 0)
        tie = self.games.get(user_id, {}).get("tie", 0)

        bot_choice = random.choice(self.choices)

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

        self.games.get(user_id, {})["net_score"] = user_score - bot_score

    @Games.game_info.subcommand(sub_cmd_name='scores',
                                sub_cmd_description='Print the scores')
    async def print_scores(self, ctx: SlashContext):
        embed = Embed(title="💯 **ScoreBoard** 💯",
                      color=Color.from_rgb(201, 234, 252),
                      footer=EmbedFooter(text='- PartyBot™'),
                      timestamp=Timestamp.now())
        sorted_items = sorted(self.games.items(), key=lambda x: (x[1]['net_score'], x[1]['user_score']), reverse=True)
        top_10 = dict(sorted_items[:10])

        medals = ['🥇', '🥈', '🥉', '🏅']
        count = 0

        for user, info in top_10.items():
            player = ''
            if count < 3:
                player = f'{medals[count]} {info.get("username")}'
            else:
                player = f'{medals[-1]} {info.get("username")}'
            embed.add_field(player,
                            f"**Net: {info.get('net_score'):02d}** -> Won: {info.get('user_score')} Lost: {info.get('bot_score')} Tied: {info.get('tie')}")

            count += 1

        await ctx.send(embeds=embed)


def setup(bot):
    RockPaperScissors(bot)
