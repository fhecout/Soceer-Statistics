import requests
from bs4 import BeautifulSoup

# URLs das páginas das ligas mais famosas
leagues = {
    'Premier League': 'https://fbref.com/pt/comps/9/Premier-League-Estatisticas',
    'La Liga': 'https://fbref.com/pt/comps/12/La-Liga-Estatisticas',
    'Bundesliga': 'https://fbref.com/pt/comps/20/Bundesliga-Estatisticas',
    'Serie A': 'https://fbref.com/pt/comps/11/Serie-A-Estatisticas',
    'Ligue 1': 'https://fbref.com/pt/comps/13/Ligue-1-Estatisticas',
    'Primeira Liga': 'https://fbref.com/pt/comps/32/Primeira-Liga-Estatisticas',
    'Eredivisie': 'https://fbref.com/pt/comps/23/Eredivisie-Estatisticas',
    'Brasileirão': 'https://fbref.com/pt/comps/24/Serie-A-Estatisticas',
    'MLS': 'https://fbref.com/pt/comps/22/Major-League-Soccer-Estatisticas',
    'Argentine Primera División': 'https://fbref.com/pt/comps/21/Primera-Division-Estatisticas'
}

# Dicionário para armazenar os códigos dos times
team_codes = {}

for league, url in leagues.items():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrando todos os links que contêm os códigos dos times
        team_links = soup.find_all('a', href=True)
        
        for link in team_links:
            href = link['href']
            if '/equipes/' in href:
                parts = href.split('/')
                if len(parts) > 3:
                    team_code = parts[3]
                    team_name = link.text.strip()
                    
                    # Filtrando times femininos
                    if "Feminino" not in team_name and "(F)" not in team_name:
                        if team_name not in team_codes:
                            team_codes[team_name] = team_code
    else:
        print(f"Erro ao acessar a página da liga: {league}")

# Salvando os códigos dos times em um arquivo .txt
with open('team_codes.txt', 'w', encoding='utf-8') as file:
    for team, code in team_codes.items():
        file.write(f"Time: {team}, Código: {code}\n")

print("Códigos dos times foram armazenados no arquivo 'team_codes.txt'.")