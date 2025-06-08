import tkinter as tk
from tkinter import messagebox

class ReversiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("リバーシ [現在：先攻 黒]")
        self.root.resizable(width=False,height=False)

        # ゲーム設定
        self.size = 8  # 8x8
        self.cell_size = 60  # ピクセル
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.turn = 1  # 1 = 黒, 2 = 白

        # 初期配置
        self.board[3][3] = self.board[4][4] = 2
        self.board[3][4] = self.board[4][3] = 1

        # キャンバスの作成
        self.canvas = tk.Canvas(self.root, width=self.size*self.cell_size, height=self.size*self.cell_size, bg="green")
        self.canvas.pack()

        # クリックイベントを設定
        self.canvas.bind("<Button-1>", self.handle_click)

        # 盤面を描画
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")

        # タイトル更新
        if self.turn == 1:
            self.root.title("リバーシ [現在：先攻 黒]")
        else:
            self.root.title("リバーシ [現在：後攻 白]")

        for y in range(self.size):
            for x in range(self.size):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

                if self.board[y][x] == 1:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="black")
                elif self.board[y][x] == 2:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="white")

    def handle_click(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        if self.is_valid_move(x, y, flip=True):
            self.board[y][x] = self.turn
            self.turn = 3 - self.turn
            self.draw_board()

            # 手番自動交代（パス判定含む）
            self.turn_change_if_needed()

    def is_valid_move(self, x, y, flip=False):
        if self.board[y][x] != 0:
            return False

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        valid = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            stones_to_flip = []

            while 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == 3 - self.turn:
                stones_to_flip.append((nx, ny))
                nx += dx
                ny += dy

            if stones_to_flip and 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == self.turn:
                if flip:
                    for fx, fy in stones_to_flip:
                        self.board[fy][fx] = self.turn
                valid = True

        return valid

    def turn_change_if_needed(self):
        # 次のターンのプレイヤーが合法手を持つか調べる
        has_move = False
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == 0 and self.is_valid_move(x, y, flip=False):
                    has_move = True
                    break
            if has_move:
                break

        if has_move:
            # 手番はそのまま → 通常通り
            self.draw_board()
        else:
            # パス → 手番交代
            messagebox.showinfo("パス", "打てる手がないためパスします。")
            self.turn = 3 - self.turn
            self.draw_board()

            # 交代後のプレイヤーも置けないならゲーム終了
            has_move_after_pass = False
            for y in range(self.size):
                for x in range(self.size):
                    if self.board[y][x] == 0 and self.is_valid_move(x, y, flip=False):
                        has_move_after_pass = True
                        break
                if has_move_after_pass:
                    break

            if not has_move_after_pass:
                self.game_over()

    def game_over(self):
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(2) for row in self.board)

        if black_count > white_count:
            result = "黒（先攻）の勝ち！"
        elif white_count > black_count:
            result = "白（後攻）の勝ち！"
        else:
            result = "引き分け！"

        messagebox.showinfo("ゲーム終了", f"黒: {black_count} 石\n白: {white_count} 石\n\n{result}")

        # やり直し確認
        retry = messagebox.askyesno("もう一度プレイ", "最初からやり直しますか？")
        if retry:
            self.reset_game()
        else:
            self.root.quit()

    def reset_game(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.turn = 1
        self.board[3][3] = self.board[4][4] = 2
        self.board[3][4] = self.board[4][3] = 1
        self.draw_board()

# メイン実行
if __name__ == "__main__":
    root = tk.Tk()
    game = ReversiGUI(root)
    root.mainloop()
