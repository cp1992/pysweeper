# TODO: Would like to split game into Model-View-Presenter
# Model
#   - Tile: stores all information/functionality for tile
# View
#   - main: initial creation of UI, setups root
#   - GameView
# Presenter
#   - GamePresenter: stores game state model, modifies UI

from GameView import GameView
from GamePresenter import GamePresenter

##################
###### MAIN ######
##################

game_presenter = GamePresenter(GameView())
game_presenter.start_game()
