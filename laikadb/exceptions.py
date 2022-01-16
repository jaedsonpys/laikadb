# Copyright © 2022 - Firlast
#
# LaikaDB, desenvolvido pela Firlast.
# Este projeto é open-source, siga as
# instruções da licença.

class Base(Exception):
    pass


class DBFileNotValid(Base):
    def __init__(self):
        super().__init__('Arquivo de banco de dados inválido')


class InvalidContentError(Base):
    def __init__(self):
        super().__init__('Conteúdo do banco de dados inválido')
