from flask import Flask, render_template, request, redirect, url_for, session

from Forms import CreateSongForm
from Song import Song
from database_functions import *

app = Flask(__name__)
app.secret_key = 'dvUEshVu3XWrc7gU73ZdT92lpWLhOrUlYS6lGrdR'


@app.route('/')
def home():
    with shelve.open('music_app.db', 'c') as music_app_db:
        song_list = create_song_list(music_app_db['Songs'])
        deleted_song_id = session.pop('deleted_song_id', None)
    session['url'] = url_for('home')
    return render_template('home.html', song_list=song_list, song_count=len(song_list),
                           deleted_song_id=deleted_song_id, current_theme=get_current_theme())


@app.route('/change-theme')
def change_theme():
    # attach theme to user object/database later
    with shelve.open('music_app.db', 'c') as music_app_db:
        current_theme = music_app_db['Theme']
        if current_theme == 'light':
            music_app_db['Theme'] = 'dark'
        else:
            music_app_db['Theme'] = 'light'
    return redirect(session.pop('url', None))


# song routes


@app.route('/create-song', methods=["GET", "POST"])
def create_song():
    print(request.form)
    create_song_form = CreateSongForm(request.form)
    if request.method == "GET" or not create_song_form.validate():
        session['url'] = url_for('create_song')
        return render_template('createSong.html', form=create_song_form,
                               current_theme=get_current_theme())
    with shelve.open('music_app.db', 'c') as music_app_db:
        song_dict = music_app_db['Songs']
        new_song_id = generate_song_id(song_dict)
        song = Song(new_song_id, list(create_song_form.data.values()))
        song_dict[new_song_id] = song
        music_app_db['Songs'] = song_dict
    return redirect(url_for('home'))


@app.route('/update-song', methods=["GET", "POST"])
def update_song():
    song_id = request.args.get('song_id')
    update_song_form = CreateSongForm(request.form)
    with shelve.open('music_app.db', 'c') as music_app_db:
        song_dict = music_app_db['Songs']
        song = song_dict.get(song_id)
        if request.method == "GET" or not update_song_form.validate():
            update_song_form.name.data = song.name
            update_song_form.artist.data = song.artist
            update_song_form.album.data = song.album
            update_song_form.track.data = song.track
            update_song_form.cover.data = song.cover
            session['url'] = url_for('update_song', song_id=song_id)
            return render_template('updateSong.html', form=update_song_form,
                                   current_theme=music_app_db['Theme'])
        else:
            song.name = update_song_form.name.data
            song.artist = update_song_form.artist.data
            song.album = update_song_form.album.data
            song.track = update_song_form.track.data
            song.cover = update_song_form.cover.data
            song_dict[song_id] = song
            music_app_db['Songs'] = song_dict
            return redirect(url_for('home'))


@app.route('/delete-song/<song_id>', methods=['POST'])
def delete_song(song_id):
    with shelve.open('music_app.db', 'c') as music_app_db:
        song_dict = music_app_db['Songs']
        song = song_dict.get(song_id)
        song.hidden = True
        song_dict[song_id] = song
        music_app_db['Songs'] = song_dict
        session['deleted_song_id'] = song_id
    return redirect(url_for('home'))


@app.route('/delete-all-songs', methods=['GET'])
def delete_all_songs():
    with shelve.open('music_app.db', 'c') as music_app_db:
        music_app_db['Songs'] = hide_all_songs(music_app_db['Songs'])
    return redirect(url_for('home'))


@app.route('/undo-delete-song/<deleted_song_id>', methods=['GET'])
def undo_delete_song(deleted_song_id):
    with shelve.open('music_app.db', 'c') as music_app_db:
        song_dict = music_app_db['Songs']
        song = song_dict.get(deleted_song_id)
        song.show()
        song_dict[deleted_song_id] = song
        music_app_db['Songs'] = song_dict
    return redirect(url_for('home'))


@app.route('/recently-deleted-songs', methods=['GET'])
def recently_deleted_songs():
    with shelve.open('music_app.db', 'c') as music_app_db:
        song_list = recently_deleted_songs_list(music_app_db['Songs'])
        session['url'] = url_for('recently_deleted_songs')
        return render_template('recentlyDeletedSongs.html', song_list=song_list,
                               song_count=len(song_list), current_theme=music_app_db['Theme'])


@app.route('/restore-song/<song_id>', methods=['POST'])
def restore_song(song_id):
    with shelve.open('music_app.db', 'c') as music_app_db:
        song_dict = music_app_db['Songs']
        song_dict.get(song_id).show()
        music_app_db['Songs'] = song_dict
    return redirect(url_for('recently_deleted_songs'))


@app.route('/permanent-delete-song/<song_id>', methods=['POST'])
def permanent_delete_song(song_id):
    with shelve.open('music_app.db', 'c') as music_app_db:
        song_dict = music_app_db['Songs']
        song_dict.pop(song_id)
        music_app_db['Songs'] = song_dict
        session['deleted_song_id'] = None
    return redirect(url_for('recently_deleted_songs'))


@app.route('/permanent-delete-all-songs', methods=['GET'])
def permanent_delete_all_songs():
    with shelve.open('music_app.db', 'c') as music_app_db:
        song_dict = music_app_db['Songs']
        if song_dict:
            new_song_dict = delete_all_songs_in_recently_deleted(song_dict)
            music_app_db['Songs'] = new_song_dict
    return redirect(url_for('recently_deleted_songs'))


@app.route('/restore-all-songs', methods=['GET'])
def restore_all_songs():
    with shelve.open('music_app.db', 'c') as music_app_db:
        song_dict = music_app_db['Songs']
        new_song_dict = show_all_songs(song_dict)
        music_app_db['Songs'] = new_song_dict
    return redirect(url_for('recently_deleted_songs'))


# playlist routes
@app.route('/playlists', methods=['GET'])
def playlists():
    session['url'] = url_for('playlists')
    return render_template('playlists.html', current_theme=session['theme'])


# profile routes

@app.route('/profile', methods=['GET'])
def profile():
    session['url'] = url_for('profile')
    return render_template('profile.html', current_theme=session['theme'])


if __name__ == "__main__":
    app.run(debug=True)
    try:
        with shelve.open('music_app.db', 'c') as music_app_database:
            if not music_app_database:
                music_app_database['Songs'] = {}
                music_app_database['Playlists'] = {}
                music_app_database['Theme'] = 'light'
    except IOError:
        print("Error opening database")
