# 🌾 Brain Backend

API RESTful desenvolvida com **Django** e **Django REST Framework** para cadastro e gerenciamento de **produtores rurais**, **fazendas**, **safras** e **culturas**. A aplicação foi construída com foco em operações CRUD e validações específicas de domínio.

---

## 🛠️ Funcionalidades

- Cadastro de **Produtores** com validação de CPF ou CNPJ.
- Cadastro de **Fazendas** com validação da soma das áreas agricultável e de vegetação.
- Cadastro de **Safras** e **Culturas** vinculadas a fazendas.
- Relações entre os modelos com serialização aninhada.
- Documentação interativa via Swagger.
- Deploy local com **Docker + PostgreSQL**.
- Acesso ao painel de administração do Django.

---

## 🧱 Tecnologias

- Python 3.10+
- Django 4.x
- Django REST Framework
- drf-spectacular (Swagger/OpenAPI)
- PostgreSQL
- Docker & Docker Compose

---

## ▶️ Como rodar o projeto com Docker

> Pré-requisitos: [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) instalados.
> docker compose up --build

## Acesse a API e a documentação:

- 🌐 Swagger local: http://localhost:8000/swagger/

## 🌍 API em produção

- A API está publicada no Render:

- https://brain-backend-5jqv.onrender.com/swagger/

## ✅ Validações implementadas

- CPF/CNPJ – validado no backend usando full_clean() com tratamento de formatos e integridade.

- Áreas de fazenda:

- A soma de área agricultável e vegetação não pode ultrapassar a área total.

- Safras únicas – um ano de safra só pode ser cadastrado uma vez.

- Culturas duplicadas – impede registros duplicados de mesma cultura por fazenda e safra.
