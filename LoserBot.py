import discord
from discord.ext import tasks
from discord import Intents
from discord.ext import commands
import requests

# Configuration
TOKEN = 'xxx'
RIOT_API_KEY = 'xxx'
summoner_name = 'xxx'
tag_line = 'xxx'
REGION = 'xxx'
REGION2 = 'xxx'

# Bot setup
intents = Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='lose')
async def get_last_loss(ctx):
    # Get summoner ID
    summoner_url = f'https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    try:
        summoner_response = requests.get(summoner_url, headers={'X-Riot-Token': RIOT_API_KEY})
        summoner_response.raise_for_status()
        summoner_data = summoner_response.json()
    except Exception as e:
        print(f"Une erreur s'est produite lors de la requête vers l'API de Riot Games : {e}")
        return

    if 'puuid' in summoner_data:
        summoner_puuid = summoner_data['puuid']
    else:
        print("La clé 'puuid' n'existe pas dans le dictionnaire summoner_data.")
        return

    # Get match list
    matchlist_url = f'https://{REGION2}.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids'
    try:
        matchlist_response = requests.get(matchlist_url, headers={'X-Riot-Token': RIOT_API_KEY})
        matchlist_response.raise_for_status()
        match_ids = matchlist_response.json()
    except Exception as e:
        print(f"Une erreur s'est produite lors de la requête pour la liste des matchs : {e}")
        return

      # Look for the last defeat
    last_loss = None
    for match_id in match_ids:
        match_url = f'https://{REGION2}.api.riotgames.com/lol/match/v5/matches/{match_id}'
        try:
            match_response = requests.get(match_url, headers={'X-Riot-Token': RIOT_API_KEY})
            match_response.raise_for_status()
            match_data = match_response.json()
        except Exception as e:
            print(f"Une erreur s'est produite lors de la requête pour le match {match_id} : {e}")
            continue

        # Check if the player lost the match
        participant_id = None
        for participant in match_data['info']['participants']:
            if participant['puuid'] == summoner_puuid:
                participant_id = participant['participantId']
                break

        if participant_id is not None:
            participant_data = match_data['info']['participants'][participant_id - 1]
            if not participant_data['win']:
                last_loss = match_data
                break

    if last_loss:
        participant_id = None
        for participant in last_loss['info']['participants']:
            if participant['puuid'] == summoner_puuid:
                participant_id = participant['participantId']
                break

        if participant_id is not None:
            participant_data = last_loss['info']['participants'][participant_id - 1]
            opponent_name = participant_data['summonerName']
            game_duration = last_loss['info']['gameDuration'] / 60
            game_duration = round(game_duration, 2)
            kills = participant_data['kills']
            deaths = participant_data['deaths']
            assists = participant_data['assists']

            await ctx.send(f"Votre dernière défaite sur League of Legends :\nJoueur : {opponent_name}\nDurée du match : {game_duration} min\nKDA : {kills}/{deaths}/{assists}")
        else:
            await ctx.send('Impossible de trouver les statistiques du participant dans le dernier match.')
    else:
        await ctx.send('Aucune défaite récente trouvée.')

bot.run(TOKEN)