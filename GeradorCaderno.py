import os
import weasyprint
from jinja2 import Environment, FileSystemLoader
import json
from pathlib import Path

# TO DO
# Remover as funções não usadas

class GeradorCaderno:
    def __init__(self, json) -> None:
        self.RAIZ = Path(__file__).resolve().parent

        self.LOCAL_ASSETS = os.path.join(self.RAIZ, 'assets')
        self.LOCAL_TEMPLATE = os.path.join(self.RAIZ, 'templates')
        self.LOCAL_CSS = os.path.join(self.RAIZ, 'static/css')
        self.DIRETORIO_DESTINO = os.path.join(self.RAIZ, 'templates')
        self.TEMPLATE = 'template.html'
        self.CSS = 'style.css'
        self.ARQUIVO_SAIDA = 'relatorio-saida.pdf'

        self.dicionario_funcoes = {
            "componente_tabela_padrao": self.componente_tabela_padrao
        }
        self.dados = json

    # Checa se o estado será com imagem azul ou branca
    def checa_estado(self, estado):
        if estado == 'Nível Ortográfico':
            return 'file://{}/check.png'.format(self.LOCAL_ASSETS)
        else:
            return 'file://{}/blank-check.png'.format(self.LOCAL_ASSETS)
    
    # Pega o título do nível
    def pega_nivel_titulo(self, nivel_numero):
        if nivel_numero == 1:
            return 'Coesão'
        if nivel_numero == 2:
            return 'Coerência Temática'
        if nivel_numero == 3:
            return 'Tipologia Textual'
        if nivel_numero == 4:
            return ''
        if nivel_numero == 5:
            return 'Registro Formal'
    
    def pega_nivel(self, nivel):
      if nivel == "A" or nivel == "Nível A":
        return '1'
      if nivel == "B" or nivel == "Nível B":
        return '2'
      if nivel == "C" or nivel == "Nível C":
        return '3'
      if nivel == "D" or nivel == "Nível D":
        return '4'
      if nivel == "E" or nivel == "Nível E":
        return '5'
    
    # TO DO
    # Colocar mais níveis ortográficos
    def pega_estados(self, estado):
      if estado == "Nível Ortográfico":
        normal = 'check.png'
        branco = 'blank-check.png'
        pre_silabico = branco
        defeito = branco
      else:
        normal = 'blank-check.png'
        branco = normal
        pre_silabico = branco
        defeito = branco

      return normal, branco, pre_silabico, defeito

    # Método que gera uma tabela padrão com bordas
    def componente_tabela_padrao(self):
        nome = self.dados['nome']
        turma = self.dados['turma']
        ciclo = self.dados['ciclo']
        data = self.dados['data']
        escola = self.dados['escola']
        cidade = self.dados['cidade']
        uf = self.dados['uf']

        estado = self.dados['result']['ortografia']['level']
        normal, branco, pre_silabico, defeito = self.pega_estados(estado)

        nivel_ortografico = self.dados['result']['ortografia']['level']
        
        cabecalho = f'''
        <div class="componente-tabela-padrao">
        <table class="tabela-padrao">
        <thead>
          <tr>
            <th class="tabela-padrao-linha tabela-aluno" colspan="2"><h3>{nome}</h3><small>{turma}</small></th>
            <th class="tabela-padrao-linha tabela-realizacao" colspan="7">Ciclo {ciclo} – Prova realizada em {data}<h6>{escola} – Cidade {cidade} – {uf}</h6></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="tabela-padrao-linha tabela-correcao-viavel" colspan="2">

              <table>
                <tr>
                  <td>
                    <img id="check-grande" src="file://{self.LOCAL_ASSETS}/check-grande.png">
                  </td>
                  <td>
                    <h2> Correção Viável: <small>{nivel_ortografico}</small></h2>
                  </td>
                </tr>
              </table>
            
            </td>
            <td class="tabela-correcoes" colspan="7">
              <table class="tabela-estado">
                <tr>
                  <td>
                    Normal
                  </td>
                  <td>
                    Em Branco
                  </td>
                  <td>
                    Pré-silábico
                  </td>
                  <td>
                    Defeito
                  </td>
                </tr>
                <tr>
                  <td><img src="file://{self.LOCAL_ASSETS}/{normal}"></td>
                  <td><img src="file://{self.LOCAL_ASSETS}/{branco}"></td>
                  <td><img src="file://{self.LOCAL_ASSETS}/{pre_silabico}"></td>
                  <td><img src="file://{self.LOCAL_ASSETS}/{defeito}"></td>
                </tr>
              </table>

              
            </td>
          </tr>'''
        
        padrao = cabecalho

        # Primeiro Nível
        primeiro_nivel = self.pega_nivel(self.dados['result']['coesao']['level'])
        primeiro_nivel_titulo = 'Coesão'
        primeiro_nivel_descricao = self.dados['result']['coesao']['description']

        # Segundo Nível
        segundo_nivel = self.pega_nivel(self.dados['result']['pontuacao']['level'])
        segundo_nivel_titulo = 'Pontuação'
        segundo_nivel_descricao = self.dados['result']['pontuacao']['description']

        # Terceiro Nível
        terceiro_nivel = self.pega_nivel(self.dados['result']['segmentacao']['level'])
        terceiro_nivel_titulo = 'Segmentação'
        terceiro_nivel_descricao = self.dados['result']['segmentacao']['description']

        # Quarto Nível
        quarto_nivel = self.pega_nivel(self.dados['result']['tipologia_textual']['level'])
        quarto_nivel_titulo = 'Tipologia Textual'
        quarto_nivel_descricao = self.dados['result']['tipologia_textual']['description']

        # Quinto Nível
        quinto_nivel = self.pega_nivel(self.dados['result']['adequacao_a_proposta']['level'])
        quinto_nivel_titulo = 'Adequação à proposta'
        quinto_nivel_descricao = self.dados['result']['adequacao_a_proposta']['description']

        corpo = f"""
          <! -- Primeiro e Segundo --!>
          <tr>
            <td class="tabela-padrao-imagem tabela-coesao-imagem" rowspan="2"><img src="file://{self.LOCAL_ASSETS}/niveis/coesao{primeiro_nivel}.png"></td>
            <td class="tabela-padrao-linha tabela-coesao coesao" rowspan="2"><h4>{primeiro_nivel_titulo}</h4><p>{primeiro_nivel_descricao}<p></td>
            
            <td class="tabela-padrao-imagem tabela-pontuacao-imagem" rowspan="2"><img src="file://{self.LOCAL_ASSETS}/niveis/pontuacao{segundo_nivel}.png"></td>
            <td class="tabela-padrao-linha tabela-pontuacao-direita pontuacao" rowspan="2"><h4>{segundo_nivel_titulo}</h4><p>{segundo_nivel_descricao}<p></td>  
          </tr>
          
          <tr>
          </tr>

          <! -- Terceiro e Quarto --!>
          <tr>
            <td class="tabela-padrao-imagem tabela-segmentacao-imagem" rowspan="2"><img src="file://{self.LOCAL_ASSETS}/niveis/segmentacao{terceiro_nivel}.png"></td>
            <td class="tabela-padrao-linha tabela-segmentacao segmentacao" rowspan="2"><h4>{terceiro_nivel_titulo}</h4><p>{terceiro_nivel_descricao}<p></td>
            
            <td class="tabela-padrao-imagem tabela-tipologia-textual-imagem" rowspan="2"><img src="file://{self.LOCAL_ASSETS}/niveis/tipologia_textual{quarto_nivel}.png"></td>
            <td class="tabela-padrao-linha tabela-tipologia-textual-direita tipologia-textual" rowspan="2"><h4>{quarto_nivel_titulo}</h4><p>{quarto_nivel_descricao}<p></td>  
          </tr>
          
          <tr>
          </tr>

          <!-- Quinto e Link -->
          <tr>
            <td class="tabela-padrao-imagem tabela-adequacao-a-proposta-imagem" rowspan="2"><img src="file://{self.LOCAL_ASSETS}/niveis/adequacao_a_proposta{quinto_nivel}.png"></td>
            <td class="tabela-padrao-linha tabela-adequacao-a-proposta adequacao-a-proposta" rowspan="2"><h4>{quinto_nivel_titulo}</h4><p>{quinto_nivel_descricao}<p></td>
            
            <td class="tabela-padrao-link tabela-link" rowspan="2" colspan="2">Acesse o <b>Plano Personalizado</b> aqui: <a href="http:/abreai.com/fedf6">http:/abreai.com/fedf6</a></td>
            
          </tr>
          <tr>
          </tr>

          <tr>
            <td class="tabela-padrao-linha tabela-rodape" colspan="2"></td>
            <td class="tabela-padrao-linha tabela-meio"></td>
            <td class="tabela-logos" colspan="6">
              <img src="file://{self.LOCAL_ASSETS}/logos.png">
            </td>
          </tr>
          
            </tbody>
            </table>
          </div>
          """

        padrao = cabecalho + corpo

        print(padrao)

        return padrao

    # Método principal que chama o JINJA para gerar o template HTML e converter em PDF
    def gerar_caderno(self):
        ambiente = Environment(loader=FileSystemLoader(self.LOCAL_TEMPLATE))
        template = ambiente.get_template(self.TEMPLATE)
        template.globals.update(self.dicionario_funcoes)
        css = os.path.join(self.LOCAL_CSS, self.CSS)

        # Variáveis
        variaveis_template = { 'assets_dir': 'file://' + self.LOCAL_ASSETS}

        # Renderizando HTML pra string
        string_renderizada = template.render(variaveis_template)
        html = weasyprint.HTML(string=string_renderizada)
        relatorio = os.path.join(self.DIRETORIO_DESTINO, self.ARQUIVO_SAIDA)
        return html.write_pdf(stylesheets=[css])