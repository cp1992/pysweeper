import tkinter as tk
from tkinter import ttk
from tkinter import Menu

from Tile import Tile

# TODO: fix how widgets are layed out, on medium/hard difficulty board overlays bomb count
# TODO: fix window size for hard difficulty

class GameView:
    # constants
    window_width = 800
    window_height = 600

    # widgets
    root = None
    board = None
    game_status_text = None
    new_game_button = None
    bomb_count_text = None

    def __get_center(self, root, window_width, window_height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        return f'{center_x}+{center_y}'

    # set window height/width, position, and title
    def create_window(self):
        self.root = tk.Tk()
        center_coordinates = self.__get_center(
            self.root, self.window_width, self.window_height)

        self.root.geometry(
            f'{self.window_width}x{self.window_height}+{center_coordinates}')
        self.root.resizable(False, False)
        self.root.title("pysweeper")

    def create_menu(self, change_difficulty_clicked_listener):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        difficulty_menu = Menu(menubar)
        difficulty_menu.add_command(label="Easy", command=lambda: change_difficulty_clicked_listener(10, 12))
        difficulty_menu.add_command(label="Medium", command=lambda: change_difficulty_clicked_listener(15, 40))
        difficulty_menu.add_command(label="Hard", command=lambda: change_difficulty_clicked_listener(25, 99))
        menubar.add_cascade(label="Difficulty", menu=difficulty_menu)

    # create board/tiles
    def create_board(self, size, tile_clicked_listener, tile_right_clicked_listener):
        self.board = ttk.Frame(self.root)
        self.board.columnconfigure(size)
        self.board.rowconfigure(size)

        tiles = []
        tile_img = tk.PhotoImage(file="assets/tile.png")
        for x in range(0, size):
            col = []
            for y in range(0, size):
                tile_widget = ttk.Label(self.board, image=tile_img)
                tile_widget.image = tile_img
                tile_widget.bind("<Button-1>", lambda _, x=x,
                                                      y=y: tile_clicked_listener(x, y))
                tile_widget.bind("<Button-2>", lambda _, x=x,
                                                      y=y: tile_right_clicked_listener(x, y))
                tile_widget.grid(column=x, row=y)
                tile = Tile(coordinates=(x, y),
                            widget=tile_widget)
                col.append(tile)
            tiles.append(col)

        self.board.place(relx=.5, rely=.5, anchor="center")

        return tiles

    def destroy_board(self):
        self.board.destroy()

    def create_game_status_frame(self, bomb_count, new_game_clicked_listener):
        # create bomb count, game status text (win/lose), and new game button which will be added to a frame object
        game_status_frame = ttk.Frame(self.root)
        self.bomb_count_text = ttk.Label(
            game_status_frame, text=f"Bombs: {bomb_count}")
        self.bomb_count_text.pack()

        self.game_status_text = ttk.Label(
            game_status_frame, text="Lost Game!")
        self.new_game_button = ttk.Button(
            game_status_frame, text="New Game", command=new_game_clicked_listener)
        game_status_frame.place(relx=.5, rely=.8, anchor="center")

    def show_game_status(self, status):
        self.game_status_text.config(text=status)
        self.game_status_text.pack()
        self.new_game_button.pack()

    def hide_game_status(self):
        self.game_status_text.pack_forget()
        self.new_game_button.pack_forget()

    def set_bomb_count(self, bomb_count):
        self.bomb_count_text.config(text=f"Bombs: {bomb_count}")
