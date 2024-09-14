from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from data_manager_interface import DataManagerInterface

Base = declarative_base()

class User(Base):
    """
    Represents a user in the database.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    movies = relationship('Movie', backref='user')

class Movie(Base):
    """
    Represents a movie in the database.
    """
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

class SQLiteDataManager(DataManagerInterface):
    """
    Manages data interactions with an SQLite database using SQLAlchemy.
    """
    def __init__(self, db_path):
        """
        Initializes the SQLiteDataManager with the given database path.

        :param db_path: Path to the SQLite database file.
        """
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_all_users(self):
        """
        Retrieves all users from the database.

        :return: A list of User objects.
        """
        session = self.Session()
        users = session.query(User).all()
        session.close()
        return users

    def get_user_by_id(self, user_id):
        """
        Retrieves a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :return: A User object if found, otherwise None.
        """
        session = self.Session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        return user

    def get_user_movies(self, user_id):
        """
        Retrieves all movies for a specific user.

        :param user_id: The ID of the user whose movies to retrieve.
        :return: A list of Movie objects associated with the user.
        """
        session = self.Session()
        movies = session.query(Movie).filter_by(user_id=user_id).all()
        session.close()
        return movies

    def add_user(self, name):
        """
        Adds a new user to the database.

        :param name: The name of the user to add.
        :return: True if the user was added successfully, otherwise False.
        """
        session = self.Session()
        try:
            new_user = User(name=name)
            session.add(new_user)
            session.commit()
            return True
        except:
            session.rollback()
            return False
        finally:
            session.close()

    def add_movie(self, user_id, title, director, year, rating):
        """
        Adds a new movie to the database.

        :param user_id: The ID of the user associated with the movie.
        :param title: The title of the movie.
        :param director: The director of the movie.
        :param year: The release year of the movie.
        :param rating: The rating of the movie.
        :return: True if the movie was added successfully, otherwise False.
        """
        session = self.Session()
        try:
            new_movie = Movie(user_id=user_id, title=title, director=director, year=year, rating=rating)
            session.add(new_movie)
            session.commit()
            return True
        except:
            session.rollback()
            return False
        finally:
            session.close()

    def update_movie(self, movie_id, title, director, year, rating, user_id):
        """
        Updates the details of an existing movie.

        :param movie_id: The ID of the movie to update.
        :param title: The new title of the movie.
        :param director: The new director of the movie.
        :param year: The new release year of the movie.
        :param rating: The new rating of the movie.
        :param user_id: The new user ID associated with the movie.
        :return: True if the movie was updated successfully, otherwise False.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                movie.title = title
                movie.director = director
                movie.year = year
                movie.rating = rating
                movie.user_id = user_id
                session.commit()
                return True
            return False
        except:
            session.rollback()
            return False
        finally:
            session.close()

    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database.

        :param movie_id: The ID of the movie to delete.
        :return: True if the movie was deleted successfully, otherwise False.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                session.delete(movie)
                session.commit()
                return True
            return False
        except:
            session.rollback()
            return False
        finally:
            session.close()
