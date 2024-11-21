#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ save user to database
        """
        test_user = User(email=email, hashed_password=hashed_password)
        self._session.add(test_user)
        self._session.commit()

        return test_user

    def find_user_by(self, **kwargs) -> User:
        """Find user by arbitrary input data arg"""
        for key in kwargs:
            if key == 'email':
                user = self._session.query(User)\
                    .filter_by(email=kwargs[key])\
                    .first()
            elif key == 'id':
                user = self._session.query(User)\
                  .filter_by(id=kwargs[key])\
                  .first()
            else:
                raise InvalidRequestError

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: str, **kwargs) -> None:
        """Update user info"""
        for key in kwargs:
            user = self.find_user_by(id=user_id)
            if key == 'hashed_password':
                user.hashed_password = kwargs['hashed_password']
            elif key == 'email':
                user.email = kwargs['email']
            else:
                raise ValueError
        self._session.commit()

        return None
