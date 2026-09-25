"""
Módulo de interface gráfica.

Constrói a janela principal do Gerenciador de Notas usando Tkinter/ttk,
organizada em três áreas funcionais (RF/4.1):
  - Cadastro/edição de aluno
  - Consulta e listagem de alunos (com pesquisa)
  - Resumo com indicadores gerais da turma

Widgets usados: Entry, Button, Label, Combobox, Treeview, Listbox,
Scrollbar (>= 6 tipos, conforme 4.1).
"""

import tkinter as tk
from tkinter import ttk, messagebox

import dados
import validacoes


class AppGerenciadorNotas:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Gerenciador de Notas - SENAI")
        self.root.geometry("880x600")
        self.root.minsize(820, 560)

        # Estado em memória
        self.alunos: list[dict] = dados.carregar_alunos()
        self.notas_atuais: list[float] = []
        self.aluno_selecionado_id: int | None = None  # índice em self.alunos
        self.alteracoes_pendentes: bool = False

        self._construir_interface()
        self._atualizar_treeview()
        self._atualizar_resumo()

        self.root.protocol("WM_DELETE_WINDOW", self._ao_fechar)
        self.root.bind("<Return>", lambda evento: self._on_adicionar_nota())

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------
    def _construir_interface(self) -> None:
        titulo = ttk.Label(
            self.root, text="Gerenciador de Notas", font=("Segoe UI", 16, "bold")
        )
        titulo.pack(pady=(10, 0))

        container = ttk.Frame(self.root, padding=10)
        container.pack(fill="both", expand=True)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(0, weight=1)

        self._construir_area_cadastro(container)
        self._construir_area_consulta(container)
        self._construir_area_resumo(container)

    def _construir_area_cadastro(self, parent: ttk.Frame) -> None:
        area = ttk.Labelframe(parent, text="Cadastro do aluno", padding=10)
        area.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ttk.Label(area, text="Nome:").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_nome = ttk.Entry(area, width=28)
        self.entry_nome.grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(area, text="Turma:").grid(row=1, column=0, sticky="w", pady=4)
        self.combo_turma = ttk.Combobox(
            area, width=25, values=["1A", "1B", "2A", "2B", "3A", "3B"]
        )
        self.combo_turma.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Separator(area, orient="horizontal").grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=8
        )

        ttk.Label(area, text="Nota da avaliação:").grid(
            row=3, column=0, sticky="w", pady=4
        )
        self.entry_nota = ttk.Entry(area, width=10)
        self.entry_nota.grid(row=3, column=1, sticky="w", pady=4)

        botoes_nota = ttk.Frame(area)
        botoes_nota.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        ttk.Button(
            botoes_nota, text="Adicionar nota", command=self._on_adicionar_nota
        ).pack(side="left")
        ttk.Button(
            botoes_nota, text="Remover selecionada", command=self._on_remover_nota
        ).pack(side="left", padx=6)

        ttk.Label(area, text="Avaliações lançadas:").grid(
            row=5, column=0, columnspan=2, sticky="w"
        )
        lista_frame = ttk.Frame(area)
        lista_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.listbox_notas = tk.Listbox(lista_frame, height=6)
        self.listbox_notas.pack(side="left", fill="x", expand=True)
        scroll_notas = ttk.Scrollbar(
            lista_frame, orient="vertical", command=self.listbox_notas.yview
        )
        scroll_notas.pack(side="right", fill="y")
        self.listbox_notas.configure(yscrollcommand=scroll_notas.set)

        botoes_principais = ttk.Frame(area)
        botoes_principais.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        ttk.Button(
            botoes_principais, text="Salvar aluno", command=self._on_salvar
        ).pack(side="left")
        ttk.Button(
            botoes_principais, text="Excluir", command=self._on_excluir
        ).pack(side="left", padx=6)
        ttk.Button(
            botoes_principais, text="Limpar", command=self._on_limpar
        ).pack(side="left")

        area.columnconfigure(1, weight=1)

    def _construir_area_consulta(self, parent: ttk.Frame) -> None:
        area = ttk.Labelframe(parent, text="Alunos cadastrados", padding=10)
        area.grid(row=0, column=1, sticky="nsew")
        area.columnconfigure(0, weight=1)
        area.rowconfigure(2, weight=1)

        busca_frame = ttk.Frame(area)
        busca_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(busca_frame, text="Pesquisar:").pack(side="left")
        self.entry_pesquisa = ttk.Entry(busca_frame, width=25)
        self.entry_pesquisa.pack(side="left", padx=6)
        self.entry_pesquisa.bind("<KeyRelease>", lambda evento: self._atualizar_treeview())
        ttk.Label(busca_frame, text="Turma:").pack(side="left", padx=(10, 0))
        self.combo_filtro_turma = ttk.Combobox(busca_frame, width=10, values=["Todas"])
        self.combo_filtro_turma.set("Todas")
        self.combo_filtro_turma.pack(side="left", padx=6)
        self.combo_filtro_turma.bind(
            "<<ComboboxSelected>>", lambda evento: self._atualizar_treeview()
        )

        colunas = ("nome", "turma", "media", "situacao")
        self.treeview = ttk.Treeview(
            area, columns=colunas, show="headings", selectmode="browse"
        )
        self.treeview.heading("nome", text="Nome")
        self.treeview.heading("turma", text="Turma")
        self.treeview.heading("media", text="Média")
        self.treeview.heading("situacao", text="Situação")
        self.treeview.column("nome", width=200)
        self.treeview.column("turma", width=70, anchor="center")
        self.treeview.column("media", width=70, anchor="center")
        self.treeview.column("situacao", width=110, anchor="center")
        self.treeview.grid(row=2, column=0, sticky="nsew")
        self.treeview.bind("<<TreeviewSelect>>", self._on_selecionar_aluno)

        scroll_tree = ttk.Scrollbar(area, orient="vertical", command=self.treeview.yview)
        scroll_tree.grid(row=2, column=1, sticky="ns")
        self.treeview.configure(yscrollcommand=scroll_tree.set)

    def _construir_area_resumo(self, parent: ttk.Frame) -> None:
        area = ttk.Labelframe(parent, text="Resumo geral", padding=10)
        area.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        for indice in range(4):
            area.columnconfigure(indice, weight=1)

        self.label_total = ttk.Label(area, text="Total de alunos: 0")
        self.label_total.grid(row=0, column=0, sticky="w", padx=6)

        self.label_media_geral = ttk.Label(area, text="Média geral: -")
        self.label_media_geral.grid(row=0, column=1, sticky="w", padx=6)

        self.label_aprovados = ttk.Label(area, text="Aprovados: 0")
        self.label_aprovados.grid(row=0, column=2, sticky="w", padx=6)

        self.label_situacao = ttk.Label(area, text="Recuperação: 0 | Reprovados: 0")
        self.label_situacao.grid(row=0, column=3, sticky="w", padx=6)

    # ------------------------------------------------------------------
    # Ações de notas no formulário
    # ------------------------------------------------------------------
    def _on_adicionar_nota(self) -> None:
        ok, erro, nota = validacoes.validar_nota(self.entry_nota.get())
        if not ok:
            messagebox.showwarning("Nota inválida", erro)
            return
        self.notas_atuais.append(nota)
        self.listbox_notas.insert("end", f"{nota:.2f}")
        self.entry_nota.delete(0, "end")
        self.entry_nota.focus_set()
        self.alteracoes_pendentes = True

    def _on_remover_nota(self) -> None:
        selecionadas = self.listbox_notas.curselection()
        if not selecionadas:
            messagebox.showinfo("Remover nota", "Selecione uma nota na lista para remover.")
            return
        indice = selecionadas[0]
        self.listbox_notas.delete(indice)
        del self.notas_atuais[indice]
        self.alteracoes_pendentes = True

    # ------------------------------------------------------------------
    # Ações principais (CRUD)
    # ------------------------------------------------------------------
    def _on_salvar(self) -> None:
        nome = self.entry_nome.get()
        turma = self.combo_turma.get()

        ok, erro = validacoes.validar_nome(nome)
        if not ok:
            messagebox.showwarning("Dados inválidos", erro)
            return

        ok, erro = validacoes.validar_turma(turma)
        if not ok:
            messagebox.showwarning("Dados inválidos", erro)
            return

        ok, erro = validacoes.validar_notas_preenchidas(self.notas_atuais)
        if not ok:
            messagebox.showwarning("Dados inválidos", erro)
            return

        aluno = {
            "nome": nome.strip(),
            "turma": turma.strip(),
            "notas": list(self.notas_atuais),
        }

        if self.aluno_selecionado_id is None:
            self.alunos.append(aluno)
        else:
            self.alunos[self.aluno_selecionado_id] = aluno

        sucesso, erro = dados.salvar_alunos(self.alunos)
        if not sucesso:
            messagebox.showerror("Erro ao salvar", erro)
            return

        messagebox.showinfo("Sucesso", "Aluno salvo com sucesso.")
        self.alteracoes_pendentes = False
        self._on_limpar()
        self._atualizar_treeview()
        self._atualizar_resumo()

    def _on_excluir(self) -> None:
        if self.aluno_selecionado_id is None:
            messagebox.showinfo("Excluir", "Selecione um aluno na lista para excluir.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Tem certeza que deseja excluir este aluno? Essa ação não pode ser desfeita.",
        )
        if not confirmar:
            return

        del self.alunos[self.aluno_selecionado_id]
        sucesso, erro = dados.salvar_alunos(self.alunos)
        if not sucesso:
            messagebox.showerror("Erro ao salvar", erro)
            return

        messagebox.showinfo("Sucesso", "Aluno excluído com sucesso.")
        self.alteracoes_pendentes = False
        self._on_limpar()
        self._atualizar_treeview()
        self._atualizar_resumo()

    def _on_limpar(self) -> None:
        self.entry_nome.delete(0, "end")
        self.combo_turma.set("")
        self.entry_nota.delete(0, "end")
        self.listbox_notas.delete(0, "end")
        self.notas_atuais = []
        self.aluno_selecionado_id = None
        self.alteracoes_pendentes = False
        if self.treeview.selection():
            self.treeview.selection_remove(self.treeview.selection())

    def _on_selecionar_aluno(self, evento=None) -> None:
        selecionado = self.treeview.selection()
        if not selecionado:
            return
        indice = int(self.treeview.item(selecionado[0], "tags")[0])
        aluno = self.alunos[indice]

        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, aluno["nome"])
        self.combo_turma.set(aluno["turma"])
        self.listbox_notas.delete(0, "end")
        self.notas_atuais = list(aluno["notas"])
        for nota in self.notas_atuais:
            self.listbox_notas.insert("end", f"{nota:.2f}")

        self.aluno_selecionado_id = indice
        self.alteracoes_pendentes = False

    # ------------------------------------------------------------------
    # Atualização de Treeview / resumo
    # ------------------------------------------------------------------
    def _atualizar_treeview(self) -> None:
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        termo = self.entry_pesquisa.get().strip().lower()
        turmas = sorted({aluno["turma"] for aluno in self.alunos})
        self.combo_filtro_turma["values"] = ["Todas"] + turmas
        turma_filtro = self.combo_filtro_turma.get() or "Todas"

        for indice, aluno in enumerate(self.alunos):
            if termo and termo not in aluno["nome"].lower():
                continue
            if turma_filtro != "Todas" and aluno["turma"] != turma_filtro:
                continue

            media = validacoes.calcular_media(aluno["notas"])
            situacao = validacoes.calcular_situacao(media)
            self.treeview.insert(
                "",
                "end",
                values=(aluno["nome"], aluno["turma"], f"{media:.2f}", situacao),
                tags=(str(indice),),
            )

    def _atualizar_resumo(self) -> None:
        total = len(self.alunos)
        self.label_total.config(text=f"Total de alunos: {total}")

        if total == 0:
            self.label_media_geral.config(text="Média geral: -")
            self.label_aprovados.config(text="Aprovados: 0")
            self.label_situacao.config(text="Recuperação: 0 | Reprovados: 0")
            return

        medias = [validacoes.calcular_media(aluno["notas"]) for aluno in self.alunos]
        media_geral = round(sum(medias) / len(medias), 2)
        situacoes = [validacoes.calcular_situacao(media) for media in medias]

        aprovados = situacoes.count("Aprovado")
        recuperacao = situacoes.count("Recuperação")
        reprovados = situacoes.count("Reprovado")

        self.label_media_geral.config(text=f"Média geral: {media_geral:.2f}")
        self.label_aprovados.config(text=f"Aprovados: {aprovados}")
        self.label_situacao.config(
            text=f"Recuperação: {recuperacao} | Reprovados: {reprovados}"
        )

    # ------------------------------------------------------------------
    # Encerramento
    # ------------------------------------------------------------------
    def _ao_fechar(self) -> None:
        if self.alteracoes_pendentes:
            sair = messagebox.askyesno(
                "Sair",
                "Há alterações não salvas no formulário. Deseja realmente sair?",
            )
            if not sair:
                return
        self.root.destroy()
