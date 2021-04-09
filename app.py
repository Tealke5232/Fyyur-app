#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from datetime import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
# TODO: connect to a local postgresql database   CHECK

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
migrate = Migrate(app, db)                                  #Flask-Migrade CHECK

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500), default="https://images.unsplash.com/photo-1529604278261-8bfcdb00a7b9?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1351&q=80")
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(250), nullable=True)
    shows = db.relationship('Show', backref='venue', cascade = 'all, delete-orphan', lazy = True)
    genres = db.Column(db.ARRAY(db.String))
    active_click = db.Column(db.Integer, default=0) #logs page hits to find trending

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120), nullable = True)
    website = db.Column(db.String(500), nullable = True)
    image_link = db.Column(db.String(500), default="https://images.unsplash.com/photo-1608723011854-24854fc61046?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=634&q=80")
    facebook_link = db.Column(db.String(120), nullable = True)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(250), nullable=True)
    genres = db.Column(db.ARRAY(db.String))
    shows = db.relationship('Show', backref='artist', cascade = 'all, delete-orphan', lazy=True)
    songs = db.relationship('Song', backref='artist', cascade = 'all, delete-orphan', lazy=True)
    active_click = db.Column(db.Integer, default=0) #logs page hits to find trending

class Song(db.Model):
    __tablename__ = 'Song'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable= False)
    release_date =  db.Column(db.DateTime(), nullable=False)
    description = db.Column(db.String(240), nullable=True)
    image_link = db.Column(db.String(500), default="https://cloud.netlifyusercontent.com/assets/344dbf88-fdf9-42bb-adb4-46f01eedd629/6d9b19ad-4701-4054-b692-3ca3c5a40b6c/gallows-belly-of-shark.jpg")
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    active_click = db.Column(db.Integer, default=0) #logs page hits to find trending

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    new_data = Artist.query.order_by(Artist.id.desc()).limit(6)             # put limit on 6
    hot_data =  Artist.query.order_by(Artist.active_click.desc()).limit(6)
    return render_template('pages/home.html', new_artists=new_data, hot_artists=hot_data)
    # index() is used throughout in order to call this function
    # when trying to redirect to home, better than having to add code
    # every time to call and collect newest artist data

#----------------------------------------------------------------------------#
# List of functionality ::
#----------------------------------------------------------------------------#
#   + Create Delete Update Search and Show venues
#   + Create Delete Update Search and Show artists
#   + Create and Show "Shows"
#   + Delete Shows when deleting either an artist
#     or venue involved with that show
#   + Display upcoming and past "Shows" inside
#     both the Venue's page and the Artist's page


#   ++ added songs functionaly, can only add, no U or D
#   ++ added a page hit counter for venue and artist
#   ++ added newest artest on homepage, newest shown first
#   ++ added Hottest artest on homepage, most active_click
#       shown first

