# Uses MVP Architecture
# Model
#   - Tile
#   - tile_service
#   - tiles_service
# View
#   - GameView
# Presenter
#   - GamePresenter

from GameView import GameView
from GamePresenter import GamePresenter

##################
###### MAIN ######
##################

game_presenter = GamePresenter(GameView())
game_presenter.start_game()
