#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)


# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String()),nullable=True, default='{}')
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=True, default='')
    website = db.Column(db.String(250),nullable=True,default='')
    shows = db.relationship('Show', backref='Venue', lazy=True)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()),nullable=True, default='{}')
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(250),nullable=True,default='')
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=True, default='')
    shows = db.relationship('Show', backref='Artist', lazy=True)



# TODO: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.all()
  data = Venue.query.distinct('city', 'state').order_by('state').all()
  return render_template('pages/venues.html', areas=data ,venues=venues)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term +'%')).all()
  venues_count = Venue.query.filter(Venue.name.ilike('%' + search_term +'%')).count()
  response = {
    "count": venues_count,
    "data": []
  }
  for venue in venues:
    response['data'].append({
      "id": venue.id,
      "name": venue.name
    })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  shows = Show.query.filter_by(venue_id=venue_id).all()
  
  data = {
    "id": venue.id,
    "name": venue.name,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "image_link": venue.image_link,
    "facebook_link": venue.facebook_link,
    "genres": venue.genres,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "website": venue.website,   
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }

  past_shows_count = 0
  upcoming_shows_count = 0
  
  for show in shows:
    if show.start_time < datetime.now():
      artist_info = Artist.query.filter_by(id=show.artist_id).first()
      data['past_shows'].append({
        "artist_id": artist_info.id,
        "artist_name": artist_info.name,
        "artist_image_link": artist_info.image_link,
        "start_time": format_datetime(str(show.start_time))
      })
      past_shows_count += 1
      data['past_shows_count'] = past_shows_count

  for show in shows:
    if show.start_time > datetime.now():
      artist_info = Artist.query.filter_by(id=show.artist_id).first()
      data['upcoming_shows'].append({
        "artist_id": artist_info.id,
        "artist_name": artist_info.name,
        "artist_image_link": artist_info.image_link,
        "start_time": format_datetime(str(show.start_time))
      }) 
      upcoming_shows_count += 1
      data['upcoming_shows_count'] = upcoming_shows_count     
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  error = False
  body = {}
  try:
    name = request.form.get('name','')
    city = request.form.get('city','')
    state = request.form.get('state','')
    address = request.form.get('address','')
    phone = request.form.get('phone','')
    image_link = request.form.get('image_link','')
    genres=request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link','')
    seeking_description = request.form.get('seeking_description','')
    if seeking_description:
      seeking_talent = True
    else:
      seeking_talent = False
    website = request.form.get('website','')
    venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,genres=genres,seeking_talent=seeking_talent,seeking_description=seeking_description,website=website)
    db.session.add(venue)
    db.session.commit()
    body['id'] = Venue.id
  except():
    db.session.rollback()
    error = True
    print(sys.exc_info)
  finally:
    db.session.close()
  if error:
    abort(500)
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
   # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except():
      db.session.rollback()
      error = True
      print(sys.exc_info())
  finally:
      db.session.close()
  if error:
    abort(500)
    flash('cannot delete it')
  else:
    flash('deleted successfully')
  return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term +'%')).all()
  artists_count = Artist.query.filter(Artist.name.ilike('%' + search_term +'%')).count()
  response = {
    "count": artists_count,
    "data": []
  }
  for artist in artists:
    response['data'].append({
      "id": artist.id,
      "name": artist.name
    })  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.filter_by(id=artist_id).first()
  shows = Show.query.filter_by(artist_id=artist_id).all()
  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_talent,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  past_shows_count = 0
  upcoming_shows_count = 0
  
  for show in shows:
    if show.start_time < datetime.now():
      venue_info = Venue.query.filter_by(id=show.venue_id).first()
      data['past_shows'].append({
        "venue_id": venue_info.id,
        "venue_name": venue_info.name,
        "venue_image_link": venue_info.image_link,
        "start_time": format_datetime(str(show.start_time))
      })
      past_shows_count += 1
      data['past_shows_count'] = past_shows_count

  for show in shows:
    if show.start_time > datetime.now():
      venue_info = Venue.query.filter_by(id=show.venue_id).first()
      data['upcoming_shows'].append({
        "venue_id": venue_info.id,
        "venue_name": venue_info.name,
        "venue_image_link": venue_info.image_link,
        "start_time": format_datetime(str(show.start_time))
      }) 
      upcoming_shows_count += 1
      data['upcoming_shows_count'] = upcoming_shows_count
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()
  artist={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_talent": artist.seeking_talent,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  try:
    name = request.form.get('name','')
    city = request.form.get('city','')
    state = request.form.get('state','')
    phone = request.form.get('phone','')
    image_link = request.form.get('image_link','')
    genres=request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link','')
    seeking_description = request.form.get('seeking_description','')
    if seeking_description:
      seeking_talent = True
    else:
      seeking_talent = False
    website = request.form.get('website','')
    
    artist = Artist.query.get(artist_id)
    artist.id=artist_id
    artist.name=name
    artist.city=city
    artist.state=state
    artist.phone=phone
    artist.image_link=image_link
    artist.facebook_link=facebook_link
    artist.genres=genres
    artist.seeking_talent=seeking_talent
    artist.seeking_description=seeking_description
    artist.website=website
    db.session.commit()
  except():
    db.session.rollback()
    error = True
    print(sys.exc_info)
  finally:
    db.session.close()
  if error:
    abort(500)
    flash('Artist ' + request.form['name'] + ' can not updated')
  else:
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    name = request.form.get('name','')
    city = request.form.get('city','')
    state = request.form.get('state','')
    address = request.form.get('address','')
    phone = request.form.get('phone','')
    image_link = request.form.get('image_link','')
    genres=request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link','')
    seeking_description = request.form.get('seeking_description','')
    if seeking_description:
      seeking_talent = True
    else:
      seeking_talent = False
    website = request.form.get('website','')
    
    venue = Venue.query.get(venue_id)
    venue.id=venue_id
    venue.name=name
    venue.city=city
    venue.state=state
    venue.address=address
    venue.phone=phone
    venue.image_link=image_link
    venue.facebook_link=facebook_link
    venue.genres=genres
    venue.seeking_talent=seeking_talent
    venue.seeking_description=seeking_description
    venue.website=website
    db.session.commit()
  except():
    db.session.rollback()
    error = True
    print(sys.exc_info)
  finally:
    db.session.close()
  if error:
    abort(500)
    flash('Venue ' + request.form['name'] + ' can not updated')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/ 
   
  error = False
  body = {}
  try:
    name = request.form.get('name','')
    city = request.form.get('city','')
    state = request.form.get('state','')
    phone = request.form.get('phone','')
    image_link = request.form.get('image_link','')
    genres=request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link','')
    seeking_description = request.form.get('seeking_description','')
    if seeking_description:
      seeking_talent = True
    else:
      seeking_talent = False
    website = request.form.get('website','')
    artist = Artist(name=name,city=city,state=state,phone=phone,image_link=image_link,facebook_link=facebook_link,genres=genres,seeking_talent=seeking_talent,seeking_description=seeking_description,website=website)
    db.session.add(artist)
    db.session.commit()
    body['id'] = artist.id
  except():
    db.session.rollback()
    error = True
    print(sys.exc_info)
  finally:
    db.session.close()
  if error:
    abort(500)
    flash('An error occurred. Artist ' + request.form['name']+ ' could not be listed.')
  else:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  shows = Show.query.order_by(Show.start_time > datetime.now()).all()
  for show in shows:
    venue = Venue.query.filter_by(id=show.venue_id).first()
    artist = Artist.query.filter_by(id=show.artist_id).first()
    data.append({
      "venue_id": show.venue_id,
      "venue_name": venue.name,
      "artist_id": show.artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

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
