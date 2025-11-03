# PROJECT: Quinn - The cyber scout for ranks, streaks, and live match tracking in League of Legends
A Discord bot that shows player rank information, ranked winstreaks and loss streaks, and live match info 
## Features
- **Live game tracking** (`!live`)  
  See current match participants, champions, ranks, game mode, and in-game time in a discord embed  
- **Red Carpet** (`!redcarpet`)  
  Track a summoner’s ranked loss streak in solo queue, perfect for tracking rage queueing! 

- **Blue Carpet** (`!bluecarpet`)  
  Track a summoner’s ranked win streak in solo queue

- **Rank Lookup** (`!rank`)  
  Get a player’s current solo queue rank, division and LP

- **Tutorial Command** (`!tutorial`)  
  Shows how to use all commands

## Built With
- Python
- [discord.py](https://discordpy.readthedocs.io/)  
- [requests](https://requests.readthedocs.io/)  
- [Riot Games API](https://developer.riotgames.com/)

## Installation and Setup
1. Clone the Repository
      ```bash
   git clone https://github.com/YOUR_USERNAME/PROJECT-Quinn.git
   cd PROJECT-Quinn
2. Install discord.py, requests, and python-dotenv requirements
   ```bash
   pip install discord.py requests python-dotenv
3. Get a Discord Bot token and Invite bot  
   Go to the Discord Developer Portal
   Click “New Application” and give it a name  
   Go to “Bot” in the sidebar, then click “Add Bot”.  
   Under the Bot tab, click “Copy Token” — this is your DISCORD_BOT_TOKEN.  
4. Get a temporary development API key from Riot Games (Riot account is required)  
   [Riot Games API](https://developer.riotgames.com/)  
5. Set up API keys and discord bot token  
   Create a .env file in project folder
   Add your key like this:
   ```env
   DISCORD_BOT_TOKEN=your-discord-bot-token
   RIOT_API_KEY=your-riot-api-key
6. Invite Bot to your server using this link (Replace YOUR_CLIENT_ID with your bot's client id found under general information in developer portal)
   https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=3072  
7. Run the bot
   ```bash
   python PROJECT-Quinn.py

## Examples
1. **Check a summoner's ranked loss streak**  
   <img width="340" height="158" alt="image" src="https://github.com/user-attachments/assets/9ede5f23-e0f9-438e-8f32-f3f195389b66" />
2. **Check a summoner's ranked win streak**  
   <img width="384" height="154" alt="image" src="https://github.com/user-attachments/assets/c456dd95-c497-4893-935c-7657e8483fef" />
3. **Check a summoner's rank**  
   <img width="292" height="128" alt="image" src="https://github.com/user-attachments/assets/803c589d-42e8-484a-88f1-aac0f6572748" />
4. **Check a summoner's live game**  
   <img width="478" height="510" alt="image" src="https://github.com/user-attachments/assets/586d2159-3e11-4f99-ae51-262e7f913914" />



