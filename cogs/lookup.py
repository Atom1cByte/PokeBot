import difflib
import discord
import requests
from discord.commands import Option
from discord.ext import commands
from discord.ui import View

class FoundView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.select(
        min_values=1,
        placeholder="Chose what info you want to show",
        options=[
            discord.SelectOption(
                label="Color",
                emoji="🏳️‍🌈",
                description="Shows the color of the pokémon"
            ),
            discord.SelectOption(
                label="Evolution Chain",
                emoji="⛓️",
                description="Shows the evolution chain of the selected pokémon"
            ),
        ],
    )
    async def select_callback(self, select, interaction):
        pass

class NotFoundView(View):
    def __init__(self, pokemon):
        super().__init__()
        self.pokemon = pokemon

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="✅")
    async def yes_btn_callback(self, button, interaction: discord.Interaction):
        await poke_interaction(self.pokemon, interaction)
        
    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="❌")
    async def no_btn_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message("> Aww. Sorry I couldn't find your pokémon. To be honest it most likely doesn't exist")

async def poke_interaction(pokemon, inter: discord.Interaction):
    resp = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}")
    try:
        await inter.response.edit_message(content="....", view=View())
    except:
        await inter.followup.send("....", view=View())

class Lookup(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_poke_list(self):
        resp = requests.get("https://pokeapi.co/api/v2/pokemon?limit=10000&offset=0")
        data = resp.json()
        pokemon = [poke["name"] for poke in data["results"]]
        return pokemon

    @commands.slash_command(
        name="lookup",
        description="Look up whichever pokemon you want"
    )
    async def lookup(
        self,
        ctx: discord.ApplicationContext, 
        pokemon: Option(str, "Enter the pokemon you want to find (pikachu by default)", required=True, default="pikachu")
    ):
        resp = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}")
        if resp.status_code == 404:
            rl_pokemon = difflib.get_close_matches(pokemon, self.get_poke_list(), 1)[0]
            await ctx.response.send_message(f"> Selected pokémon not found. Did you mean {rl_pokemon}?", view=NotFoundView(rl_pokemon))
        else:
            await ctx.response.defer()
            await poke_interaction(pokemon, ctx)


def setup(client):
    client.add_cog(Lookup(client))
