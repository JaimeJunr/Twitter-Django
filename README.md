### 🐧 Twitter Django

## 📌 Sobre o Projeto

O **Twitter Django** é uma aplicação web que replica as principais funcionalidades do Twitter, permitindo que os usuários publiquem tweets, sigam outros usuários e interajam com conteúdos na plataforma.
construído com Django, Bootstrap e JavaScript. Ele permite que os usuários criem tweets, retuitem, curtam e deletem tweets, além de visualizar perfis de outros usuários.

## 🚀 Tecnologias Utilizadas

Este projeto foi desenvolvido com as seguintes tecnologias:

- **Backend:** Django + Django REST Framework
- **Frontend:** Django Templates + JavaScript
- **Banco de Dados:** SQLite
- **Autenticação:** Django Auth
- **Estilização:** Bootstrap
- **Deploy:** PythonAnywhere
- **Django:** Framework web Python para o backend.
- **Bootstrap:** Framework CSS para o frontend.
- **JavaScript:** Para interatividade no frontend.
- **HTML/CSS:** Para a estrutura e estilo das páginas.
- **Font Awesome:** Para ícones.

## 🐜 Funcionalidades

✔ Criar conta e fazer login/logout  
✔ Publicar e excluir tweets  
✔ Seguir e deixar de seguir usuários  
✔ Curtir e comentar tweets  
✔ Buscar tweets e perfis

- **Criação de Tweets:** Os usuários podem criar novos tweets com conteúdo textual.
- **Retweets:** Os usuários podem retweetar tweets existentes, com a opção de adicionar um comentário.
- **Curtidas:** Os usuários podem curtir tweets, e o número de curtidas é exibido.
- **Deleção de Tweets:** Os usuários podem deletar seus próprios tweets.
- **Visualização de Perfis:** Os usuários podem visualizar os perfis de outros usuários e seus tweets.
- **Paginação:** A lista de tweets é paginada para melhorar o desempenho.
- **Modal de Retweet:** Um modal Bootstrap é usado para confirmar e adicionar comentários aos retweets.
- **Interatividade com JavaScript:** As funcionalidades de curtir, retweetar e deletar tweets são implementadas com JavaScript para melhorar a experiência do usuário.

## ⚙️ Como Rodar o Projeto

### 💻 Requisitos

- **Python 3.9+**
- **Poetry** (para gerenciar dependências)

### 🛠 Passos para Execução

1. Clone o repositório:

   ```sh
   git clone https://github.com/JaimeJunr/twitterclone.git
   cd twitterclone
   ```

2. Instale as dependências com Poetry:

   ```sh
   poetry install
   ```

3. Realize as migrações do banco de dados:

   ```sh
   poetry run python manage.py migrate
   ```

4. Crie um superusuário para acessar o painel de administração:

   ```bash
   python manage.py createsuperuser
   ```

5. Inicie o servidor:

   ```sh
   poetry run python manage.py runserver
   ```

6. Acesse o aplicativo via `http://127.0.0.1:8000/`

## 💒 Estrutura do Projeto

```bash
/twitter-clone
├── app/               # API e backend Django
│   ├── manage.py      # Arquivo principal do Django
│   ├── twitterclone/ # Configuração do projeto
│   ├── templates/     # HTML + Django Templates
│   ├── staticfiles/        # Arquivos CSS e JS
│   ├── media/ # Imagens
│   ├── db.sqlite3 # Banco de Dados
│   ├── user/         # Aplicação para gerenciamento dos objetos, como usuarios, tweets, etc.
│   └── ...
└── README.md
```

## 🛠 Contribuindo

Se você deseja contribuir para o **Twitter Clone**, siga estes passos:

1. Faça um fork do repositório
2. Crie um branch para a sua feature (`git checkout -b minha-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adicionando minha feature'`)
4. Envie para o repositório remoto (`git push origin minha-feature`)
5. Abra um **Pull Request**

## 📝 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

💻 **Desenvolvido por [Jaime Junr](https://github.com/JaimeJunr) 🚀**
