import sqlite3
import json
import os

def link_ja_foi_postado(link_recebido):
    
    conexao = sqlite3.connect("noticias.db")
    
    conexao.row_factory = sqlite3.Row
    
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM noticias_postadas WHERE link = ?", (link_recebido,))
    
    resultado = cursor.fetchone()
    
    conexao.close()
    
    if resultado is not None:
        return True 
    else:
        return False

def salvar_novo_link(link_aprovado):
    conexao = sqlite3.connect("noticias.db")
    cursor = conexao.cursor()
    
    cursor.execute("INSERT INTO noticias_postadas (link) VALUES (?)", (link_aprovado,))
    
    # IMPORTANTE: Sempre que alterar dados (INSERT, UPDATE, DELETE), precisa do commit
    conexao.commit()
    conexao.close()

def testar_validacao_noticia():
    pasta_dados = "dados_teste"
    
    arquivo_entrada = os.path.join(pasta_dados, "link_noticias.json")
    arquivo_banco = os.path.join(pasta_dados, "noticias_postadas.json")
    
    try:
        with open(arquivo_entrada, "r", encoding="utf-8") as f:
            noticia_atual = json.load(f)
            link_atual = noticia_atual.get("link")
    except FileNotFoundError:
        print(f"Erro: O arquivo não foi encontrado em: '{arquivo_entrada}'")
        print("Verifique se a pasta 'dados_teste' existe e contém o arquivo 'link_noticias.json'.")
        return
    
    if os.path.exists(arquivo_banco):
        with open(arquivo_banco, "r", encoding="utf-8") as f:
            try:
                historico_postagens = json.load(f)
            except json.JSONDecodeError:
                historico_postagens = []
    else:
        historico_postagens = []
        
    links_postados = [noticia["link"] for noticia in historico_postagens if "link" in noticia]
    
    if link_atual in links_postados:
        print("noticia ja postada")
        return "noticia ja postada"
    else:
        print("validando noticia")
        
        chamar_ia_para_validar(noticia_atual, arquivo_banco, historico_postagens)
        return "validando noticia"


def chamar_ia_para_validar(noticia, caminho_arquivo_banco, historico_postagens):
    """
    Função simuladora da IA. Se a IA aprovar, ela salva a notícia 
    na pasta correta 'dados_teste/noticias_postadas.json'.
    """
    print(f"-> [IA] Analisando a relevância do link: {noticia['link']}...")
    
    ia_aprovou = True 
    
    if ia_aprovou:
        print("-> [IA] Notícia aprovada! Salvando no banco de dados local...")
        
        historico_postagens.append(noticia)
        
        pasta_destino = os.path.dirname(caminho_arquivo_banco)
        if pasta_destino and not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
        
        with open(caminho_arquivo_banco, "w", encoding="utf-8") as f:
            json.dump(historico_postagens, f, indent=4, ensure_ascii=False)
            
        print(f"-> [Sucesso] Link armazenado em '{caminho_arquivo_banco}'. Pronto para enviar ao Embed!")
    else:
        print("-> [IA] Notícia descartada por falta de relevância.")

# --- EXECUTAR O TESTE ---
if __name__ == "__main__":
    testar_validacao_noticia()