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
            dbname: str = 'laika.db.json'
    ) -> None:
        """Inicializa ou conecta-se
        a um banco de dados.

        Se o banco de dados com o nome
        especificado em no argumento "filename"
        já existir, ele será usado, caso contrário,
        será criado.

        :param dbname: Nome do documento do banco de dados.
        (o padrão é "laika.db.json").
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
            raise FileNotFoundError('Arquivo do banco de dados não encontrado.')
        except json.JSONDecodeError:
            raise DBFileNotValid
        else:
            # verificando se os valores
            # existem
            try:
                is_valid = db_data['isValid']
                created_in = db_data['createdIn']
                last_update = db_data['lastUpdate']
                content = db_data['content']
            except KeyError:
                raise DBFileNotValid

            if not isinstance(content, dict):
                raise InvalidContentError

            return db_data

    def _save_db(self, db: dict) -> None:
        """Salva o banco de dados.

        :param db: Dicionário do banco de dados
        :return: None
        """

        try:
            time_now = str(datetime.now())
            db['lastUpdate'] = time_now

            with open(self.dbname, 'w') as db_file:
                json.dump(db, db_file,
                          indent=4, ensure_ascii=False)
        except FileNotFoundError:
            raise FileNotFoundError('Arquivo do banco de dados não encontrado.')

    def add_parent(self, name: str, content: dict) -> None:
        """Cria um novo objeto na raíz
        do banco de dados.

        Este objeto podem ser utilizados
        como "pai" para outros objetos.

        :return: None
        """

        db = self._open_db()
        db_content: dict = db.get('content')
        db_content[name] = content

        db['content'] = db_content
        self._save_db(db)

    def add_child(self, parent_name: str, child_name, content: dict) -> None:
        """Adiciona um novo filho ao objeto
        pai.

        Caso este objeto pai não exista,
        ele será criado.

        :param parent_name: Nome do objeto pai
        :param child_name: Nome do objeto filho
        :param content: Conteúdo do objeto filho
        :return: None
        """

        db = self._open_db()
        db_content: dict = db.get('content')

        if parent_name not in db_content:
            obj = {}
            obj[child_name] = content

            self.add_parent(parent_name, obj)
            return

        db_content[parent_name][child_name] = content
        db['content'] = db_content

        self._save_db(db)

    def get_parent(self, parent_name: str) -> [dict, None]:
        """Obtém um objeto "pai" com
        todos os seus filhos dentro.

        Se ele não existir, None é retornado.

        :param parent_name: Nome do objeto pai
        :return: Conteúdo do objeto pai ou None.
        """

        db = self._open_db()
        db_content = db.get('content')

        parent = db_content.get(parent_name)
        return parent

    def get_child(self, parent_name: str, child_name: str) -> [dict, None]:
        """Obtém um objeto filho de um
        objeto pai.

        Se ele não existir, None é retornado.

        :param parent_name: Nome o objeto pai.
        :param child_name: Nome do objeto filho
        :return: Conteúdo do objeto pai ou None.
        """

        db = self._open_db()
        db_content = db.get('content')

        parent = db_content.get(parent_name)

        if not parent:
            return None

        child = parent.get(child_name)
        return child


if __name__ == '__main__':
    db = LaikaDB()

    db.add_parent('meuObjeto', {})
    db.add_child('meuObjeto', 'filho', {})

    print(db.get_parent('meuObjeto'))
    print(db.get_child('meuObjeto', 'filho'))
