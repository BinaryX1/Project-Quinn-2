import discord
import sqlite3
from discord.ext import commands
from discord import Embed, Color
import requests
import database
import time

#Fix having to use quotations for names with spaces

from dotenv import load_dotenv
import os

load_dotenv()
bot_token = os.getenv("DISCORD_BOT_TOKEN")

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

champion_key_to_name = {}
def load_champion_data(): #Prepares champion database from data dragon for the live game command
    versions_url = f"https://ddragon.leagueoflegends.com/api/versions.json" #Getting correct version for data dragon
    versions = requests.get(versions_url).json()
    current_version = versions[0]

    champions_data_url = f"https://ddragon.leagueoflegends.com/cdn/{current_version}/data/en_US/champion.json" #Getting champion database from data dragon
    champions_data = requests.get(champions_data_url).json()

    for champion in champions_data["data"].values():
        champion_key_to_name[int(champion["key"])] = champion["id"]
    
    print(champion_key_to_name)

def return_player_rank(puuid):
    summoner_rank_data_url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    response4 = requests.get(summoner_rank_data_url, headers=headers)
    rank_data = response4.json()
    if not rank_data:
        return "Unranked"
    for entries in rank_data:
        if entries["queueType"]=="RANKED_SOLO_5x5":
            summoner_rank = entries["tier"]
            summoner_division = entries["rank"]
            summoner_LP = entries["leaguePoints"]
            rank = f"{summoner_rank} {summoner_division} {summoner_LP} LP"
            return rank
    return "Unranked"

@bot.event
async def on_ready():
    load_champion_data()

@bot.command()
async def screenshot(ctx):
    await ctx.send("Hello World")

headers = {"X-Riot-Token": os.getenv("RIOT_API_KEY")}

@bot.command()
async def redcarpet(ctx, summoner_name, tagLine):
    start_time = time.time()
    ranked_loss_counter = 0

    await ctx.send(f"Tracking red carpet for {summoner_name} {tagLine}...")
    puuid_data_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tagLine}"
    response1 = requests.get(puuid_data_url, headers=headers)
    print(response1)
    if response1.status_code == 401:
        await ctx.send(f"Tell flyquest to update the api key")
        return
    elif response1.status_code != 200:
        await ctx.send(f"Error, please try again later")
        return    
    account_data = response1.json()
    puuid = account_data.get('puuid')

    summoner_match_data_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response2 = requests.get(summoner_match_data_url, headers=headers)
    print(response2)
    match_history = response2.json()
    print(match_history)
    
    ranked_win_found = False
    for match in match_history:
        match_analysis_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}"
        response3 = requests.get(match_analysis_url, headers=headers)
        print(response3)
        match_analysis = response3.json()
        if match_analysis['info']['queueId']==420 and match_analysis['info']['gameDuration'] > 180:
            for player in match_analysis['info']['participants']:
                if player['puuid'] == puuid:
                    if player['win'] == False:
                        ranked_loss_counter += 1
                        ranked_win_found = False
                        break
                    else:
                        ranked_win_found = True
                        break
        if ranked_win_found:
            break
        else:
            continue     

    print("%s seconds"%(time.time()-start_time))
    await ctx.send(f"{summoner_name} has a {ranked_loss_counter} game red carpet")

@bot.command()
async def bluecarpet(ctx, summoner_name, tagLine):
    ranked_win_counter = 0

    await ctx.send(f"Tracking blue carpet for {summoner_name} {tagLine}...")
    puuid_data_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tagLine}"
    response1 = requests.get(puuid_data_url, headers=headers)
    print(response1)
    if response1.status_code == 401:
        await ctx.send(f"Tell flyquest to update the api key")
        return
    elif response1.status_code != 200:
        await ctx.send(f"Error, please try again later")
        return
    account_data = response1.json()
    puuid = account_data.get('puuid')

    summoner_match_data_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response2 = requests.get(summoner_match_data_url, headers=headers)
    print(response2)
    match_history = response2.json()
    print(match_history)
    
    ranked_loss_found = False
    for match in match_history:
        match_analysis_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}"
        response3 = requests.get(match_analysis_url, headers=headers)
        print(response3)
        match_analysis = response3.json()
        if match_analysis['info']['queueId']==420 and match_analysis['info']['gameDuration'] > 180:
            for player in match_analysis['info']['participants']:
                if player['puuid'] == puuid:
                    if player['win'] == True:
                        ranked_win_counter += 1
                        ranked_loss_found = False
                    else:
                        ranked_loss_found = True
                        break
        if ranked_loss_found:
            break
        else:
            continue               
    
    await ctx.send(f"{summoner_name} has a {ranked_win_counter} game blue carpet")
    
