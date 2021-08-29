class FilmCard:
    def __init__(self, release_year, title, origin, genre, plot):
        self.release_year = release_year
        self.title = title
        self.origin = origin
        self.genre = genre
        self.plot = plot
    
    def get_box(self, box_name):
        if box_name == 'release_year':
            return self.release_year
        if box_name == 'title':
            return self.title
        if box_name == 'origin':
            return self.origin
        if box_name == 'genre':
            return self.genre
        if box_name == 'plot':
            return self.plot
    
    def print_film_info(self):
        print(f'{self.title}\t{self.release_year}\n{self.plot}\n')