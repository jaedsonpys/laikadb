# LaikaDB

![BADGE](https://img.shields.io/static/v1?label=status&message=em%20desenvolvimento&color=orange?style=status&logo=appveyor)
![BADGE](https://img.shields.io/static/v1?label=linguagem&message=Python&color=white?style=status&logo=python)

LaikaDB é um banco de dados noSQL para uso local e simples, onde você pode realizar gravações e leituras de forma eficiente e simples. Todos os dados ficam guardados em um arquivo JSON.

Com arquivos JSON, você pode movimentar seu banco de dados e ter diversas cópias dele guardadas como backup. Você pode utilizar um banco de dados existente ou criar um novo diretamente com o LaikaDB.

## Guia

- [Como usar](#Como-usar)
  - [Criando um objeto pai](#Criando-um-objeto-pai)
  - [Adicionando um objeto filho](#Adicionando-um-objeto-filho)
- [Licença](#Licença)

# Como usar

Para usar o LaikaDB, é necessário primeiramente baixar o código-fonte. Crie um diretório na pasta raíz ou na pasta ```laikadb/examples``` para fazer seu primeiro uso.

## Criando um objeto pai

Vamos começar com um exemplo básico, criando um objeto pai simples:

```python
from laikadb import LaikaDB

db = LaikaDB()
db.add_parent('meuObjeto', {})
```

Pronto, após isso, um arquivo ```laika.db.json``` será criado em seu diretório e lá contém todas as informações necessárias para o funcionamento do LaikaDB.

> Objetos "pai" sempre estarão na raíz do banco de dados
