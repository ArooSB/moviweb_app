from flask import Flask, render_template, request, redirect, url_for, flash
from datamanager.sqlite_data_manager import SQLiteDataManager
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize SQLiteDataManager
db_path = 'instance/moviweb.db'
data_manager = SQLiteDataManager(db_path)

# OMDb API configuration
class MovieFetcher:
    API_URL = 'http://www.omdbapi.com/'
    API_KEY = 'b489c489'

    def fetch_movie(self, title):
        """
        Fetches movie details from the OMDb API based on the movie title.

        :param title: The title of the movie to fetch.
        :return: A dictionary with movie details if found, otherwise None.
        """
        response = requests.get(self.API_URL, params={"t": title, "apikey": self.API_KEY})
        if response.status_code == 200:
            data = response.json()
            if data['Response'] == 'True':
                return {
                    "title": data.get('Title'),
                    "director": data.get('Director'),
                    "year": data.get('Year'),
                    "rating": float(data.get('imdbRating', 0)),
                    "poster": data.get('Poster')
                }
        return None

fetcher = MovieFetcher()

@app.route('/')
def index():
    """
    Renders the list of all users.

    :return: Rendered template for users list.
    """
    return render_template('users_list.html', users=data_manager.get_all_users())

@app.route('/user/<int:user_id>/movies')
def user_movies(user_id):
    """
    Renders the movies for a specific user.

    :param user_id: The ID of the user whose movies are to be displayed.
    :return: Rendered template for user movies or a 404 error if the user is not found.
    """
    user = data_manager.get_user_by_id(user_id)
    if user:
        movies = data_manager.get_user_movies(user_id)
        return render_template('user_movies.html', user=user, movies=movies)
    else:
        return render_template('404.html'), 404

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Handles the addition of a new user.

    :return: Rendered template for adding a user or a redirect to the index if the user is added successfully.
    """
    if request.method == 'POST':
        name = request.form['name']
        if data_manager.add_user(name):
            flash('User added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Error adding user.', 'error')
    return render_template('add_user.html')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    """
    Handles the addition of a new movie.

    :return: Rendered template for adding a movie or a redirect to the user movies page if the movie is added successfully.
    """
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']
        user_id = request.form['user_id']

        # Fetch movie details from OMDb API using MovieFetcher
        movie_data = fetcher.fetch_movie(title)

        if movie_data:
            # Optionally override with user input
            title = movie_data.get('title', title)
            director = movie_data.get('director', director)
            year = movie_data.get('year', year)
            rating = movie_data.get('rating', rating)

            if data_manager.add_movie(user_id, title, director, year, rating):
                flash('Movie added successfully!', 'success')
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                flash('Error adding movie.', 'error')
        else:
            flash('Movie not found.', 'error')
    return render_template('add_movie.html', users=data_manager.get_all_users())

@app.route('/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(movie_id):
    """
    Handles the update of a movie's details.

    :param movie_id: The ID of the movie to be updated.
    :return: Rendered template for updating a movie or a redirect to the user movies page if the movie is updated successfully.
    """
    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        return render_template('404.html'), 404

    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']
        user_id = request.form['user_id']

        if data_manager.update_movie(movie_id, title, director, year, rating, user_id):
            flash('Movie updated successfully!', 'success')
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            flash('Error updating movie.', 'error')

    return render_template('update_movie.html', movie=movie, users=data_manager.get_all_users())

@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    """
    Handles the deletion of a movie.

    :param movie_id: The ID of the movie to be deleted.
    :return: Redirects to the user movies page or renders a 404 error if the movie is not found.
    """
    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        return render_template('404.html'), 404

    user_id = movie.user_id
    if data_manager.delete_movie(movie_id):
        flash('Movie deleted successfully!', 'success')
    else:
        flash('Error deleting movie.', 'error')

    return redirect(url_for('user_movies', user_id=user_id))

if __name__ == '__main__':
    app.run(debug=True)
