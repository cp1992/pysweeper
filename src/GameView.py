import tkinter as tk
from tkinter import ttk

from Tile import Tile


class GameView:

    # constants
    window_width = 800
    window_height = 600

    # widgets
    root = None
    game_status_text = None
    new_game_button = None

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

    # create board/tiles
    def create_board(self, size, tile_clicked_listener, tile_right_clicked_listener):
        frame = ttk.Frame(self.root)
        frame.columnconfigure(size)
        frame.rowconfigure(size)

        tiles = []
        tileImg = tk.PhotoImage(file="assets/tile.png")
        for x in range(0, size):
            col = []
            for y in range(0, size):
                tileWidget = ttk.Label(frame, image=tileImg)
                tileWidget.image = tileImg
                tileWidget.bind("<Button-1>", lambda _, x=x,
                                y=y: tile_clicked_listener(x, y))
                tileWidget.bind("<Button-2>", lambda _, x=x,
                                y=y: tile_right_clicked_listener(x, y))
                tileWidget.grid(column=x, row=y)
                tile = Tile(coordinates=(x, y),
                            widget=tileWidget)
                col.append(tile)
            tiles.append(col)

        frame.place(relx=.5, rely=.5, anchor="center")

        return tiles

    def create_game_status_frame(self, bomb_count, new_game_clicked_listener):
        # create bomb count, game status text (win/lose), and new game button which will be added to a frame object
        game_status_frame = ttk.Frame(self.root)
        self.bomb_count_text = ttk.Label(game_status_frame, text=f"Bombs: {bomb_count}")
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
