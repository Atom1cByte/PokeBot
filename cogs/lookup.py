import discord
import requests
import difflib
from discord.ui import View
from discord.commands import Option
from discord.ext import commands

class NotFoundView(View):
    def __init__(self, pokemon):
        self.pokemon = pokemon

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="✅")
    async def yes_btn_callback(self, button, interaction: discord.Interaction):
        await poke_interaction(self.pokemon, interaction)
        
    @discord.ui.button(label="No", style=discord.ButtonStyle.green, emoji="✅")
    async def no_btn_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message("> Aww. Sorry I couldn't find your pokémon. To be honest it most likely doesn't exist")

async def poke_interaction(pokemon, inter: discord.Interaction):
    pass

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
            ctx.response.send_message(f"> Selected pokémon not found. Did you mean {rl_pokemon}?", view=NotFoundView(rl_pokemon))
        else:
            await poke_interaction(pokemon, ctx)


def setup(client):
    client.add_cog(Lookup(client))