#  Venues: Search and show
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    areas = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state).order_by('state').all()
    data = []
    for area in areas:
        venues = Venue.query.filter_by(state=area.state).filter_by(city=area.city).order_by('name').all()
        venue_data = []
        data.append({
            'city': area.city,
            'state': area.state,
            'venues': venue_data
        })
        for venue in venues:
            venue_data.append({
                'id': venue.id,
                'name': venue.name
            })
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term=request.form.get('search_term', '')
  data=Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  response={
    "count": data.count(),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    try:
        click_updater = Venue.query.get(venue_id)
        click_updater.active_click = click_updater.active_click + 1
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    venue = Venue.query.filter_by(id=venue_id).first_or_404()
    past_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time < str(datetime.now())
    ).all()
    upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time > str(datetime.now())
    ).all()

    data = {
        'id': venue.id,
        'name': venue.name,
        'city': venue.city,
        'state': venue.state,
        'address': venue.address,
        'phone': venue.phone,
        'image_link': venue.image_link,
        'facebook_link': venue.facebook_link,
        'wesbite': venue.website,
        'seeking_talent': venue.seeking_talent,
        'seeking_description': venue.seeking_description,
        'active_click': venue.active_click,
        'shows': venue.shows,
        'genres': venue.genres,
        'past_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        } for artist, show in past_shows],
        'upcoming_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        } for artist, show in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }
    return render_template('pages/show_venue.html', venue=data)

#  Venue: Create & Delete
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        facebook_link = request.form['facebook_link']
        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, facebook_link=facebook_link, genres=genres)
        db.session.add(venue)
        db.session.commit()
        flash('Venue, ' + request.form['name'] + ', was successfully listed!')
    except:
        db.session.rollback()
        error = True
        flash('Error during Submission, Venue was NOT successfully listed!')
    finally:
        db.session.close()
    if error:
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)
    else:
        return index()

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.filter_by(id=venue_id).one()
        db.session.delete(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        return index()

#  Artists: Search and Show
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data=Artist.query.order_by('name').all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term=request.form.get('search_term', '')
  data=Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  response={
    "count": data.count(),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    try:
        click_updater = Artist.query.get(artist_id)
        click_updater.active_click = click_updater.active_click + 1
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    artist = Artist.query.filter_by(id=artist_id).first_or_404()
    past_shows = db.session.query(Venue, Show).join(Show).join(Artist).filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time < str(datetime.now())
    ).all()
    upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist).filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time > str(datetime.now())
    ).all()

    data = {
        'id': artist.id,
        'name': artist.name,
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'image_link': artist.image_link,
        'facebook_link': artist.facebook_link,
        'wesbite': artist.website,
        'seeking_venue': artist.seeking_venue,
        'seeking_description': artist.seeking_description,
        'shows': artist.shows,
        'songs': artist.songs,
        'active_click': artist.active_click,
        'genres': artist.genres,
        'past_shows': [{
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time
        } for venue, show in past_shows],
        'upcoming_shows': [{
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time
        } for venue, show in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }
    return render_template('pages/show_artist.html', artist=data)


#  Venue/Arists: Update
#  ----------------------------------------------------------------
#

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  try:
      artist=Artist.query.get(artist_id)
  except:
      return render_template('errors/404.html'), 404
  finally:
      return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
 error = False
 try:
     artist = Artist.query.get(artist_id)   # regulated by the form, never is empty
     artist.name = request.form['name']
     artist.city = request.form['city']
     artist.state = request.form['state']
     artist.phone = request.form['phone']
     genres = request.form['genres']

     website = request.form['website']      # allowed to be empty by form
     if website != '':                      # do these if statements to preserve old
         artist.website = website           # data during testing
     facebook_link = request.form['facebook_link']
     if facebook_link != '':
         artist.facebook_link = facebook_link
     image_link = request.form['image_link']
     if image_link != '':
         artist.image_link = image_link

     if 'seeking_venue' not in request.form:    # if not true nothing gets returend
         artist.seeking_venue = False           # so just check if returned
     else:
         artist.seeking_venue = True
     seeking_description = request.form['seeking_description']
     if seeking_description != '':
         artist.seeking_description = seeking_description

     db.session.commit()
     flash('Artist, ' + request.form['name'] + ', was successfully Updated!')
 except:                                         # error handler
     db.session.rollback()                         # defaults to a rollback
     error = True
     flash('Error during Submission, Artist was NOT successfully Updated!')
 finally:
     db.session.close()
 if error:
     form = ArtistForm()
     artist = Artist.query.get(artist_id)
     return render_template('forms/edit_artist.html', form=form, artist=artist)
 else:
     return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  try:
      venue=Venue.query.get(venue_id)
  except:
      return render_template('errors/404.html'), 404
  finally:
      return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:
      venue = Venue.query.get(venue_id)             # reference artist: edit POST comments
                                                    # for explanation on format
      venue.name = request.form['name']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.address = request.form['address']
      venue.phone = request.form['phone']
      genres = request.form['genres']

      website = request.form['website']
      if website != '':
          venue.website = website
      facebook_link = request.form['facebook_link']
      if facebook_link != '':
          venue.facebook_link = facebook_link
      image_link = request.form['image_link']
      if image_link != '':
          venue.image_link = image_link

      if 'seeking_talent' not in request.form:
          venue.seeking_talent = False
      else:
          venue.seeking_talent = True
      seeking_description = request.form['seeking_description']
      if seeking_description != '':
          venue.seeking_description = seeking_description

      db.session.commit()
      flash('Venue, ' + request.form['name'] + ', was successfully Updated!')
  except:
      db.session.rollback()
      error = True
      flash('Error during Submission, Venue was NOT successfully Updated!')
  finally:
      db.session.close()
  if error:
      form = VenueForm()
      venue = Venue.query.get(venue_id)
      return render_template('forms/edit_venue.html', form=form, venue=venue)
  else:
      return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist and delete
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        facebook_link = request.form['facebook_link']
        artist = Artist(name=name, city=city, state=state, phone=phone, facebook_link=facebook_link, genres=genres)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
        flash('Error during Submission, Artist was NOT successfully listed!')
    finally:
        db.session.close()
    if error:
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)
    else:
        return index()

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    error = False
    try:
        artist = Artist.query.filter_by(id=artist_id).one()
        db.session.delete(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        return index() #I use index() to avoid having to call artist data from here
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.order_by('start_time').all()
  data = []
  for show in shows:
      data.append({
        "venue_id": show.venue_id,
        "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
        "artist_id": show.artist_id,
        "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
        "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
        "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    try:
        artist_id=request.form['artist_id']
        venue_id=request.form['venue_id']
        start_time=request.form['start_time']
        show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed! See you at '+start_time)
    except:
        db.session.rollback()
        error = True
        flash('Error durring submission, show not added')
    finally:
        db.session.close()
    if error:
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)
    else:
        return index()

#  Add Songs
#  ----------------------------------------------------------------
@app.route('/songs/<int:artist_id>/add')
def add_song(artist_id):
    form = SongForm()
    return render_template('forms/new_song.html', form=form, artist_id=artist_id)

@app.route('/songs/<int:artist_id>/add', methods=['POST'])
def add_song_submission(artist_id):
    error = False
    try:
        name = request.form['name']
        description = request.form['description']
        release_date = request.form['release_date']
        #image_link = request.form['image_link']      # turned image link off for now so the default always shows
        song = Song(artist_id=artist_id, name=name, description=description, release_date=release_date) #image_link=image_link)
        db.session.add(song)
        db.session.commit()
        flash('Song successfuly added')
    except:
        db.session.rollback()
        error = True
        flash('error Durring submission, song not added')
    finally:
        db.session.close()
    if error:
        form = SongForm()
        return render_template('forms/new_song.html', form=form, artist_id=artist_id)
    else:
        return index()#show_artist(artist_id)




    form = SongForm()
    return render_template('forms/new_song.html', form=form, artist_id=artist_id)

#  error Handlers
#  ----------------------------------------------------------------
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
# Todolist
#Updates
#deletes
#add update and delete buttons
