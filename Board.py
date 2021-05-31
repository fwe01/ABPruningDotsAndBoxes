from collections import deque
from Box import *


class Board:
    '''
    Constructor
    '''
    def __init__(self, column, row):
        # inisiasi skor pemain dan ai
        self.player_score = 0
        self.ai_score = 0

        # set panjang dan lebar papan
        self.m = column
        self.n = row

        self.boxes = self.generate_boxes(column, row)
        self.open_vectors = self.generate_vectors(column, row)

        # membuat set dari objek yang menyimpan titik-titik yang terhubung
        self.connected_vectors = set()

        # inisiasi nilai alpha dan beta untuk alpha beta pruning
        self.alpha = -100000
        self.beta = 100000

    '''
    Fungsi untuk menghasilkan objek-objek Box pada board.
    Box-box tersebut berfungsi untuk menyimpan meta data yang dibutuhkan untuk
    merepresentasikan informasi state.
    '''
    def generate_boxes(self, m, n):
        row = m
        column = n
        boxes = [[Box(0, 0) for j in range(column)] for i in range(row)]
        for i in range(m):
            for j in range(n):
                boxes[i][j] = (Box(i, j))
        return boxes

    '''
    Fungsi untuk menghasilkan vektor-vektor yang merepresentasikan semua gerakan yang mungkin yang dapat
    dimainkan pada board dengan ukuran m baris dan n kolom. Vektor-vektor tersebut disimpan sebagai tuple yang
    berisi koordinat titik dan disimpan dalam queue. Queue tersebut dan list yang berisi box-box yang berhubungan dengan
    koordinat-koordinat titik tersebut digunakan untuk merepresentasikan game state.
    Format vektor adalah ((x1, y1), (x2, y2))
    '''
    def generate_vectors(self, m, n):
        vec = deque()
        for i in range(0, m + 1):
            for j in range(0, n):
                vec.append(((j, i), (j + 1, i)))
                if i < m:
                    vec.append(((j, i), (j, i + 1)))
            if i < m:
                vec.append(((n, i), (n, i + 1)))
        return vec

    '''
    Fungsi untuk menampilkan state board yang terkini pada command line.
    '''
    def display(self):
        print("Skor player: %s" % self.player_score)
        print("Skor AI: %s" % self.ai_score)

        # cetak label x-axis
        h_str = "\n  "
        for i in range(self.m + 1):
            h_str = h_str + "   %s" % i
        print(h_str)

        # mencetak board
        box_value = " "
        for i in range(self.m + 1):
            # tambahkan label y-axis di awal baris
            h_str = "%s " % i
            v_str = "     "
            for j in range(self.n + 1):
                # periksa koneksi horizontal
                if ((j - 1, i), (j, i)) in self.connected_vectors:
                    h_str = h_str + "---o"
                else:
                    h_str = h_str + "   o"

                # periksa nilai box dari kotak
                if j < self.n:
                    if self.boxes[j][i - 1].top_left == (j, i - 1):
                        box_value = self.boxes[j][i - 1].value
                else:
                    box_value = " "

                # periksa koneksi vertikal
                if ((j, i - 1), (j, i)) in self.connected_vectors:
                    v_str = v_str + "| %s " % box_value
                else:
                    v_str = v_str + "  %s " % box_value
            print(v_str)
            print(h_str)
        print("")

    '''
    Fungsi untuk melakukan move pada board. Move diperiksa dengan mencari koordinat yang dipilih dalam queue "open_vectors".
    Jika ditemukan, maka pop koordinat tersebut dari "open_vectors" dan tambahkan koordinat tersebut ke "connected_vectors".
    Selanjutnya, periksa apakah ada box yang sudah di-capture.
    Jika move tidak berhasil, maka return -1. 
    '''
    def move(self, coordinates, player):
        if player == True:
            player = 1
        elif player == False:
            player = 0
        if coordinates in self.open_vectors:
            self.open_vectors.remove(coordinates)
            self.connected_vectors.add(coordinates)
            self.check_boxes(coordinates, player)
            return 0
        else:
            return -1

    '''
    Fungsi untuk menerima himpunan koordinat dan player yang bermain sekarang.
    Dalam fungsi ini dilakukan iterasi dari list box untuk mencari apakah suatu garis berada pada box yang tersimpan.
    Jika terbentuk sebuah box, player yang men-capture box tersebut diberikan poin tambahan dan dijadikan pemiliki box.
    '''
    def check_boxes(self, coordinates, player):
        for i in range(self.m):
            for j in range(self.n):
                # identifikasi box berdasarkan koordinat kiri atas
                box = self.boxes[i][j]
                if coordinates in box.lines:
                    box.make_edge(coordinates)
                if box.captured is True and box.owner is None:
                    box.owner = player
                    self.prevComplete = True
                    # beri poin kepada player yang men-capture box
                    # human player
                    if player == 0:
                        self.player_score += box.value
                    # ai player
                    elif player == 1:
                        self.ai_score += box.value
