import random
import string
import shelve


def find_user(user_dict, email):
    for user in user_dict.values():
        if email == user.get_email():
            return user
    return False


def get_current_theme():
    with shelve.open('music_app.db', 'c') as music_app_db:
        return music_app_db.get('Theme', None)


def generate_song_id(song_dict):
    new_id = 'S' + "".join([str(random.choice((range(10)))) for _ in range(8)])
    if new_id in song_dict:
        return generate_song_id(song_dict)
    return new_id


def generate_user_id(user_dict):
    new_id = random.choice(string.ascii_uppercase[:7]) + "".join([str(random.choice((range(10)))) for _ in range(8)])
    if new_id in user_dict:
        return generate_song_id(user_dict)
    return new_id


def create_song_list(song_dict):
    return list(enumerate([song for song in song_dict.values() if not song.hidden], 1))


def recently_deleted_songs_list(song_dict):
    return list(enumerate([song for song in song_dict.values() if song.hidden], 1))


def delete_all_songs_in_recently_deleted(song_dict):
    return {song_id: song for song_id, song in song_dict.items() if not song.hidden}


def show_all_songs(song_dict):
    return {song_id: song.show() for song_id, song in song_dict.items()}


def hide_all_songs(song_dict):
    print(song_dict.items())
    x = {song_id: song.hide() for song_id, song in song_dict.items()}
    print(x)
    return x

