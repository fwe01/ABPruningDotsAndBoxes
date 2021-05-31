class Box:
    '''
    Constructor
    '''
    def __init__(self, x, y):
        # himpunan koordinat box
        self.coordinates = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]

        # koordinat kiri atas
        self.top_left = (x, y)

        # garis atas
        self.top_line = (self.coordinates[0], self.coordinates[1])

        # garis kanan
        self.right_line = (self.coordinates[1], self.coordinates[3])

        # garis bawah
        self.bottom_line = (self.coordinates[2],  self.coordinates[3])

        # garis kiri
        self.left_line = (self.coordinates[0],  self.coordinates[2])

        # himpunan garis box
        self.lines = ([self.top_line, self.right_line, self.bottom_line, self.left_line])

        # indikator dari titik yang terhubung
        self.top_connected = False
        self.right_connected = False
        self.bottom_connected = False
        self.left_connected = False

        # pemain yang mendapatkan box
        self.owner = None
        self.captured = False

        # set nilai dari box
        self.value = 1

    '''
    Fungsi untuk membuat rusuk (edge) atau menghubungkan dua titik dalam box
    '''
    def make_edge(self, coordinates):
        edge = coordinates
        edge_created = False
        if edge in self.lines:
            if edge == self.top_line and self.top_connected == False:
                self.top_connected = True
                edge_created = True
            elif edge == self.right_line and self.right_connected == False:
                self.right_connected = True
                edge_created = True
            elif edge == self.bottom_line and self.bottom_connected == False:
                self.bottom_connected = True
                edge_created = True
            elif edge == self.left_line and self.left_connected == False:
                self.left_connected = True
                edge_created = True
        if self.top_connected == True and self.right_connected == True and self.bottom_connected == True and self.left_connected == True:
            self.captured = True
        return edge_created
