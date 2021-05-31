from copy import deepcopy
from Board import *


class DotsAndBoxes:
    def __init__(self, x, y, _ply):
        self.ply = _ply
        self.board = Board(x, y)

    '''
    Fungsi yang berisi main loop game dan memberi turn untuk human player dan ai player secara bergantian sampai
    semua garis terisi pada board.
    '''

    def execute_game(self):
        print("Playing Dots And Boxes")
        while len(self.board.open_vectors) > 0:
            print("Tekan 0 dan enter untuk keluar")

            self.board.display()

            move_status = self.player_move()
            if move_status == False:
                break

            self.ai_move()
        self.display_result()

    '''
    Fungsi untuk menerima move dari human player dengan format x1,y1,x2,y2 yang berarti (x1,y1) dihubungkan dengan (x2,y2).
    Move yang valid akan me-return 0 dan keluar dari loop, tetapi move yang tidak valid akan me-return -1 dan
    menampilkan pesan error.
    '''

    def player_move(self):
        while True:
            try:
                integers = input("Koordinat yang ingin dihubungkan (x1 y1 x2 y2): ")

                integers = integers.split()

                for i in range(0, len(integers)):
                    integers[i] = int(integers[i])

                if integers == 0:
                    return False

                coordinates = ((integers[0], integers[1]), (integers[2], integers[3]))

                move_status = self.board.move(coordinates, 0)

                if move_status == 0:
                    break
                elif move_status == -1:
                    print("Koordinat tidak valid")
            except SyntaxError:
                print("Input tidak valid")
        return True

    '''
    Fungsi untuk melakukan move dari ai player setelah human player melakukan move.
    Fungsi ini memanggil minimax() untuk mengeksekusi algoritma alpha-beta pruning.
    Hasil dari eksekusi alpha-beta pruning dipakai untuk menentukan move ai player.
    '''

    def ai_move(self):
        # salin state board terkini untuk kalkulasi tree
        state = deepcopy(self.board)
        open_vectors = deepcopy(self.board.open_vectors)

        # mengambil koordinat dari algoritma minimax
        coordinates = self.minimax(state, open_vectors, self.ply, True)

        self.board.move(coordinates[1], 1)

    '''
    Fungsi untuk mengeksekusi algoritma alpha-beta pruning.
    Parameter:
        state - state board terkini
        open_vectors - himpunan vektor yang dapat dipilih dari state board terkini
        ply - total depth dari game tree
        max - nilai "True" merepresentasikan AI dan "False" merepresentasikan human player
    Individual succesor state dibuat dalam main loop sebelum dilakukan pemanggilan algoritma alpha-beta pruning
    secara rekursif untuk menjelajahi keturunan selanjutnya dalam game tree.
    '''

    def minimax(self, state, open_vectors, ply, max_min):
        # nilai default dari best_move_val adalah -inf untuk layer Max dan +inf untuk layer Min
        if max_min == True:
            best_move_val = (-1000000, None)
        else:
            best_move_val = (1000000, None)

        # jika successor sudah habis atau depth limit sudah tercapai
        # maka evaluasi dan kembalikan nilai dari state terkini
        if ply == 0 or len(open_vectors) == 0:
            h = self.evaluation_function(state)
            return (h, None)

        # mendapatkan successor
        for i in range(0, len(open_vectors)):
            # mendapatkan koordinat dari successor state terkini
            move = open_vectors.pop()

            # melakukan deep copy dari state yang akan dijelajahi
            state_copy = deepcopy(state)
            open_vectors_copy = deepcopy(open_vectors)
            state_copy.move(move, max_min)

            # tambahkan koordinat kembali ke "open_vectors" untuk memastikan
            # child state selanjutnya dalam depth terkini dapat menjelajahi sisa state dalam tree
            open_vectors.appendleft(move)

            # Alpha-Beta Pruning

            # periksa nilai yang diperlukan (alpha di min node dan beta di max node) sebelum menjelajahi node children.
            h = self.evaluation_function(state_copy)
            if max_min == True:
                if h >= state_copy.beta:
                    return (h, move)
                else:
                    state_copy.alpha = max(state_copy.alpha, h)
            else:
                if h <= state_copy.alpha:
                    return (h, move)
                else:
                    state_copy.beta = min(state_copy.beta, h)

            # lakukan pemanggilan minimax() secara rekursif dengan child state
            # goal state di-propagate kembali ke atas tree di akhir rekursi, saat depth limit tercapai atau open moves habis
            next_move = self.minimax(state_copy, open_vectors_copy, ply - 1, not max_min)

            # bandingkan skor dari child state dengan "best_move_val"
            if max_min == True:
                # pada max level, cari skor yang lebih besar dari skor maksimum terkini
                if next_move[0] > best_move_val[0]:
                    best_move_val = (next_move[0], move)
            else:
                # pada min level, cari skor yang lebih kecil dari skor minimum terkini
                if next_move[0] < best_move_val[0]:
                    best_move_val = (next_move[0], move)
        return best_move_val

    '''
    Fungsi evaluasi untuk menghitung nilai heuristik dari state yang diberi.
    Nilai heuristik dihitung dengan mengurangi skor total AI player dengan skor total human player.
    '''

    def evaluation_function(self, state):
        h = state.ai_score - state.player_score
        return h

    '''
    Fungsi untuk menampilkan skor player dan pemenang dari game.
    '''

    def display_result(self):
        self.board.display()

        if self.board.player_score > self.board.ai_score:
            print("Human Player Menang!")
        elif self.board.player_score < self.board.ai_score:
            print("AI Player Menang!")
        else:
            print("Seri!")

        print("Skor human player: %s" % self.board.player_score)
        print("Skor AI player: %s" % self.board.ai_score)