### 🐧 Twitter Clone  

![Twitter Clone](https://via.placeholder.com/800x400.png?text=Twitter+Clone+Logo)  

## 📌 Sobre o Projeto  

O **Twitter Clone** é uma aplicação web que replica as principais funcionalidades do Twitter, permitindo que os usuários publiquem tweets, sigam outros usuários e interajam com conteúdos na plataforma.  

## 🚀 Tecnologias Utilizadas  

Este projeto foi desenvolvido com as seguintes tecnologias:  

- **Backend:** Django + Django REST Framework  
- **Frontend:** Django Templates + JavaScript  
- **Banco de Dados:** SQLite  
- **Autenticação:** Django Auth  
- **Estilização:** Bootstrap  
- **Deploy:** PythonAnywhere  

## 🐜 Funcionalidades  

✔ Criar conta e fazer login/logout  
✔ Publicar, editar e excluir tweets  
✔ Seguir e deixar de seguir usuários  
✔ Curtir e comentar tweets  
✔ Notificações em tempo real  
✔ Buscar tweets e perfis  

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

4. Inicie o servidor:  
   ```sh
   poetry run python manage.py runserver
   ```

5. Acesse o aplicativo via `http://127.0.0.1:8000/`  

## 💒 Estrutura do Projeto  

```bash
/twitter-clone
├── app/               # API e backend Django
│   ├── manage.py      # Arquivo principal do Django
│   ├── twitter_clone/ # Configuração do projeto
│   ├── users/         # Aplicação para gerenciamento de usuários
│   ├── tweets/        # Aplicação para funcionalidades de tweets
│   ├── templates/     # HTML + Django Templates
│   ├── static/        # Arquivos CSS, JS e imagens
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

