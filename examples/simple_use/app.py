from laikadb import LaikaDB

db = LaikaDB()

# mostra a data da última atualização
print(db.get_last_update())

user_data = {'email': 'test@python.org',
             'age': 15}

db.add_parent('users', {})
db.add_child('users', 'Jaedson', content=user_data)
