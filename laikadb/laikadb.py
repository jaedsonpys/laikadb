import json
import os

from datetime import datetime

from exceptions import DBFileNotValid
from exceptions import InvalidContentError

DEFAULT_DB_STRUCTURE = {'isValid': None,
                        'createdIn': None,
                        'lastUpdate': None,
                        'content': {}}


class LaikaDB:
    def __init__(
            self,
            dbname: str = 'laika.db'
    ) -> object:
        """Inicializa ou conecta-se
        a um banco de dados.

        Se o banco de dados com o nome
        especificado em no argumento "filename"
        já existir, ele será usado, caso contrário,
        será criado.

        :param dbname: Nome do documento do banco de dados.
        (o padrão é "laika.db").
        """

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

    def _create_db(self) -> None:
        time_now = str(datetime.now())
        db_dict: dict = DEFAULT_DB_STRUCTURE.copy()

        db_dict['createdIn'] = time_now
        db_dict['lastUpdate'] = time_now
        db_dict['isValid'] = True

        with open(self.dbname, 'w') as db:
            json.dump(db_dict, db, indent=4, ensure_ascii=False)

    def _open_db(self) -> dict:
        """Abre e retorna o conteúdo
        do banco de dados

        :return: Conteúdo do banco de dados
        """

        try:
            with open(self.dbname, 'r') as db:
                db_data = json.load(db)
        except FileNotFoundError:
            raise FileNotFoundError('DB file not found')
        except json.JSONDecodeError:
            raise DBFileNotValid
        else:
            is_valid = db_data.get('isValid')
            created_in = db_data.get('createdIn')
            last_update = db_data.get('lastUpdate')
            content = db_data.get('content')

            list_for_verify = [is_valid, created_in,
                               last_update, content]

            # verificando se os valores existem
            if not all(list_for_verify):
                raise DBFileNotValid

            if not isinstance(content, dict):
                raise InvalidContentError

            return db_data
