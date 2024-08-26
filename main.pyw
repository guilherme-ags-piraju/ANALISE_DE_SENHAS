# ==============================================================================
#  Projeto: PRJ003_ANALISE_DE_SENHA
#  Versão:  v1.2
#  Autor:   Guilherme Augusto
#  Data:    2024-08-26
# ==============================================================================

"""
Este programa avalia a força de uma senha fornecida com base em vários critérios,
como comprimento, inclusão de letras maiúsculas e minúsculas, números, caracteres
especiais e a ausência de padrões comuns (como "12345" ou "senha"). Além disso,
oferece a opção de gerar uma senha segura e exportar relatórios detalhados.

Histórico de Revisões:
------------------------------------------------------------------------------
v1.0 - 2024-08-25 - Guilherme Augusto
    * Criação da lógica
v1.1 - 2024-08-26 - Guilherme Augusto
    * Código refatorado para maior clareza e eficiência
    * Adicionadas sugestões de senhas fortes
    * Implementado feedback visual em tempo real
    * Adicionado suporte para exportação de relatórios
v1.2 - 2024-08-26 - Guilherme Augusto
    * Adicionada função de gerar senha segura
    * Relatório detalhado com feedback completo
    * Mensagem de senha forte adicionada
------------------------------------------------------------------------------
"""
# ==============================================================================
#  Início do código
# ==============================================================================

import tkinter as tk
from tkinter import messagebox
import random
import string
import csv
from senhas_faceis import senhas_fracas

# Função para gerar uma senha forte com caracteres aleatórios
def gerar_senha_forte(tamanho=12):
    """
    Gera uma senha segura com um comprimento específico.
    A senha deve ter pelo menos 12 caracteres.

    :param tamanho: Comprimento da senha a ser gerada (mínimo de 12).
    :return: Senha gerada como uma string.
    """
    if tamanho < 12:
        raise ValueError("A senha deve ter pelo menos 12 caracteres.")
    caracteres = string.ascii_letters + string.digits + '@!#$%&*'
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha

# Função para exportar a senha gerada para um arquivo CSV
def exportar_relatorio(senha_gerada):
    """
    Exporta a senha gerada para um arquivo CSV chamado 'relatorio_senha_gerada.csv'.

    :param senha_gerada: Senha gerada que será salva no arquivo.
    """
    with open('relatorio_senha_gerada.csv', 'a', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow([senha_gerada])

# Função para exibir a pontuação da senha com base em critérios de segurança
def exibir_pontuacao_senha(pontuacao_final, pontuacao_inicial=6):
    """
    Atualiza o rótulo com o nível de segurança da senha e sua pontuação.

    :param pontuacao_final: Pontuação final da senha.
    :param pontuacao_inicial: Pontuação inicial máxima da senha.
    """
    niveis = {
        0: "Senha extremamente fraca",
        1: "Senha fraca",
        2: "Senha média",
        3: "Senha média",
        4: "Senha forte",
        5: "Senha muito forte",
        6: "Senha excelente"
    }
    nivel_seguranca = niveis.get(pontuacao_final, "Nível de segurança desconhecido")
    resultado_var.set(f"Nível de segurança: {nivel_seguranca}\nPontuação: {pontuacao_final}/{pontuacao_inicial}")

# Função para detectar sequências repetidas na senha
def detectar_repeticoes_senha(senha, tamanho_sequencia=3):
    """
    Detecta padrões repetidos na senha para ajudar a identificar padrões previsíveis.

    :param senha: Senha fornecida pelo usuário.
    :param tamanho_sequencia: Tamanho das sequências a serem verificadas.
    :return: Dicionário com sequências repetidas e suas contagens.
    """
    padroes = {}
    for i in range(len(senha) - tamanho_sequencia + 1):
        sequencia = senha[i:i + tamanho_sequencia]
        padroes[sequencia] = padroes.get(sequencia, 0) + 1
    return {seq: count for seq, count in padroes.items() if count > 1}

# Atualiza o feedback visual com base na entrada do usuário
def atualizar_feedback_visual(event=None):
    """
    Atualiza a cor de fundo do campo de entrada com base no comprimento da senha digitada.

    :param event: Evento de digitação que aciona a atualização.
    """
    senha_usuario = entrada_senha.get()
    if senha_usuario:
        if len(senha_usuario) > 12:
            entrada_senha.config(bg="#d4edda")  # Verde claro
        else:
            entrada_senha.config(bg="#f8d7da")  # Vermelho claro
        resultado_var.set(f"Comprimento: {len(senha_usuario)} caracteres")
    else:
        entrada_senha.config(bg="#ffffff")  # Cor padrão

# Valida a senha fornecida pelo usuário com base em critérios de segurança
def validar_senha():
    """
    Avalia a força da senha fornecida e exibe um relatório detalhado.
    """
    senha_usuario = entrada_senha.get()
    if not senha_usuario:
        messagebox.showwarning("Aviso", "Por favor, digite uma senha para validação.")
        return
    pontuacao_inicial = 6
    pontuacao_final = pontuacao_inicial
    mensagens = []
    if senha_usuario in senhas_fracas:
        mensagens.append("Sua senha é fraca! Evite usar senhas fáceis de serem descobertas.\n")
        pontuacao_final -= 1
    if len(senha_usuario) <= 6:
        mensagens.append(f"Sua senha é muito curta! ({len(senha_usuario)} caracteres). "
                         f"Experimente usar uma senha maior.\n")
        pontuacao_final -= 1
    caracteres_especiais = set('@!#$%&*')
    if not any(char in caracteres_especiais for char in senha_usuario):
        mensagens.append("Experimente adicionar caracteres especiais (Ex: @, !, #, $, %, &, *).\n")
        pontuacao_final -= 1
    if senha_usuario.isdigit():
        mensagens.append("Senha contém somente números! "
                         "Experimente adicionar letras para uma senha mais segura.\n")
        pontuacao_final -= 1
    if senha_usuario.islower():
        mensagens.append("Senha não possui letra maiúscula. "
                         "Experimente adicionar letras maiúsculas para uma senha mais forte.\n")
        pontuacao_final -= 1
    repeticoes = detectar_repeticoes_senha(senha_usuario, tamanho_sequencia=3)
    if repeticoes:
        mensagens.append(f"Sequências repetidas encontradas. "
                         f"Experimente não utilizar sequências repetidas.\n")
        pontuacao_final -= 1
    if pontuacao_final == pontuacao_inicial:
        mensagens.append("Parabéns! Sua senha atende a todos os critérios e é considerada muito segura!\n")
    exibir_pontuacao_senha(pontuacao_final, pontuacao_inicial)
    messagebox.showinfo("Avaliação da Senha", "\n".join(mensagens))

# Gera uma senha segura com base no comprimento fornecido
def gerar_senha():
    """
    Gera uma nova senha segura com base no comprimento especificado pelo usuário
    e salva a senha gerada em um arquivo CSV.
    """
    tamanho_str = entrada_tamanho.get()
    if not tamanho_str:
        messagebox.showwarning("Aviso", "Por favor, digite o comprimento da senha.")
        return
    try:
        tamanho = int(tamanho_str)
        senha_forte = gerar_senha_forte(tamanho)
        messagebox.showinfo("Senha Gerada", f"Sua nova senha segura é: {senha_forte}\n"
                                            f"Você pode visualizar-lá no arquivo 'relatorio_senha_gerada.csv'.")
        exportar_relatorio(senha_forte)
    except ValueError:
        messagebox.showerror("Erro", "O comprimento deve ser um número inteiro válido.")

# Centraliza a janela na tela
def centralizar_janela(janela, largura, altura):
    """
    Centraliza a janela na tela com base nas dimensões fornecidas.

    :param janela: Instância da janela Tkinter.
    :param largura: Largura da janela.
    :param altura: Altura da janela.
    """
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f'{largura}x{altura}+{x}+{y}')

