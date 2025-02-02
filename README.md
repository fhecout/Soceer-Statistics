# Estatísticas de Times de Futebol

Um aplicativo desktop que permite visualizar estatísticas detalhadas de times de futebol, incluindo dados de partidas e jogadores.

## Funcionalidades

- **Busca por Time**: Digite o nome do time para ver suas estatísticas
- **Estatísticas de Partidas**: 
  - Data e resultado dos jogos
  - Gols marcados e sofridos
  - Cartões amarelos e vermelhos
  - Impedimentos
  - Estatísticas de chutes
- **Estatísticas de Jogadores**:
  - Número de jogos
  - Gols marcados
  - Assistências
  - Cartões amarelos e vermelhos
  - Médias por jogo
- **Exportação para Excel**: Possibilidade de exportar os dados para um arquivo Excel

## Como Usar

1. Execute o arquivo `scraper.exe`
2. Digite o nome do time que deseja pesquisar na caixa de texto
3. Clique no botão "Buscar"
4. Os dados serão exibidos em duas abas:
   - Aba "Partidas": Mostra o histórico de jogos do time
   - Aba "Jogadores": Mostra as estatísticas individuais dos jogadores
5. Para exportar os dados, clique no botão "Exportar Excel"

## Notas Importantes

- Os dados são obtidos em tempo real do site FBref
- As estatísticas são atualizadas automaticamente a cada busca
- O arquivo de times e códigos está integrado ao executável
- As datas mais recentes são mostradas primeiro na lista de partidas

## Requisitos

- Sistema Operacional Windows
- Não é necessário ter Python instalado
- Conexão com a internet para buscar os dados

## Problemas Comuns

Se você encontrar algum dos seguintes problemas:

1. **Time não encontrado**: Verifique se o nome do time está escrito corretamente
2. **Erro de conexão**: Verifique sua conexão com a internet
3. **Dados não aparecem**: Tente realizar a busca novamente

## Desenvolvimento

Este aplicativo foi desenvolvido em Python usando as seguintes bibliotecas:
- tkinter para a interface gráfica
- pandas para manipulação de dados
- requests e BeautifulSoup4 para web scraping
- openpyxl para exportação Excel
