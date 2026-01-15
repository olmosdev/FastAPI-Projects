from operations import add_user
from models import User, Role


def test_add_user_into_the_database(session):
    user = add_user(
        session=session,
        username="sheldonsonny",
        password="difficultpassword",
        email="sheldonsonny@email.com",
    )

    assert (
        session.query(User)
        .filter(User.id == user.id)
        .first()
        == user
    )