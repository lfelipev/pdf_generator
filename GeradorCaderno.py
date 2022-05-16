import os
import weasyprint
from jinja2 import Environment, FileSystemLoader
import json
from pathlib import Path

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
        if estado == 'True':
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
    
    # Pega a descrição do nível
    def pega_nivel_descricao(self, nivel_numero):
        if nivel_numero == 1:
            return 'Palavras e períodos justapostos e desconexos ao longo do texto, ou seja, ausência de articulação, porém há uma coesão marcada pela relação lógica entre palavras e/ou enunciados ou Repertório coesivo escasso e com desvios recorrentes.'
        if nivel_numero == 2:
            return 'Apresenta progressão textual insuficiente, utilizando-se apenas das ideias da situação motivadora e/ou Apresenta progressão textual completa, porém com predomínio de trechos copiados da situação motivadora.'
        if nivel_numero == 3:
            return 'Apresenta e desenvolve apenas 2 (duas) partes estruturantes do enredo narrativo (orientação, complicação e desfecho) e/ou apresenta as 3 (três) partes, mas não desenvolve 2 (duas) delas e/ou apresenta apenas 2 (dois) elementos que concorrem para a construção da narrativa (personagens, narrador, organização temporal, lugar).'
        if nivel_numero == 4:
            return ''
        if nivel_numero == 5:
            return 'Apresenta estrutura morfossintática bem empregada com, no máximo, 5 (cinco) desvios pontuais e não recorrentes.'

    # Método que gera uma tabela padrão com bordas
    def componente_tabela_padrao(self):
        nome = self.dados['nome']
        ano = self.dados['ano']
        turma = self.dados['turma']
        ciclo = self.dados['ciclo']
        data = self.dados['data']
        escola = self.dados['escola']
        cidade = self.dados['cidade']
        uf = self.dados['uf']

        normal = self.dados['estado']['normal']
        branco = self.dados['estado']['branco']
        insuficiente = self.dados['estado']['insuficiente']
        anulado = self.dados['estado']['anulado']
        copia = self.dados['estado']['copia']
        nao_alfabetico = self.dados['estado']['nao_alfabetico']
        fuga_ao_tema = self.dados['estado']['fuga_ao_tema']
        fuga_a_tipologia = self.dados['estado']['fuga_a_tipologia']

        cabecalho = '''
        <div class="componente-tabela-padrao">
        <table class="tabela-padrao">
        <thead>
          <tr>
            <th class="tabela-padrao-linha tabela-aluno" colspan="2"><h3>{}</h3><small><b>{}</b> Ano - Turma <b>{}</b></small></th>
            <th class="tabela-padrao-linha tabela-realizacao" colspan="7">Ciclo {} – Prova realizada em {}<h6>{} – Cidade {} – {}</h6></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="tabela-padrao-linha tabela-correcao-viavel" colspan="2">

              <table>
                <tr>
                  <td>
                    <img id="check-grande" src="file://{}/check-grande.png">
                  </td>
                  <td>
                    <h2> Correção Viável</h2>
                  </td>
                </tr>
              </table>
            
            </td>
            <td class="tabela-padrao-linha tabela-correcoes" colspan="7">
              <table class="tabela-estado">
                <tr>
                  <td>
                    Normal
                  </td>
                  <td>
                    Branco
                  </td>
                  <td>
                    Insuficiente
                  </td>
                  <td>
                    Anulado
                  </td>
                  <td>
                    Cópia
                  </td>
                  <td>
                    Não alfabético
                  </td>
                  <td>
                    Fuga ao tema
                  </td>
                  <td>
                    Fuga à tipologia
                  </td>
                </tr>
                <tr>
                  <td><img src="{}"></td>
                  <td><img src="{}"></td>
                  <td><img src="{}"></td>
                  <td><img src="{}"></td>
                  <td><img src="{}"></td>
                  <td><img src="{}"></td>
                  <td><img src="{}"></td>
                  <td><img src="{}"></td>
                </tr>
              </table>

              
            </td>
          </tr>'''.format(nome, ano, turma, ciclo, data, escola, cidade, uf, self.LOCAL_ASSETS, self.checa_estado(normal), self.checa_estado(branco), self.checa_estado(insuficiente), self.checa_estado(anulado), self.checa_estado(copia), self.checa_estado(nao_alfabetico), self.checa_estado(fuga_ao_tema), self.checa_estado(fuga_a_tipologia))

        niveis = len(self.dados['niveis'])

        padrao = cabecalho
        for i in range(0, niveis):
            nivel_numero = self.dados['niveis'][i]['numero']
            nivel_img = 'file://{}/nivel{}.png'.format(self.LOCAL_ASSETS, nivel_numero)
            nivel_titulo = self.pega_nivel_titulo(int(nivel_numero))
            nivel_descricao = self.pega_nivel_descricao(int(nivel_numero))

            padrao = padrao + """
            <!-- Nível 5 -->
            <tr>
            <td class="tabela-padrao-imagem tabela-nivel-{}-imagem" rowspan="2"><img src="{}"></td>
            <td class="tabela-padrao-linha tabela-nivel-{} nivel-{}" rowspan="2"><h4>{}</h4><p>{}</p></td>
            <td class="tabela-padrao-linha  pontos-niveis-cabecalho pontos-niveis-cabecalho-1" colspan="7" rowspan="2">
            <table id="interna" class="tabela-interna">
            <tr>
            <td class="td-cabecalho"><p>O que está bom</p></td>
            <td class="td-lista">
            <ul class="lista-padrao-verde">""".format(nivel_numero, nivel_img, nivel_numero, nivel_numero, nivel_titulo, nivel_descricao)

            for elemento in self.dados['niveis'][i]['o-que-esta-bom']:
                padrao = padrao + "<li>{}</li>".format(elemento)
                        
            padrao = padrao + """
            </ul>
            </td>
            </tr>
            <tr>
            <td class="td-cabecalho"><p>O que pode melhorar</p></td>
            <td class="td-lista">
            <ul class="lista-padrao-vermelho">
            """

            for elemento in self.dados['niveis'][i]['o-que-pode-melhorar']:
                padrao = padrao + "<li>{}</li>".format(elemento)
            
            padrao = padrao + """
            <li>Emprego indevido da vírgula</li>
            </ul>
            </td>
            </tr>
            </table>
            </td>
            </tr>
            <tr>
            </tr>
            """
        rodape = """
            <tr>
                <td class="tabela-padrao-linha tabela-rodape" colspan="2">Acesse o <b>Plano Personalizado</b> aqui: <a href="http:/abreai.com/fedf6">http:/abreai.com/fedf6</a></td>
                <td class="tabela-padrao-linha tabela-meio"></td>
                <td class="tabela-padrao-linha tabela-logos" colspan="6">Logos</td>
            </tr>
            </tbody>
            </table>
        </div>
        """
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
        return html.write_pdf(relatorio, stylesheets=[css])

# Método que retorna o JSON do caderno no formato dicionário
def get_json():
    # Open the orders.json file
    with open("caderno.json", encoding='utf-8') as file:
        # Load its content and make a new dictionary
        data = json.load(file)
        return data

json = get_json()
    
gerar_caderno = GeradorCaderno(json)
gerar_caderno.gerar_caderno()