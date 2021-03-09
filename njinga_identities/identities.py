from os import getenv
from json import dumps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from njinga_identities.models import Base, Model


class Identity:
    """
    Settings for authorization.
    Initialize dataself.__base and authorize user.
    """
    __engine = create_engine(
        getenv(
            'SQL_URL'
        ) if getenv(
            'SQL_URL'
        ) else 'sqlite:///njinga_identities.sqlite'
    )
    __Session = sessionmaker(bind=__engine)
    __session = __Session()
    __base = Base

    def __init__(
        self: object
    ) -> str:
        self.logged = False

    @property
    def create_tables(
        self: object
    ):
        self.__base.metadata.create_all(
            self.__engine,
            tables=[Model],
            checkfirst=True
        )

    def create_user(
        self: object,
        username: str,
        password: str,
        email: str
    ) -> bool:
        try:
            self.__session.add(
                Model(
                    username=username,
                    password=self.__secret.generate(
                        password
                    ),
                    email=email
                )
            )
            self.__session.commit()
        except IntegrityError:
            raise IntegrityError('Username or email exists.')
        return True

    def __get_user(
        self: object,
        username: str
    ) -> Model:
        return self.__session.query(
            Model
        ).filter(
            Model.username == username
        ).first()

    @property
    def show_users(
        self: object
    ) -> dumps:
        users = []
        [
            users.append(
                {
                    'username': instance.username,
                    'email': instance.email,
                    'enabled': instance.enabled
                }
            ) for instance in self.__session.query(
                Model
            ).order_by(
                Model.username
            )
        ]
        return dumps(users)

    def change_password(
        self: object,
        username: str,
        password: str
    ) -> None:
        user = self.return_user(username)
        user.password = password
        self.__session.commit()

    def change_email(
        self: object,
        username: str,
        email: str
    ) -> None:
        user = self.return_user(username)
        user.email = email
        self.__session.commit()

    def enable_user(
        self: object,
        username: str,
        enabled: bool = False
    ) -> bool:
        user = self.return_user(username)
        user.enabled = enabled
        self.__session.commit()

    def __repr__(
        self: object
    ) -> str:
        return dumps(
            {
                'logged': self.logged
            }
        )
