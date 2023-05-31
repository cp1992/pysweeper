import tkinter as tk
from tkinter import ttk
from tkinter import Menu

from utils import flatten

from Tile import Tile


class GameView:
    # constants
    window_width = 1200
    window_height = 900

    # widgets
    window = None
    root = None
    board = None
    game_status_frame = None
    game_status_text = None
    new_game_button = None
    bomb_count_text = None

    # set window height/width, position, and title
    def create_window(self):
        self.window = tk.Tk()
        self.window.state('zoomed')
        self.window.resizable(False, False)
        self.window.title("pysweeper")

        self.root = ttk.Frame(self.window)
        self.root.place(relx=.5, rely=.5, anchor="center")

    def create_menu(self, change_difficulty_clicked_listener):
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        difficulty_menu = Menu(menubar)
        difficulty_menu.add_command(label="Easy", command=lambda: change_difficulty_clicked_listener("easy"))
        difficulty_menu.add_command(label="Medium", command=lambda: change_difficulty_clicked_listener("medium"))
        difficulty_menu.add_command(label="Hard", command=lambda: change_difficulty_clicked_listener("hard"))
        menubar.add_cascade(label="Difficulty", menu=difficulty_menu)

    # create board/tiles
    def create_board(self, size, tile_clicked_listener, tile_right_clicked_listener):
        if not self.board:
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

        self.board.pack()

        return tiles

    def destroy_tiles(self, tiles):
        for tile in flatten(tiles):
            tile.widget.destroy()

    def create_game_status_frame(self, bomb_count, new_game_clicked_listener):
        # create bomb count, game status text (win/lose), and new game button which will be added to a frame object
        self.game_status_frame = ttk.Frame(self.root)
        self.bomb_count_text = ttk.Label(
            self.game_status_frame, text=f"Bombs: {bomb_count}")
        self.bomb_count_text.pack()

        self.game_status_text = ttk.Label(
            self.game_status_frame, text="Lost Game!")
        self.new_game_button = ttk.Button(
            self.game_status_frame, text="New Game", command=new_game_clicked_listener)
        self.game_status_frame.pack(pady=20)

    def show_game_status(self, status):
        self.game_status_text.config(text=status)
        self.game_status_text.pack()
        self.new_game_button.pack()

    def hide_game_status(self):
        self.game_status_text.pack_forget()
        self.new_game_button.pack_forget()

    def set_bomb_count(self, bomb_count):
        self.bomb_count_text.config(text=f"Bombs: {bomb_count}")
