class Song:
    def __init__(self, song_id, data_inputs):
        self.id = song_id
        self.name = data_inputs[0]
        self.artist = data_inputs[1]
        self.album = data_inputs[2]
        self.track = data_inputs[3]
        self.cover = data_inputs[4]
        self.total_listens = 0
        self.hidden = False

    def show(self):
        self.hidden = False
        return self

    def hide(self):
        self.hidden = True
        return self

