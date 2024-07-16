from models import db, User


def init_db():
    db.connect()
    db.create_tables([User])


def add_user(name, age):
    user = User(name=name, age=age)
    user.save()


def get_users():
    return User.select()


if __name__ == '__main__':
    init_db()

    # Adding users
    add_user('Alice', 30)
    add_user('Bob', 25)

    # Fetching and displaying users
    users = get_users()
    for user in users:
        print(f'User {user.id}: {user.name}, {user.age} years old')
