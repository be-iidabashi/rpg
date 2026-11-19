import pyxel
import random
import json
import os
import PyxelUniversalFont as puf

# フォントの初期化
WRITER = puf.Writer("misaki_gothic.ttf")

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 192
TILE_SIZE = 16

# ==========================================
# ★ シーン番号の定義（SCENE_TITLE を 0 に追加）
# ==========================================
SCENE_TITLE = 0
SCENE_MAP = 1
SCENE_BATTLE = 2
SCENE_RESULT = 3
SCENE_GAMEOVER = 4

MAP_DATA = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2],
    [2, 1, 0, 0, 0, 0, 1, 0, 2, 2, 2, 0, 0, 1, 0, 2],
    [2, 1, 0, 2, 2, 0, 1, 0, 2, 0, 2, 0, 0, 1, 0, 2],
    [2, 1, 0, 2, 2, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2],
    [2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
    [2, 0, 0, 1, 0, 2, 2, 2, 2, 0, 1, 0, 2, 2, 0, 2],
    [2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 2, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


class RPGApp:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Pyxel RPG")

        if os.path.exists("my_resource.pyxres"):
            pyxel.load("my_resource.pyxres")

        self.monsters_master = self.load_monsters()
        
        # 最初はタイトル画面から開始
        self.init_game()
        self.scene = SCENE_TITLE

        pyxel.run(self.update, self.draw)

    def init_game(self):
        """★ ゲームの初期化処理（タイトルに戻る際やリトライ用）"""
        self.player = {
            "name": "勇者",
            "x": 16,
            "y": 40,
            "hp": 50,
            "max_hp": 50,
            "atk": 10,
            "potions": 3,
            "exp": 0
        }
        self.battle_turn = "player_turn"
        self.current_monster = None
        self.msg = ""

    def load_monsters(self):
        if os.path.exists("monsters.json"):
            try:
                with open("monsters.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return [
            {"name": "スライム", "hp": 20, "max_hp": 20, "atk": 5, "exp": 10, "u": 16, "v": 0, "w": 16, "h": 16},
            {"name": "魔王", "hp": 80, "max_hp": 80, "atk": 15, "exp": 100, "u": 32, "v": 0, "w": 16, "h": 16}
        ]

    def update(self):
        # 1. タイトル画面の入力待ち
        if self.scene == SCENE_TITLE:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.init_game()  # ステータス等の初期化
                self.scene = SCENE_MAP
                self.msg = "矢印キーでマップを歩こう！"

        # 2. マップ画面
        elif self.scene == SCENE_MAP:
            self.update_map()

        # 3. 戦闘画面
        elif self.scene == SCENE_BATTLE:
            self.update_battle()

        # 4. 戦闘結果画面（スペースでマップへ）
        elif self.scene == SCENE_RESULT:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = SCENE_MAP
                self.msg = ""

        # 5. ゲームオーバー画面（スペースでタイトルへ戻る）
        elif self.scene == SCENE_GAMEOVER:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = SCENE_TITLE

    def update_map(self):
        moved = False
        new_x, new_y = self.player["x"], self.player["y"]

        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            new_y -= TILE_SIZE
            moved = True
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            new_y += TILE_SIZE
            moved = True
        elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            new_x -= TILE_SIZE
            moved = True
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            new_x += TILE_SIZE
            moved = True

        tile_x = new_x // TILE_SIZE
        tile_y = (new_y - 20) // TILE_SIZE

        if 0 <= tile_y < len(MAP_DATA) and 0 <= tile_x < len(MAP_DATA[0]):
            if MAP_DATA[tile_y][tile_x] != 2:
                self.player["x"], self.player["y"] = new_x, new_y
            else:
                moved = False

        if moved:
            self.msg = ""
            if random.random() < 0.15:
                self.start_battle()

    def start_battle(self):
        self.scene = SCENE_BATTLE
        self.battle_turn = "player_turn"
        m_data = random.choice(self.monsters_master)
        self.current_monster = {
            "name": m_data["name"],
            "hp": m_data["hp"],
            "max_hp": m_data["max_hp"],
            "atk": m_data["atk"],
            "exp": m_data["exp"],
            "u": m_data.get("u", 16),
            "v": m_data.get("v", 0),
            "w": m_data.get("w", 16),
            "h": m_data.get("h", 16)
        }
        self.msg = f"{self.current_monster['name']} が あらわれた！"

    def update_battle(self):
        # プレイヤーの入力待ち
        if self.battle_turn == "player_turn":
            if pyxel.btnp(pyxel.KEY_1):
                damage = self.player["atk"] + random.randint(-2, 3)
                self.current_monster["hp"] -= damage
                self.msg = f"{self.player['name']}の こうげき！ {damage}のダメージ！"  # (SPACE)を削除

                if self.current_monster["hp"] <= 0:
                    self.current_monster["hp"] = 0
                    self.msg = f"{self.current_monster['name']}を たおした！"           # (SPACE)を削除
                    self.scene = SCENE_RESULT
                    return

                self.battle_turn = "player_msg"

            elif pyxel.btnp(pyxel.KEY_2):
                if self.player["potions"] > 0:
                    self.player["potions"] -= 1
                    self.player["hp"] = min(self.player["max_hp"], self.player["hp"] + 25)
                    self.msg = "ポーションをつかった！ HPがかいふくした！"              # (SPACE)を削除
                    self.battle_turn = "player_msg"
                else:
                    self.msg = "ポーションが ない！"

            elif pyxel.btnp(pyxel.KEY_3):
                if random.random() < 0.6:
                    self.msg = "うまく にげだした！"
                    self.scene = SCENE_MAP
                else:
                    self.msg = "にげきれなかった！"                                     # (SPACE)を削除
                    self.battle_turn = "player_msg"

        # 勇者の行動結果表示 ➔ SPACEで敵の攻撃へ
        elif self.battle_turn == "player_msg":
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                m_damage = self.current_monster["atk"] + random.randint(-1, 2)
                self.player["hp"] -= m_damage
                self.msg = f"{self.current_monster['name']}の こうげき！ {m_damage}のダメージ！"  # (SPACE)を削除

                if self.player["hp"] <= 0:
                    self.player["hp"] = 0
                    self.scene = SCENE_GAMEOVER
                    self.msg = "ゆうしゃは たおれてしまった..."
                    return

                self.battle_turn = "enemy_msg"

        # 敵の行動結果表示 ➔ SPACEでコマンド選択へ復帰
        elif self.battle_turn == "enemy_msg":
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.msg = ""
                self.battle_turn = "player_turn"

    def draw(self):
        pyxel.cls(0)

        if self.scene == SCENE_TITLE:
            self.draw_title()
        elif self.scene == SCENE_MAP:
            self.draw_map()
        elif self.scene in (SCENE_BATTLE, SCENE_RESULT):
            self.draw_battle()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover()

        # ★ 最下部メッセージ枠の描画
        if self.msg and self.scene != SCENE_TITLE:
            pyxel.rectb(0, 168, WINDOW_WIDTH, 24, 7)
            
            # メッセージ本文の描画
            WRITER.draw(8, 176, self.msg, 8, 7)

            # ★ SPACEキー入力待ち状態か判定するフラグ
            is_waiting_space = (
                self.scene == SCENE_RESULT or 
                (self.scene == SCENE_BATTLE and self.battle_turn in ("player_msg", "enemy_msg"))
            )

            # SPACE待ち ＆ 点滅タイミングの時にだけ (SPACE) を右端に表示
            if is_waiting_space and (pyxel.frame_count // 20) % 2 == 0:
                # 画面右端（X=190, Y=176）あたりに (SPACE) を点滅描画
                WRITER.draw(190, 176, "(SPACE)", 8, 10)  # 10=黄色でアクセント

    def draw_title(self):
        """★ タイトル画面の描画"""
        WRITER.draw(100, 60, "パイセル ＲＰＧ", 8, 10)
        
        # 点滅させる演出（一定フレームごとに表示/非表示）
        if (pyxel.frame_count // 30) % 2 == 0:
            WRITER.draw(80, 120, "- PRESS SPACE TO START -", 8, 7)

    def draw_gameover(self):
        """★ ゲームオーバー画面の描画"""
        WRITER.draw(110, 70, "GAME OVER", 8, 8)
        if (pyxel.frame_count // 30) % 2 == 0:
            WRITER.draw(80, 120, "- PRESS SPACE TO TITLE -", 8, 7)

    def draw_map(self):
        for row_idx, row in enumerate(MAP_DATA):
            for col_idx, tile_type in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE + 24

                if tile_type == 0:
                    u, v = 0, 16
                elif tile_type == 1:
                    u, v = 16, 16
                elif tile_type == 2:
                    u, v = 32, 16

                pyxel.blt(x, y, 0, u, v, TILE_SIZE, TILE_SIZE)

        pyxel.rect(0, 0, WINDOW_WIDTH, 24, 0)
        WRITER.draw(8, 8, f"HP: {self.player['hp']}/{self.player['max_hp']}", 8, 11)
        WRITER.draw(100, 8, f"薬: {self.player['potions']}", 8, 10)
        WRITER.draw(180, 8, f"EXP: {self.player['exp']}", 8, 9)

        pyxel.blt(self.player["x"], self.player["y"], 0, 0, 0, TILE_SIZE, TILE_SIZE, 0)

    def draw_battle(self):
        pyxel.rectb(8, 8, WINDOW_WIDTH - 16, 152, 7)

        m = self.current_monster
        pyxel.blt(112, 28, 0, m["u"], m["v"], m["w"], m["h"], 0, scale=2)

        WRITER.draw(20, 24, f"てき: {m['name']}", 8, 7)
        WRITER.draw(20, 36, f"HP: {max(0, m['hp'])}/{m['max_hp']}", 8, 8)
        
        WRITER.draw(20, 80, f"ゆうしゃ: {self.player['name']}", 8, 7)
        WRITER.draw(20, 92, f"HP: {self.player['hp']}/{self.player['max_hp']}", 8, 11)

        if self.scene == SCENE_BATTLE and self.battle_turn == "player_turn":
            pyxel.rect(16, 128, 224, 20, 1)
            WRITER.draw(24, 134, "[1] たたかう   [2] くすり   [3] にげる", 8, 7)


if __name__ == "__main__":
    RPGApp()