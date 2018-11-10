# Star Wars API da B2W [![Build Status](https://travis-ci.com/diegosperes/bchallenge.svg?branch=master)](https://travis-ci.com/diegosperes/bchallenge)

Para realizar o setup do projeto é bem simple, baster ter o docker ou uma instancia do mongodb rodando em sua maquina.

    docker:
        - make build
        - make migrations
        - make run-prod

    sem o docker:
        - make setup
        - make migrations
        - make run

Uma das vantagens de utilizar o docker é que possui o nginx realizando o proxy das requisições para a aplicação, além de não existir a necessidade de instalar o mongodb nem o virtualenv - tudo isolado :)

Esse projeto utilizou recursos do mongodb 4, caso algo não funcione check se o ambiente está direitinho!

Como utilizar a api:

    Nginx -> http://localhost:8080
    App -> http://localhost:8000

    Busca por nome:
        (GET) http://localhost:8080/planet?name=IV
        (GET) http://localhost:8080/movie?name=sith

    Busca por id:
        (GET) http://localhost:8080/planet/{id}
        (GET) http://localhost:8080/movie/{id}

    Lista:
        (GET) http://localhost:8080/planet/
        (GET) http://localhost:8080/movie/

    Inserção:
        (POST) http://localhost:8080/planet
        (POST) http://localhost:8080/movie

    Update:
        (POST) http://localhost:8080/planet/{id}
        (POST) http://localhost:8080/movie/{id}

    Delete:
        (DELETE) http://localhost:8080/planet/{id}
        (DELETE) http://localhost:8080/movie/{id}

## O que poderia ser evoluído
Com o nginx na frente da aplicação é possível inserir uma camada de autenticação, verificando se o usuário está autorizado a inserir, atualizar e deletar os dados. HTTP2?
Poderia no futuro utilizar o memcached ou redis como camada de cache para guardar os dados vindo do mongodb, existe diversos benefícios um deles é a resiliência.
Foi criado um indice no mongo para realizar a busca por nome, infelizmente o banco de dados não suporta fuzzy queries como o elasticsearch.

## Como rodar os testes
    make tests

## OBS
Existe um banco de dados para os testes e um para aplicação.
A execução do make migrations irá popular o banco de dados e criar os indexes de busca.
A requisitar um planet por id, os dados serão agregados aos relativos na coleção movie.
