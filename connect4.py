import tkinter as tk
from enum import Enum
import time
class ConnectFour:
    class Player(Enum):
        RED = 1
        YELLOW = -1

    def __init__(self, parent: tk.Widget) -> None:
        self.RED_COLOUR = '#d60606'
        self.RED_HIGHLIGHT_COLOUR = '#f79e9e'
        self.YELLOW_COLOUR = '#e0e012'
        self.YELLOW_HIGHLIGHT_COLOUR = '#f6f79e'
        self.FRAME_COLOUR = '#2869d1'
        self.EMPTY_COLOUR = '#ffffff'
        self.OUTLINE_COLOUR = '#000000'

        self.ROWS = 6
        self.COLUMNS = 7
        self.CHECKER_RADIUS = 20
        self.CHECKER_PADDING = 15

        self.board_height = (
            self.CHECKER_RADIUS * 2 * self.ROWS + self.CHECKER_PADDING * (self.ROWS + 1)
        )
        self.board_width = (
            self.CHECKER_RADIUS * 2 * self.COLUMNS
            + self.CHECKER_PADDING * (self.COLUMNS + 1)
        )

        self.board = [[0] * self.COLUMNS for _ in range(self.ROWS)]
        self.current_player = self.Player.RED
        self.column_under_mouse = -1
        self.locked = False

        self.parent = parent
        self.canvas_checker_ids = [[-1] * self.COLUMNS for _ in range(self.ROWS)]
        self.column_ranges: list[tuple[int, range]] = []
        self.board_canvas = tk.Canvas(
            self.parent,
            bd=0,
            bg=self.FRAME_COLOUR,
            highlightthickness=0,
            height=self.board_height,
            width=self.board_width,
        )

        self.init_board()

    def init_board(self) -> None:
        for r in range(self.ROWS):
            for c in range(self.COLUMNS):
                x0 = (c + 1) * self.CHECKER_PADDING + 2 * self.CHECKER_RADIUS * c
                y0 = (r + 1) * self.CHECKER_PADDING + 2 * self.CHECKER_RADIUS * r
                checker_id = self.board_canvas.create_oval(
                    x0,
                    y0,
                    x0 + 2 * self.CHECKER_RADIUS,
                    y0 + 2 * self.CHECKER_RADIUS,
                    fill=self.EMPTY_COLOUR,
                    outline=self.OUTLINE_COLOUR,
                    width=2,
                )
                self.canvas_checker_ids[r][c] = checker_id
                self.column_ranges.append((c, range(x0, x0 + 2 * self.CHECKER_RADIUS)))

        self.board_canvas.grid(row=0, column=0)
        self.board_canvas.bind('<Motion>', self.mouse_motion_handler)
        self.board_canvas.bind('<ButtonRelease-1>', self.mouse_click_handler)

    def mouse_motion_handler(self, event: tk.Event) -> None:
        if self.locked:
            return
        for column, threshold in self.column_ranges:
            if event.x in threshold:
                self.column_under_mouse = column
                self.highlight_column(column)
                break
        else:
            self.column_under_mouse = -1
            self.unhighlight_columns()

    def mouse_click_handler(self, event: tk.Event) -> None:
        if self.locked:
            return
        self.place_checker(self.column_under_mouse)

    def switch_player(self) -> None:
        if self.current_player == self.Player.RED:
            self.current_player = self.Player.YELLOW

        elif self.current_player == self.Player.YELLOW:
            self.current_player = self.Player.RED

    def change_checker_colour(self, checker_id: int, colour: str) -> None:
        self.board_canvas.itemconfigure(checker_id, fill=colour)

    def place_checker(self, column: int) -> None:
        if self.column_under_mouse == -1 or self.locked:
            return
        for row in range(self.ROWS - 1, -1, -1):
            if not self.board[row][column]:
                player_val: int = self.current_player.value
                self.board[row][column] = player_val
                self.change_checker_colour(
                    self.canvas_checker_ids[row][column],
                    self.RED_COLOUR
                    if self.current_player is self.Player.RED
                    else self.YELLOW_COLOUR,
                )
                if self.check_wins(row, column):
                    print(self.current_player.name)
                self.switch_player()
                self.highlight_column(column)
                return

    def highlight_column(self, column: int) -> None:
        self.unhighlight_columns()
        for row in range(self.ROWS):
            if self.board[row][column]:
                break
            self.change_checker_colour(
                self.canvas_checker_ids[row][column],
                self.RED_HIGHLIGHT_COLOUR
                if self.current_player is self.Player.RED
                else self.YELLOW_HIGHLIGHT_COLOUR,
            )

    def unhighlight_columns(self) -> None:
        for column in range(self.COLUMNS):
            for row in range(self.ROWS):
                if self.board[row][column]:
                    break
                self.change_checker_colour(
                    self.canvas_checker_ids[row][column],
                    self.EMPTY_COLOUR,
                )

    def check_wins(self, row: int, column: int) -> bool:
        return (
            self.check_win_vertical(column)
            or self.check_win_horizontal(row)
            or self.check_win_rl_diagonal(row, column)
            or self.check_win_rl_diagonal(row, column)
        )

    def check_win_vertical(self, column: int) -> bool:
        c = [row[column] for row in self.board]
        for i in range(0, self.ROWS - 3):
            if abs(sum(c[i : i + 4])) == 4:
                return True
        return False

    def check_win_horizontal(self, row: int) -> bool:
        r = self.board[row]
        for i in range(0, self.COLUMNS - 3):
            if abs(sum(r[i : i + 4])) == 4:
                return True
        return False

    def check_win_lr_diagonal(self, row: int, col: int) -> bool:
        if col - row in range(-2, 4):
            pr, pc = row, col
            while not (pc <= 3 and pr <= 2):
                pr -= 1
                pc -= 1
            for i in range(3):
                lst = [self.board[pr + j][pc + j] for j in range(4)]
                if abs(sum(lst)) == 4:
                    return True
                if pr - 1 in range(self.ROWS) and pc - 1 in range(self.COLUMNS):
                    pr -= 1
                    pc -= 1
                else:
                    break
        return False

    def check_win_rl_diagonal(self, row: int, col: int) -> bool:
        if row + col in range(3, 9):
            pr, pc = row, col
            while not (pc >= 3 and pr <= 2):
                pr -= 1
                pc += 1
            for i in range(3):
                lst = [self.board[pr + j][pc - j] for j in range(4)]
                if abs(sum(lst)) == 4:
                    return True
                if pr - 1 in range(self.ROWS) and pc + 1 in range(self.COLUMNS):
                    pr -= 1
                    pc += 1
                else:
                    break
        return False

    def reset_game(self):
        for idl in self.canvas_checker_ids:
            for i in idl:
                self.change_checker_colour(i, self.EMPTY_COLOUR)

        self.board = [[0] * self.COLUMNS for _ in range(self.ROWS)]
        self.current_player = self.Player.RED
        self.column_under_mouse = -1


def main():
    root = tk.Tk()
    root.title('Connect 4')
    root.resizable(False, False)
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0)
    ConnectFour(main_frame)
    root.mainloop()


if __name__ == '__main__':
    main()
