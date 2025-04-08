from enum import Enum

RED     = 1             # Số đại diện cho màu quân cờ trên board
YELLOW  = - RED
IDLE    = 0             # Ô trống, chưa đánh


WIDTH = 600             # Screen width
FIRST_MOVING = RED

DISPLAY_TURN_RUNTIME = False        # Thời gian chạy của từng turn (do MatchMaker đếm)
    