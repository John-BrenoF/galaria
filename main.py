import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, UnidentifiedImageError
import ttkbootstrap as ttk
import itertools

EXTENSOES_IMAGENS = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff")

def buscar_imagens(diretorio, filtro_ext=None):
    imagens = []
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            if file.lower().endswith(EXTENSOES_IMAGENS):
                if filtro_ext is None or file.lower().endswith(filtro_ext):
                    imagens.append(os.path.join(root, file))
    return imagens

def criar_placeholder_image(size):
    img = Image.new('RGB', (size, size), color = 'gray')
    return ImageTk.PhotoImage(img)

def abrir_imagem(caminho):
    global current_image_index, imagens_list
    try:
        img = Image.open(caminho)
    except UnidentifiedImageError:
        return
    top = ttk.Toplevel()
    top.title(os.path.basename(caminho))
    top.geometry(f"{top.winfo_screenwidth()-100}x{top.winfo_screenheight()-150}")
    
    img.thumbnail((top.winfo_screenwidth()-100, top.winfo_screenheight()-150))
    foto = ImageTk.PhotoImage(img)
    lbl = ttk.Label(top, image=foto)
    lbl.image = foto
    lbl.pack(padx=20, pady=20, expand=True)

    current_image_index = imagens_list.index(caminho)

    def proxima(e=None):
        abrir_imagem(imagens_list[(current_image_index+1) % len(imagens_list)])
        top.destroy()
    def anterior(e=None):
        abrir_imagem(imagens_list[(current_image_index-1) % len(imagens_list)])
        top.destroy()

    top.bind("<Right>", proxima)
    top.bind("<Left>", anterior)
    top.bind("<Escape>", lambda e: top.destroy())
    lbl.bind("<Button-1>", proxima)

    btn_deletar = ttk.Button(top, text="🗑️ Deletar Imagem", command=lambda: [deletar_imagem(caminho), top.destroy()], bootstyle="danger")
    btn_deletar.pack(pady=10)

    frame_renomear = ttk.Frame(top)
    frame_renomear.pack(pady=5)

    nome_atual = os.path.splitext(os.path.basename(caminho))[0]
    var_novo_nome = tk.StringVar(value=nome_atual)
    entry_renomear = ttk.Entry(frame_renomear, textvariable=var_novo_nome, width=40)
    entry_renomear.pack(side="left", padx=5)

    def acao_renomear():
        nonlocal caminho
        novo_caminho = renomear_imagem(caminho, var_novo_nome.get())
        if novo_caminho:
            caminho = novo_caminho
            top.title(os.path.basename(caminho))
    
    btn_renomear = ttk.Button(frame_renomear, text="Renomear", command=acao_renomear, bootstyle="info")
    btn_renomear.pack(side="left", padx=5)

def deletar_imagem(caminho):
    global imagens_list
    if os.path.exists(caminho):
        if var_confirmar_exclusao.get():
            resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar a imagem: {os.path.basename(caminho)}?")
            if not resposta:
                return
        
        os.remove(caminho)
        print(f"Imagem deletada: {caminho}")
        imagens_list = [img for img in imagens_list if img != caminho]
        atualizar_galeria()
    else:
        print(f"Erro: Imagem não encontrada para deletar: {caminho}")

def renomear_imagem(caminho_antigo, novo_nome):
    global imagens_list
    diretorio, nome_antigo = os.path.split(caminho_antigo)
    extensao = os.path.splitext(nome_antigo)[1]
    novo_caminho = os.path.join(diretorio, novo_nome + extensao)

    if os.path.exists(caminho_antigo):
        try:
            os.rename(caminho_antigo, novo_caminho)
            print(f"Imagem renomeada de {caminho_antigo} para {novo_caminho}")
            index = imagens_list.index(caminho_antigo)
            imagens_list[index] = novo_caminho
            atualizar_galeria()
            return novo_caminho
        except OSError as e:
            print(f"Erro ao renomear imagem: {e}")
    else:
        print(f"Erro: Imagem não encontrada para renomear: {caminho_antigo}")
    return None

