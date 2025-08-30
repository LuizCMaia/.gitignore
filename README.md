# 📝 Agenda de Tarefas Desktop com Python

Uma aplicação de desktop simples e funcional para gerenciamento de tarefas, desenvolvida inteiramente em Python utilizando a biblioteca Flet para a interface gráfica e SQLite para o banco de dados.

## ✨ Funcionalidades

- **Cadastro Completo de Tarefas:** Adicione tarefas com nome, descrição, tipo, data de início e data final.
- **Gerenciamento de Status:** Marque tarefas como "Feito" ou "Não Feito".
- **Busca Dinâmica:** Filtre tarefas em tempo real digitando no campo de busca (busca por nome ou descrição).
- **Interface Intuitiva:** Separação clara entre tarefas pendentes e concluídas.
- **Regras de Negócio:** Tarefas concluídas não podem ser apagadas, garantindo a integridade do histórico.

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python
- **Interface Gráfica:** Flet (Flutter para Python)
- **Banco de Dados:** SQLite 3 (embutido no Python)

## ⚙️ Como Executar o Projeto

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
    cd SEU_REPOSITORIO
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    venv\Scripts\activate     # No Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicialize o Banco de Dados (apenas na primeira vez):**
    ```bash
    python database.py
    ```

5.  **Execute a aplicação:**
    ```bash
    python main.py
    ```