@bot.command()
async def rank(ctx, summoner_name, tagLine):
    puuid_data_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tagLine}"
    response1 = requests.get(puuid_data_url, headers=headers)
    print(response1)
    if response1.status_code == 401:
        await ctx.send(f"Tell flyquest to update the api key")
        return
    elif response1.status_code != 200:
        await ctx.send(f"Error, please try again later")
        return
    account_data = response1.json()
    puuid = account_data.get('puuid')
    summoner_rank_data_url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    response4 = requests.get(summoner_rank_data_url, headers=headers)
    rank_data = response4.json()
    if not rank_data:
        await ctx.send(f"{summoner_name} is unranked")
        return
    for entries in rank_data:
        if entries["queueType"]=="RANKED_SOLO_5x5":
            summoner_rank = entries["tier"]
            summoner_division = entries["rank"]
            summoner_LP = entries["leaguePoints"]
    await ctx.send(f"{summoner_name} is {summoner_rank} {summoner_division} {summoner_LP} LP")

@bot.command()
async def live(ctx, summoner_name, tagLine):
    live_embed = Embed(
        title = f"{summoner_name}'s Live Game Info",
        description = "Shows game participants, champions, gametime etc.",
        color = Color.red()
        )
    
    puuid_data_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tagLine}" #Find puuid of player
    response1 = requests.get(puuid_data_url, headers=headers)
    print(response1)
    if response1.status_code == 401:
        await ctx.send(f"Tell flyquest to update the api key")
        return    
    elif response1.status_code != 200:
        await ctx.send(f"Error, please try again later")
        return
    account_data = response1.json()
    puuid = account_data.get('puuid')
    print(puuid)

    live_game_data_url = f"https://na1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}"
    response2 = requests.get(live_game_data_url, headers=headers)
    print(response2)
    if response2.status_code == 404:
        await ctx.send(f"{summoner_name} is not in a match")
    live_game_data = response2.json()

    game_time_seconds= live_game_data["gameLength"]
    minutes = ((game_time_seconds)//60)
    seconds = game_time_seconds%60
    if seconds >= 10:
        Embed.add_field(live_embed, name="Game time", value=f"{minutes}:{seconds}", inline = False)
    elif seconds <= 10:
        Embed.add_field(live_embed, name="Game time", value=f"{minutes}:0{seconds}", inline = False)

    gamemode_ID = live_game_data["gameQueueConfigId"]
    if gamemode_ID == 420:
        gamemode = "Ranked Solo/Duo"
    elif gamemode_ID == 440:
        gamemode = "Ranked Flex"
    elif gamemode_ID == 400:
        gamemode = "Draft Pick"
    elif gamemode_ID == 430:
        gamemode = "Swiftplay"
    elif gamemode_ID == 450:
        gamemode = "ARAM"
    elif gamemode_ID == 900:
        gamemode = "ARURF"
    elif gamemode_ID == 1020:
        gamemode = "One For All"
    elif gamemode_ID == 1400:
        gamemode = "Ultimate Spellbook"
    else:
        gamemode = "Unknown"
    
    Embed.add_field(live_embed, name = "Gamemode", value=f"{gamemode}", inline = True)


    blue_team_players = ""
    red_team_players = ""
    
    participants = live_game_data["participants"]
    for player in participants:
        player_puuid = player["puuid"]
        player_name_data_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{player_puuid}"
        player_name = requests.get(player_name_data_url, headers=headers).json()["gameName"]
        player_tag = requests.get(player_name_data_url, headers=headers).json()["tagLine"]
        player_rank = return_player_rank(player_puuid)
        champion_key = player["championId"]
        champion = champion_key_to_name[champion_key]
        player_team = player["teamId"]
        if player_team == 100:
            blue_team_players+=f"{player_name} ({player_rank}) - {champion}\n"
        else:
            red_team_players+=f"{player_name} ({player_rank}) - {champion}\n"


    Embed.add_field(live_embed, name = "Blue team", value = blue_team_players, inline=False)
    Embed.add_field(live_embed, name = "Red team", value = red_team_players, inline=False)
            

    


    await ctx.send(embed=live_embed)


    

@bot.command()
async def tutorial(ctx):
    await ctx.send(
        'Use command !redcarpet then enter your summoner name then your tag to find your red carpet (ranked loss streak). ' \
        'For example: !redcarpet Binary 6790.\n' \
        'If your summoner name is more than one word please put it in quotation marks followed by your tag, for example: "rainbow dash" NA1' \
        'To find your blue carpet (ranked win streak) follow the same steps but use command !bluecarpet instead'
        'To find the rank of a user use command !rank followed by their summoner name and tag'
        'To find live game info use command !live followed by summoner name and tag'
        )        




        
bot.run(bot_token)