
import flet as ft
import sqlite3
from datetime import datetime

DB_FILE = "agenda.db"

def main(page: ft.Page):
    page.title = "Minha Agenda de Tarefas"
    page.window_width = 900
    page.window_height = 850
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    card_bgcolor = ft.Colors.WHITE70

 
    def db_execute(query, params=()):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def db_query_all(query, params=()):
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]


    nome_tarefa = ft.TextField(label="Nome da tarefa...", expand=True)
    descricao_tarefa = ft.TextField(label="Descrição...", expand=True)
    tipo_tarefa = ft.TextField(label="Tipo (Ex: Trabalho)", expand=True)

    data_inicio_texto = ft.TextField(label="Data Início", hint_text="DD/MM/AAAA", width=150)
    data_final_texto = ft.TextField(label="Data Final", hint_text="DD/MM/AAAA", width=150)
    
    tarefas_pendentes_col = ft.Column(spacing=10)
    tarefas_concluidas_col = ft.Column(spacing=10)

   
    def renderizar_tarefas(search_term=None):
        tarefas_pendentes_col.controls.clear()
        tarefas_concluidas_col.controls.clear()

        query = "SELECT * FROM tarefas"
        params = []
        if search_term:
            query += " WHERE nome LIKE ? OR descricao LIKE ?"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        query += " ORDER BY id DESC"

        tarefas = db_query_all(query, params)
        
        for tarefa in tarefas:
            botoes_card = [
                ft.TextButton(
                    text="Marcar Feito" if tarefa['status'] == 'pendente' else "Não Feito",
                    icon=ft.Icons.DONE if tarefa['status'] == 'pendente' else ft.Icons.UNDO,
                    on_click=lambda e, t_id=tarefa['id'], t_status=tarefa['status']: atualizar_status_clique(t_id, t_status)
                )
            ]
            
            if tarefa['status'] == 'pendente':
                botoes_card.append(
                    ft.TextButton(
                        text="Deletar", 
                        icon=ft.Icons.DELETE, 
                        icon_color=ft.Colors.RED,
                        on_click=lambda e, t_id=tarefa['id']: deletar_clique(t_id)
                    )
                )

            card_tarefa = ft.Card(
                ft.Container(
                    ft.Column([
                        ft.ListTile(
                            title=ft.Text(tarefa['nome'], weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(tarefa['descricao']),
                        ),
                        ft.Row([
                            ft.Text(f"Tipo: {tarefa['tipo_tarefa'] or 'N/D'}", size=12, italic=True),
                            ft.Text(f"Início: {tarefa['data_inicio'] or 'N/A'}", size=12, italic=True),
                            ft.Text(f"Fim: {tarefa['data_final'] or 'N/A'}", size=12, italic=True),
                        ], spacing=15),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=botoes_card
                        )
                    ]),
                    padding=10
                )
            )
            if tarefa['status'] == 'pendente':
                tarefas_pendentes_col.controls.append(card_tarefa)
            else:
                tarefas_concluidas_col.controls.append(card_tarefa)
        
        page.update()

    def adicionar_clique(e):
        if not nome_tarefa.value:
            return
        
        db_execute(
            "INSERT INTO tarefas (nome, descricao, tipo_tarefa, data_inicio, data_final) VALUES (?, ?, ?, ?, ?)",
            (nome_tarefa.value, descricao_tarefa.value, tipo_tarefa.value, data_inicio_texto.value, data_final_texto.value)
        )
        nome_tarefa.value, descricao_tarefa.value, tipo_tarefa.value = "", "", ""
        data_inicio_texto.value, data_final_texto.value = "", ""
        
        renderizar_tarefas()

    def deletar_clique(tarefa_id):
        db_execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        renderizar_tarefas()

    def atualizar_status_clique(tarefa_id, status_atual):
        novo_status = 'conclida' if status_atual == 'pendente' else 'pendente'
        db_execute("UPDATE tarefas SET status = ? WHERE id = ?", (novo_status, tarefa_id))
        renderizar_tarefas()

    def on_search_change(e):
        renderizar_tarefas(search_term=e.control.value)

    campo_busca = ft.TextField(
        label="Buscar por nome ou descrição...",
        on_change=on_search_change,
        prefix_icon=ft.Icons.SEARCH
    )

    
    bg_image = ft.Image(
        src="tarefas.png",
      
        fit=ft.ImageFit.COVER,
        repeat=ft.ImageRepeat.NO_REPEAT,
        opacity=1,
        expand=True
    )

    painel_conteudo = ft.Container(
        width=700,
        padding=25,
        border_radius=ft.border_radius.all(10),
        bgcolor=card_bgcolor,
        content=ft.Column(
            [
                ft.Text("Minha Agenda de Tarefas", size=30, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                campo_busca,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Column([
                    ft.Row([nome_tarefa, descricao_tarefa, tipo_tarefa], spacing=10),
                    ft.Row([data_inicio_texto, data_final_texto], alignment=ft.MainAxisAlignment.START, spacing=10),
                    ft.ElevatedButton("Adicionar Tarefa", on_click=adicionar_clique, icon=ft.Icons.ADD),
                ], spacing=10),
                ft.Divider(height=20),
                ft.Text("Tarefas Pendentes", size=20),
                tarefas_pendentes_col,
                ft.Divider(height=20),
                ft.Text("Tarefas Concluídas", size=20),
                tarefas_concluidas_col,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=15
        )
    )

    page.add(
        ft.Stack(
            controls=[
              
                ft.Container(
                    expand=True,
                    content=bg_image,
                  
                ),
                ft.Row(
                    controls=[
                        painel_conteudo
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    expand=True
                )
            ],
            expand=True
        )
    )

    renderizar_tarefas()

ft.app(target=main)
