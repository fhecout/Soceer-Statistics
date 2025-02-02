import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Define headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}

# Esquema de cores profissional
COLORS = {
    'primary': '#1e3d59',      # Azul escuro profundo
    'secondary': '#ff6e40',    # Laranja vibrante
    'accent': '#17c3b2',       # Verde água
    'background': '#f5f9ff',   # Azul muito claro
    'text_dark': '#2b2d42',    # Quase preto
    'text_light': '#ffffff',   # Branco
    'success': '#06d6a0',      # Verde suave
    'warning': '#ffd93d',      # Amarelo suave
    'error': '#ef476f',        # Vermelho suave
    'gray': '#e9ecef'          # Cinza claro
}

# Função para carregar os códigos dos times do arquivo .txt
def carregar_codigos_times():
    team_codes = {}
    try:
        with open('team_codes.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if "Time:" in line and "Código:" in line:
                    parts = line.strip().split(", ")
                    team_name = parts[0].replace("Time: ", "")
                    team_code = parts[1].replace("Código: ", "")
                    # Armazena o nome original como chave e também uma versão em lowercase
                    team_codes[team_name] = team_code
                    team_codes[team_name.lower()] = team_code
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo 'team_codes.txt' não encontrado.")
    return team_codes

# Função para extrair dados de uma tabela do FBref
def extract_table_data(url, table_id):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': table_id})
        if table:
            data = []
            for row in table.find_all('tr')[1:]:
                cells = row.find_all(['th', 'td'])
                if len(cells) > 0:
                    data.append([cell.text.strip() for cell in cells])
            return data
    return []

# Função para buscar dados do time
def buscar_dados_time():
    time = entry_time.get().strip()
    if not time:
        messagebox.showerror("Erro", "Por favor, insira o nome de um time.")
        return

    # Carregar os códigos dos times
    team_codes = carregar_codigos_times()
    if not team_codes:
        return

    # Verificar se o time existe no dicionário (agora case-insensitive)
    time_lower = time.lower()
    if time_lower not in team_codes:
        messagebox.showerror("Erro", f"Time '{time}' não encontrado no arquivo de códigos.")
        return

    # Obter o código do time
    team_code = team_codes[time_lower]

    # URLs das páginas de estatísticas
    url_misc = f'https://fbref.com/pt/equipes/{team_code}/2024-2025/partidas/all_comps/misc/{time}-Historicos-dos-Jogos-Todos-os-campeonatos'
    url_shooting = f'https://fbref.com/pt/equipes/{team_code}/2024-2025/partidas/all_comps/shooting/{time}-Historicos-dos-Jogos-Todos-os-campeonatos'
    url_corner = f'https://fbref.com/pt/equipes/{team_code}/2024-2025/partidas/all_comps/defense/{time}-Historicos-dos-Jogos-Todos-os-campeonatos'

    # Extraindo dados das tabelas
    misc_data = extract_table_data(url_misc, 'matchlogs_for')
    shooting_data = extract_table_data(url_shooting, 'matchlogs_for')
    corner_data = extract_table_data(url_corner, 'matchlogs_for')

    if not misc_data or not shooting_data or not corner_data:
        messagebox.showerror("Erro", f"Não foi possível encontrar dados para o time {time}.")
        return

    # Processando os dados e combinando
    match_data = []
    total_goals = 0
    total_fouls = 0
    total_yellow_cards = 0
    total_red_cards = 0
    total_corners = 0
    total_matches = 0
    total_shots = 0
    total_shots_on_target = 0
    total_fouls_drawn = 0
    total_offsides = 0

    for i in range(len(misc_data)):
        if len(misc_data[i]) >= 16 and len(shooting_data[i]) >= 10:
            data = misc_data[i][0]
            competition = misc_data[i][2]
            local = misc_data[i][5]
            result = misc_data[i][6]
            goals_time = misc_data[i][7]
            gols_contra = misc_data[i][8]
            opponent = misc_data[i][9]
            yellow_cards = misc_data[i][10]
            red_cards = misc_data[i][11]
            offsides = misc_data[i][15]
            fouls_committed = misc_data[i][13]
            fouls_drawn = misc_data[i][14]

            # Dados de chutes
            total_shots_match = shooting_data[i][11]
            shots_on_target_match = shooting_data[i][12]

            # Dados de escanteios - agora na coluna correta
            corners = corner_data[i][6] if len(corner_data[i]) > 6 else '0'

            # Conversão segura para números
            try:
                goals_time = int(goals_time) if str(goals_time).isdigit() else 0
                yellow_cards = int(yellow_cards) if yellow_cards.isdigit() else 0
                red_cards = int(red_cards) if red_cards.isdigit() else 0
                fouls_committed = int(fouls_committed) if fouls_committed.isdigit() else 0
                fouls_drawn = int(fouls_drawn) if fouls_drawn.isdigit() else 0
                corners = int(corners) if corners.isdigit() else 0
                total_shots_match = int(total_shots_match) if total_shots_match.isdigit() else 0
                shots_on_target_match = int(shots_on_target_match) if shots_on_target_match.isdigit() else 0
                offsides = int(offsides) if offsides.isdigit() else 0
            except (ValueError, TypeError):
                continue

            # Resultado do jogo
            if result == "V":
                result_text = "Vitória"
            elif result == "D":
                result_text = "Derrota"
            elif result == "E":
                result_text = "Empate"
            else:
                continue

            # Acumulando totais para médias
            total_goals += goals_time
            total_fouls += fouls_committed
            total_fouls_drawn += fouls_drawn
            total_yellow_cards += yellow_cards
            total_red_cards += red_cards
            total_corners += corners
            total_shots += total_shots_match
            total_shots_on_target += shots_on_target_match
            total_offsides += offsides
            total_matches += 1

            match_data.append({
                "Data": data,
                "Resultado": result_text,
                "Campeonato": competition,
                "Local": local,
                "Time": time,
                "Placar": f"{goals_time} x {gols_contra}",
                "Oponente": opponent,
                "Cartões Amarelos": yellow_cards,
                "Cartões Vermelhos": red_cards,
                "Impedimentos": offsides,
                "Faltas Cometidas": fouls_committed,
                "Faltas Sofridas": fouls_drawn,
                "Total de Chutes": total_shots_match,
                "Chutes a Gol": shots_on_target_match,
                "% de Chutes a Gol": round((shots_on_target_match / total_shots_match * 100), 2) if total_shots_match > 0 else 0,
                "Escanteios": corners
            })

    # Calculando médias
    if total_matches > 0:
        avg_goals = round(total_goals / total_matches, 2)
        avg_fouls = round(total_fouls / total_matches, 2)
        avg_fouls_drawn = round(total_fouls_drawn / total_matches, 2)
        avg_yellow_cards = round(total_yellow_cards / total_matches, 2)
        avg_red_cards = round(total_red_cards / total_matches, 2)
        avg_corners = round(total_corners / total_matches, 2)
        avg_shots = round(total_shots / total_matches, 2)
        avg_shots_on_target = round(total_shots_on_target / total_matches, 2)
        avg_shots_percentage = round((total_shots_on_target / total_shots * 100), 2) if total_shots > 0 else 0
        avg_offsides = round(total_offsides / total_matches, 2)
    else:
        avg_goals = avg_fouls = avg_fouls_drawn = avg_yellow_cards = avg_red_cards = avg_corners = avg_shots = avg_shots_on_target = avg_shots_percentage = avg_offsides = 0

    # Adicionando linha com médias
    match_data.append({
        "Data": "MÉDIA POR JOGO",
        "Resultado": "-",
        "Campeonato": "-",
        "Local": "-",
        "Time": time,
        "Placar": f"{avg_goals:.2f}",
        "Oponente": "-",
        "Cartões Amarelos": avg_yellow_cards,
        "Cartões Vermelhos": avg_red_cards,
        "Impedimentos": avg_offsides,
        "Faltas Cometidas": avg_fouls,
        "Faltas Sofridas": avg_fouls_drawn,
        "Total de Chutes": avg_shots,
        "Chutes a Gol": avg_shots_on_target,
        "% de Chutes a Gol": avg_shots_percentage,
        "Escanteios": avg_corners
    })

    # Criando DataFrame com os dados processados
    match_df = pd.DataFrame(match_data)
    root.match_df = match_df

    atualizar_grid(tree_matches, match_df, match_columns)

    # URL da página de estatísticas dos jogadores
    url_players = f'https://fbref.com/pt/equipes/{team_code}/{time}-Estatisticas'
    response_players = requests.get(url_players, headers=headers)

    players_data = []
    if response_players.status_code == 200:
        soup_players = BeautifulSoup(response_players.content, 'html.parser')
        
        # Encontrando o div principal de estatísticas
        stats_div = soup_players.find('div', {'id': 'all_stats_standard'})

        total_matches = 0
        total_goals = 0
        total_assists = 0
        total_yellow_cards = 0
        total_red_cards = 0
        
        if stats_div:
            table_players = stats_div.find('table', {'class': 'stats_table'})
            
            if table_players:
                for row in table_players.find_all('tr')[1:]:
                    cells = row.find_all(['th', 'td'])
                    
                    if len(cells) >= 15:
                        name = cells[0].text.strip()
                        
                        # Pular linhas de totais ou vazias
                        if "Total" in name or name == "" or name == "Jogador":
                            continue
                        
                        # Extraindo as estatísticas básicas
                        matches_played = cells[4].text.strip()  # MP (Matches Played)
                        goals = cells[8].text.strip()  # Gols
                        assists = cells[9].text.strip()  # Assistências
                        yellow_cards = cells[14].text.strip()  # Cartões Amarelos
                        red_cards = cells[15].text.strip()  # Cartões Vermelhos

                        # Convertendo para números
                        matches_played = int(matches_played) if matches_played.isdigit() else 0
                        goals = int(goals) if goals.isdigit() else 0
                        assists = int(assists) if assists.isdigit() else 0
                        yellow_cards = int(yellow_cards) if yellow_cards.isdigit() else 0
                        red_cards = int(red_cards) if red_cards.isdigit() else 0

                        # Atualizando totais
                        total_matches += matches_played
                        total_goals += goals
                        total_assists += assists
                        total_yellow_cards += yellow_cards
                        total_red_cards += red_cards

                        players_data.append({
                            "Jogador": name,
                            "Jogos": matches_played,
                            "Gols": goals,
                            "Assistências": assists,
                            "Cartões Amarelos": yellow_cards,
                            "Cartões Vermelhos": red_cards,
                            "Média de Gols por Jogo": round(goals / matches_played, 2) if matches_played > 0 else 0,
                            "Média de Assistências por Jogo": round(assists / matches_played, 2) if matches_played > 0 else 0
                        })

                # Adicionando linha de médias do time
                if players_data:
                    players_data.append({
                        "Jogador": "Média do Time",
                        "Jogos": round(total_matches / len(players_data), 2),
                        "Gols": round(total_goals / len(players_data), 2),
                        "Assistências": round(total_assists / len(players_data), 2),
                        "Cartões Amarelos": round(total_yellow_cards / len(players_data), 2),
                        "Cartões Vermelhos": round(total_red_cards / len(players_data), 2),
                        "Média de Gols por Jogo": round(total_goals / total_matches, 2) if total_matches > 0 else 0,
                        "Média de Assistências por Jogo": round(total_assists / total_matches, 2) if total_matches > 0 else 0
                    })

    # Criando DataFrame para os jogadores e atualizando o grid
    players_df = pd.DataFrame(players_data)
    root.players_df = players_df
    atualizar_grid(tree_players, players_df, player_columns)

def atualizar_grid(tree, df, columns):
    for item in tree.get_children():
        tree.delete(item)

    # Ordenar o DataFrame pela data em ordem decrescente se a coluna 'Data' existir
    if 'Data' in df.columns:
        df = df.sort_values(by='Data', ascending=False)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# Interface gráfica
root = tk.Tk()
root.title(" Análise Estatística do Futebol")
root.geometry("1800x1000")  

# Configurando o tema e estilo
style = ttk.Style()
style.theme_use('clam')

# Configurando estilos personalizados com design mais moderno
style.configure('MainFrame.TFrame', background=COLORS['background'])
style.configure('Header.TFrame', background=COLORS['primary'])
style.configure('Content.TFrame', background=COLORS['background'])

# Estilos de texto
style.configure('Title.TLabel',
               font=('Segoe UI', 28, 'bold'),
               foreground=COLORS['text_light'],
               background=COLORS['primary'])

style.configure('Subtitle.TLabel',
               font=('Segoe UI', 14),
               foreground=COLORS['text_light'],
               background=COLORS['primary'])

style.configure('Search.TLabel',
               font=('Segoe UI', 12),
               foreground=COLORS['text_dark'],
               background=COLORS['background'])

# Estilo dos botões
style.configure('Primary.TButton',
               font=('Segoe UI', 11, 'bold'),
               background=COLORS['secondary'],
               foreground=COLORS['text_light'])

style.configure('Secondary.TButton',
               font=('Segoe UI', 11),
               background=COLORS['accent'],
               foreground=COLORS['text_light'])

# Estilo da Treeview mais moderna
style.configure('Custom.Treeview',
               font=('Segoe UI', 10),
               rowheight=35,
               background='white',
               fieldbackground='white',
               foreground=COLORS['text_dark'])

style.configure('Custom.Treeview.Heading',
               font=('Segoe UI', 11, 'bold'),
               background=COLORS['primary'],
               foreground=COLORS['text_light'],
               relief='flat')

style.map('Custom.Treeview',
          background=[('selected', COLORS['accent'])],
          foreground=[('selected', COLORS['text_light'])])

style.map('Custom.Treeview.Heading',
          background=[('active', COLORS['secondary'])])

# Configurando a cor de fundo principal
root.configure(bg=COLORS['primary'])

# Frame principal
main_frame = ttk.Frame(root, style='MainFrame.TFrame')
main_frame.pack(fill=tk.BOTH, expand=True)

# Header com design moderno
header_frame = ttk.Frame(main_frame, style='Header.TFrame')
header_frame.pack(fill=tk.X)

# Container para o conteúdo do header
header_content = ttk.Frame(header_frame, style='Header.TFrame')
header_content.pack(pady=20)

title_label = ttk.Label(header_content,
                       text=" Análise Estatística do Futebol",
                       style='Title.TLabel')
title_label.pack(anchor='center')

subtitle_label = ttk.Label(header_content,
                          text="Sistema Profissional de Análise de Desempenho",
                          style='Subtitle.TLabel')
subtitle_label.pack(anchor='center', pady=(5, 0))

# Container principal do conteúdo
content_frame = ttk.Frame(main_frame, style='Content.TFrame')
content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

# Barra de status moderna
status_frame = ttk.Frame(content_frame, style='Content.TFrame')
status_frame.pack(fill=tk.X, pady=(10, 0))

status_label = ttk.Label(status_frame,
                        text=" Sistema pronto para uso",
                        font=('Segoe UI', 10),
                        foreground=COLORS['primary'])
status_label.pack(side=tk.LEFT)

# Função para atualizar o status com ícones
def update_status(message, color=COLORS['primary']):
    icon = ""  # Padrão
    if color == COLORS['error']:
        icon = ""
    elif color == COLORS['success']:
        icon = ""
    elif color == COLORS['accent']:
        icon = ""
    status_label.configure(text=f"{icon} {message}", foreground=color)

# Função wrapper para busca com feedback visual
def buscar_dados_time_wrapper():
    update_status("Buscando dados...", COLORS['accent'])
    try:
        buscar_dados_time()
        update_status("Dados atualizados com sucesso!", COLORS['success'])
    except Exception as e:
        update_status(f"Erro: {str(e)}", COLORS['error'])

# Função de exportação com feedback visual
def exportar_excel():
    if hasattr(root, 'match_df') and hasattr(root, 'players_df'):
        try:
            filename = f"{entry_time.get()}_Stats.xlsx"
            with pd.ExcelWriter(filename, engine="openpyxl") as writer:
                root.match_df.to_excel(writer, sheet_name="Últimas 6 Partidas", index=False)
                root.players_df.to_excel(writer, sheet_name="Estatísticas dos Jogadores", index=False)
            update_status(f"Arquivo exportado com sucesso: {filename}", COLORS['success'])
        except Exception as e:
            update_status(f"Erro ao exportar: {str(e)}", COLORS['error'])
    else:
        update_status("Primeiro busque os dados de um time antes de exportar.", COLORS['warning'])

# Frame de pesquisa com visual elegante
search_frame = ttk.Frame(content_frame, style='Content.TFrame')
search_frame.pack(fill=tk.X, pady=(0, 20))

# Container de pesquisa centralizado com borda suave
search_container = ttk.Frame(search_frame, style='Content.TFrame')
search_container.pack(anchor='center')

# Label e entrada de pesquisa
label = ttk.Label(search_container,
                 text="Nome do Time:",
                 style='Search.TLabel')
label.pack(side=tk.LEFT, padx=5)

# Estilizando a entrada
entry_style = ttk.Style()
entry_style.configure('Custom.TEntry',
                     fieldbackground='white',
                     borderwidth=0)

entry_time = ttk.Entry(search_container,
                      width=40,
                      font=('Segoe UI', 12),
                      style='Custom.TEntry')
entry_time.pack(side=tk.LEFT, padx=15)

# Botões com ícones e estilos modernos
search_button = ttk.Button(search_container,
                          text=" Buscar Estatísticas",
                          style='Primary.TButton',
                          command=buscar_dados_time_wrapper)
search_button.pack(side=tk.LEFT, padx=5)

export_button = ttk.Button(search_container,
                          text=" Exportar Excel",
                          style='Secondary.TButton',
                          command=exportar_excel)
export_button.pack(side=tk.LEFT, padx=5)

# Notebook com design moderno
notebook_style = ttk.Style()
notebook_style.configure('Custom.TNotebook',
                        background=COLORS['background'])
notebook_style.configure('Custom.TNotebook.Tab',
                        font=('Segoe UI', 11),
                        padding=[15, 10],
                        background=COLORS['gray'])
notebook_style.map('Custom.TNotebook.Tab',
                  background=[('selected', COLORS['primary'])],
                  foreground=[('selected', COLORS['text_light'])])

notebook = ttk.Notebook(content_frame, style='Custom.TNotebook')
notebook.pack(fill=tk.BOTH, expand=True)

# Frame para partidas com padding e borda suave
matches_frame = ttk.Frame(notebook, style='Content.TFrame')
notebook.add(matches_frame, text=" Últimas Partidas")

# Colunas para as partidas
match_columns = [
    "Data", "Resultado", "Campeonato", "Local", "Time", "Placar", "Oponente",
    "Cartões Amarelos", "Cartões Vermelhos", "Impedimentos", "Faltas Cometidas",
    "Faltas Sofridas", "Total de Chutes", "Chutes a Gol", "% de Chutes a Gol", "Escanteios"
]

# Container para a tabela de partidas
matches_container = ttk.Frame(matches_frame, style='Content.TFrame')
matches_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Treeview com estilo personalizado
tree_matches = ttk.Treeview(matches_container,
                           columns=match_columns,
                           show="headings",
                           style='Custom.Treeview')

# Scrollbars estilizadas
scrollbar_matches_y = ttk.Scrollbar(matches_container,
                                  orient="vertical",
                                  command=tree_matches.yview)
scrollbar_matches_x = ttk.Scrollbar(matches_container,
                                  orient="horizontal",
                                  command=tree_matches.xview)

tree_matches.configure(yscrollcommand=scrollbar_matches_y.set,
                      xscrollcommand=scrollbar_matches_x.set)

# Configuração do grid com padding
tree_matches.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
scrollbar_matches_y.grid(row=0, column=1, sticky="ns")
scrollbar_matches_x.grid(row=1, column=0, sticky="ew")

matches_container.grid_rowconfigure(0, weight=1)
matches_container.grid_columnconfigure(0, weight=1)

# Configurando colunas com larguras otimizadas
for col in match_columns:
    tree_matches.heading(col, text=col)
    if col in ["Data", "Resultado", "Local", "Time", "Oponente"]:
        tree_matches.column(col, width=130, minwidth=130)
    else:
        tree_matches.column(col, width=110, minwidth=110)

# Frame para estatísticas dos jogadores
players_frame = ttk.Frame(notebook, style='Content.TFrame')
notebook.add(players_frame, text=" Estatísticas dos Jogadores")

# Colunas para os jogadores
player_columns = [
    "Jogador", "Jogos", "Gols", "Assistências",
    "Cartões Amarelos", "Cartões Vermelhos",
    "Média de Gols por Jogo", "Média de Assistências por Jogo"
]

# Container para a tabela de jogadores
players_container = ttk.Frame(players_frame, style='Content.TFrame')
players_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Treeview de jogadores com estilo personalizado
tree_players = ttk.Treeview(players_container,
                           columns=player_columns,
                           show="headings",
                           style='Custom.Treeview')

# Scrollbars para a tabela de jogadores
scrollbar_players_y = ttk.Scrollbar(players_container,
                                  orient="vertical",
                                  command=tree_players.yview)
scrollbar_players_x = ttk.Scrollbar(players_container,
                                  orient="horizontal",
                                  command=tree_players.xview)

tree_players.configure(yscrollcommand=scrollbar_players_y.set,
                      xscrollcommand=scrollbar_players_x.set)

# Configurando colunas dos jogadores
for col in player_columns:
    tree_players.heading(col, text=col)
    if col == "Jogador":
        tree_players.column(col, width=250, minwidth=250)
    elif col in ["Jogos", "Gols"]:
        tree_players.column(col, width=100, minwidth=100)
    else:
        tree_players.column(col, width=170, minwidth=170)

# Grid layout para a tabela de jogadores
tree_players.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
scrollbar_players_y.grid(row=0, column=1, sticky="ns")
scrollbar_players_x.grid(row=1, column=0, sticky="ew")

players_container.grid_rowconfigure(0, weight=1)
players_container.grid_columnconfigure(0, weight=1)

root.mainloop()