# Alterar a cor de fundo dos botões quando o mouse passa sobre eles
def on_enter(event):
    """
    Altera a cor de fundo do botão quando o mouse passa sobre ele.

    :param event: Evento de passar o mouse sobre o botão.
    """
    event.widget.config(bg="#1c8c54", fg="#ffffff")

# Alterar a cor de fundo dos botões quando o mouse sai deles
def on_leave(event):
    """
    Restaura a cor de fundo do botão quando o mouse sai dele.

    :param event: Evento de sair o mouse do botão.
    """
    event.widget.config(bg="#1c7c54", fg="#ffffff")

# Configuração da interface gráfica com Tkinter
root = tk.Tk()
root.title("Análise de Segurança de Senha - Guilherme Augusto")
root.configure(bg="#2e3f4f")

# Centraliza a janela na tela
centralizar_janela(root, 450, 500)

# Título da aplicação
titulo = tk.Label(root, text="Validador de Senhas", font=("Arial", 18, "bold"), fg="#ffffff", bg="#2e3f4f")
titulo.pack(pady=15)

# Subtítulo da aplicação
subtitulo = tk.Label(root, text="Digite sua senha abaixo:", font=("Arial", 14), fg="#ffffff", bg="#2e3f4f")
subtitulo.pack(pady=10)

# Campo de entrada para a senha do usuário
entrada_senha = tk.Entry(root, show="*", width=35, font=("Arial", 12), borderwidth=2, relief="flat")
entrada_senha.pack(pady=15)
entrada_senha.bind('<KeyRelease>', atualizar_feedback_visual)

# Botão para validar a senha fornecida
botao_validar = tk.Button(root, text="Validar Senha", font=("Arial", 12, "bold"), bg="#1c7c54", fg="#ffffff",
                          command=validar_senha)
botao_validar.pack(pady=10)
botao_validar.bind("<Enter>", on_enter)
botao_validar.bind("<Leave>", on_leave)

# Rótulo para exibir o resultado da validação da senha
resultado_var = tk.StringVar()
resultado_label = tk.Label(root, textvariable=resultado_var, font=("Arial", 12), fg="#ffffff", bg="#2e3f4f")
resultado_label.pack(pady=15)

# Label para informar o comprimento da senha a ser gerada
tamanho_label = tk.Label(root, text="Digite o comprimento da senha a ser gerada:", font=("Arial", 12),
                         fg="#ffffff", bg="#2e3f4f")
tamanho_label.pack(pady=10)

# Campo de entrada para o comprimento da senha a ser gerada
entrada_tamanho = tk.Entry(root, width=10, font=("Arial", 12), borderwidth=2, relief="flat")
entrada_tamanho.pack(pady=5)

# Botão para gerar uma nova senha segura
botao_gerar = tk.Button(root, text="Gerar Senha Segura", font=("Arial", 12, "bold"), bg="#1c7c54", fg="#ffffff",
                       command=gerar_senha)
botao_gerar.pack(pady=10)
botao_gerar.bind("<Enter>", on_enter)
botao_gerar.bind("<Leave>", on_leave)

# Rodapé com a informação do autor
footer = tk.Label(root, text="Desenvolvido por Guilherme Augusto", font=("Arial", 10), fg="#ffffff", bg="#2e3f4f")
footer.pack(side="bottom", pady=10)

# Inicia o loop principal da interface gráfica
root.mainloop()