import json
import os

from datetime import datetime

DEFAULT_DB_STRUCTURE = {'isValid': None,
                        'createdIn': None,
                        'lastUpdate': None,
                        'content': {}}


class LaikaDB:
    def __init__(
            self,
            dbname: str = 'laika.db',
            cryptography: bool = True
    ) -> object:
        """Inicializa ou conecta-se
        a um banco de dados.

        Se o banco de dados com o nome
        especificado em no argumento "filename"
        já existir, ele será usado, caso contrário,
        será criado.

        :param dbname: Nome do documento do banco de dados.
        (o padrão é "laika.db").

        :param cryptography: True para ativar a criptografia
        e False para desativar.
        """

        # criar método para criptografar dados

        self.cryptography = cryptography
        self.dbname = dbname

        self._initialize()

    def _initialize(self) -> None:
        # verificando se o banco de dados
        # especificado já existe

        already_exists = os.path.isfile(self.dbname)
        if not already_exists:
            # se não existir, será criado
            # com o nome que está armazenado em
            # self.dbname

            return self._create_db()

        self._open_db()

    def _create_db(self) -> None:
        time_now = str(datetime.now())
        db_dict: dict = DEFAULT_DB_STRUCTURE.copy()

        db_dict['createdIn'] = time_now
        db_dict['lastUpdate'] = time_now
        db_dict['isValid'] = True

        with open(self.dbname, 'w') as db:
            json.dump(db_dict, db, indent=4, ensure_ascii=False)