def atualizar_galeria(event=None):
    app.after(50, lambda: carregar_galeria(var_diretorio.get(), var_busca.get(), var_ext.get()))

def carregar_galeria(diretorio, filtro="", filtro_ext=None):
    global imagens_list
    ext_para_buscar = filtro_ext if filtro_ext != "Todos" else None
    imagens = buscar_imagens(diretorio, ext_para_buscar)
    imagens_list = imagens.copy()
    if filtro:
        imagens = [img for img in imagens if filtro.lower() in os.path.basename(img).lower()]

    for widget in frame_galeria.winfo_children():
        widget.destroy()

    lbl_progresso_texto.pack(pady=(2, 0))
    barra_progresso.pack(fill="x", padx=20, pady=0, side="bottom")
    barra_progresso["maximum"] = len(imagens)
    barra_progresso["value"] = 0
    var_progresso_texto.set(f"Carregando 0 de {len(imagens)} imagens...")
    app.update_idletasks()

    largura_janela = app.winfo_width() - 200
    colunas = max(3, largura_janela // (miniatura_tamanho.get() + 20))

    for i, caminho in enumerate(imagens):
        try:
            img = Image.open(caminho)
            img.thumbnail((miniatura_tamanho.get(), miniatura_tamanho.get()))
            img = ImageOps.fit(img, (miniatura_tamanho.get(), miniatura_tamanho.get()), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(img)

            frame_item = ttk.Frame(frame_galeria, padding=5, bootstyle="secondary")
            frame_item.grid(row=i // colunas, column=i % colunas, padx=10, pady=10, sticky="n")

            btn = ttk.Button(frame_item, image=foto, command=lambda c=caminho: abrir_imagem(c), bootstyle="light")
            btn.image = foto
            btn.pack()

            lbl_nome = ttk.Label(frame_item, text=os.path.basename(caminho)[:25], anchor="center", wraplength=miniatura_tamanho.get())
            lbl_nome.pack(pady=(5,0))

            def on_enter(e, b=btn):
                b.configure(style="info.TButton")
            def on_leave(e, b=btn):
                b.configure(style="light.TButton")
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        except UnidentifiedImageError:
            print(f"Arquivo não suportado: {caminho}")
            foto = criar_placeholder_image(miniatura_tamanho.get())
            btn = ttk.Button(frame_item, image=foto, command=lambda c=caminho: abrir_imagem(c), bootstyle="light")
            btn.image = foto
            btn.pack()
        finally:
            barra_progresso["value"] += 1
            var_progresso_texto.set(f"Carregando {barra_progresso['value']} de {barra_progresso['maximum']} imagens...")
            app.update_idletasks()
    
    barra_progresso.pack_forget()
    lbl_progresso_texto.pack_forget()

def abrir_configuracoes():
    config_window = ttk.Toplevel()
    config_window.title("⚙️ Configurações")
    config_window.geometry("450x350")

    ttk.Label(config_window, text="Tema:", bootstyle="inverse-light").pack(pady=10)
    tema_entry = ttk.Combobox(config_window, values=app.style.theme_names(), state="readonly")
    tema_entry.set(app.style.theme_use())
    tema_entry.pack(pady=5)

    def aplicar_tema():
        app.style.theme_use(tema_entry.get())
    ttk.Button(config_window, text="Aplicar Tema", bootstyle="primary", command=aplicar_tema).pack(pady=10)

    ttk.Label(config_window, text="Tamanho das Miniaturas:", bootstyle="inverse-light").pack(pady=10)
    ttk.Scale(config_window, from_=80, to=300, variable=miniatura_tamanho, orient="horizontal").pack(pady=5)
    ttk.Button(config_window, text="Aplicar Tamanho", bootstyle="info", command=atualizar_galeria).pack(pady=10)

    ttk.Label(config_window, text="Confirmação ao Deletar:", bootstyle="inverse-light").pack(pady=10)
    check_confirm_delete = ttk.Checkbutton(config_window, text="Pedir confirmação antes de deletar", variable=var_confirmar_exclusao, bootstyle="round-toggle")
    check_confirm_delete.pack(pady=5)

def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar.pack_forget()
        toggle_sidebar_btn.pack_configure(side="left", anchor="nw", padx=5, pady=5)
    else:
        sidebar.pack(fill="y", side="left")
        toggle_sidebar_btn.pack_forget()
        toggle_sidebar_btn.pack(side="left", anchor="nw", padx=5, pady=5)
    sidebar_visible = not sidebar_visible

app = ttk.Window(themename="darkly")
app.title("📸 Galeria Moderna - BigLinux")
try:
    app.attributes("-zoomed", True)
except:
    try:
        app.attributes("-fullscreen", True)
    except:
        app.style.theme_use("default")

miniatura_tamanho = tk.IntVar(app, value=160)
var_diretorio = tk.StringVar(app, value="/home/.../Imagens/")
var_busca = tk.StringVar(app)
var_ext = tk.StringVar(app, value=None)
imagens_list = []
current_image_index = 0
sidebar_visible = True
var_progresso_texto = tk.StringVar(app, value="")
var_confirmar_exclusao = tk.BooleanVar(app, value=True)

sidebar = ttk.Frame(app, padding=5, bootstyle="dark")
toggle_sidebar_btn = ttk.Button(app, text="☰", command=lambda: toggle_sidebar(), bootstyle="secondary")
toggle_sidebar_btn.pack(side="left", anchor="nw", padx=5, pady=5)

sidebar.pack(fill="y", side="left")

ttk.Label(sidebar, text="📁 Pasta:").pack(pady=(5, 2))
ttk.Entry(sidebar, textvariable=var_diretorio, width=30).pack(pady=2, padx=2)
ttk.Button(sidebar, text="Mudar Pasta", bootstyle="primary", command=lambda: var_diretorio.set(filedialog.askdirectory() or var_diretorio.get()) or atualizar_galeria()).pack(pady=2, padx=2)

ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=5)

ttk.Label(sidebar, text="🔎 Buscar:").pack(pady=(10, 5))
ttk.Entry(sidebar, textvariable=var_busca, width=30).pack(pady=5, padx=5)
ttk.Button(sidebar, text="Filtrar", bootstyle="success", command=atualizar_galeria).pack(pady=5, padx=5)

ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=10)

ttk.Label(sidebar, text="Tipo:").pack(pady=(10, 5))
ext_combobox = ttk.Combobox(sidebar, textvariable=var_ext, values=[ext for ext in EXTENSOES_IMAGENS] + ["Todos"], state="readonly", width=25)
ext_combobox.set("Todos")
ext_combobox.pack(pady=2, padx=2)
ext_combobox.bind("<<ComboboxSelected>>", atualizar_galeria)

ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=10)

ttk.Button(sidebar, text="⚙️ Configurações", bootstyle="secondary", command=abrir_configuracoes).pack(side="bottom", pady=5, padx=2)

lbl_progresso_texto = ttk.Label(app, textvariable=var_progresso_texto, bootstyle="secondary")
lbl_progresso_texto.pack_forget()

barra_progresso = ttk.Progressbar(app, length=300, bootstyle="secondary")
barra_progresso.pack_forget()

canvas_frame = ttk.Frame(app)
canvas_frame.pack(fill="both", expand=True, side="right")

canvas = tk.Canvas(canvas_frame, highlightthickness=0)
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

frame_galeria = ttk.Frame(canvas)
canvas.create_window((0,0), window=frame_galeria, anchor="nw")
frame_galeria.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

def _on_mousewheel(event):
    if event.num == 4 or event.delta > 0:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:
        canvas.yview_scroll(1, "units")
canvas.bind("<MouseWheel>", _on_mousewheel)
canvas.bind("<Button-4>", _on_mousewheel)
canvas.bind("<Button-5>", _on_mousewheel)

app.after(100, atualizar_galeria)

app.mainloop()
