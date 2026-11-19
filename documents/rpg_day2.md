# 2日目ハンズオン教材：Pyxelでつくる 2DレトロRPG開発

1日目で作った「ターミナルで動くテキストRPG」のプログラム（データ管理やバトルロジック）をそのまま活用し、2日目はレトロゲームエンジン **Pyxel** を使って、本格的な2DレトロRPGへ進化させましょう！

---

## 🎯 本日のゴール

* 16×16ドット絵のプレイヤーやマップチップを画面に描画できる
* 2Dマップをグラフィックで表示し、壁判定つきで歩き回れる
* ランダムエンカウントでバトル画面へ遷移し、1日目のバトルロジックで戦える
* `PyxelUniversalFont` を使い、8×8ドットの美しい日本語メッセージを表示できる
* タイトル ➔ マップ ➔ バトル ➔ リザルト ➔ ゲームオーバー ➔ タイトル のゲームループを完成させる

---

## 📂 1. 事前準備とファイル構成

本日の作業フォルダ（`rpg/`）の中に、以下のファイルが正しく揃っているか確認してください。

```text
rpg/
├── main.py               # 本日メインで作成するPythonプログラム
├── make_res.py           # ドット絵リソース生成スクリプト
├── misaki_gothic.ttf     # 日本語ドット絵フォントファイル（8x8）
└── monsters.json         # 1日目に作成したモンスターデータ
```

---

## 🎨 2. ドット絵リソースの生成 (`make_res.py`)

まずはゲーム内で使用するキャラクター、マップチップ（草原・道・木）、モンスターのドット絵データを生成します。

以下のコードを `make_res.py` として作成し、ターミナルで実行してください。

```python
import pyxel

# Pyxelの初期化
pyxel.init(160, 120)

# ==========================================
# 1. プレイヤー (u:0, v:0) / 16x16
# ==========================================
player_pixels = [
    [0,0,0,0,0,11,11,11,11,11,11,0,0,0,0,0],
    [0,0,0,0,11,11,11,11,11,11,11,11,0,0,0,0],
    [0,0,0,11,11,11,11,11,11,11,11,11,11,0,0,0],
    [0,0,0,0,15,15,15,15,15,15,15,15,0,0,0,0],
    [0,0,0,0,15,1,15,15,15,15,1,15,0,0,0,0],
    [0,0,0,0,15,15,15,15,15,15,15,15,0,0,0,0],
    [0,0,0,0,0,15,15,15,15,15,15,0,0,0,0,0],
    [0,0,8,8,8,8,8,8,8,8,8,8,8,8,8,0],
    [0,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
    [0,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
    [0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0],
    [0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,0],
    [0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,0],
    [0,0,0,4,4,4,4,0,0,4,4,4,4,0,0,0],
    [0,0,0,4,4,4,4,0,0,4,4,4,4,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
for y, row in enumerate(player_pixels):
    for x, col in enumerate(row):
        pyxel.images[0].pset(x, y, col)

# ==========================================
# 2. スライム (u:16, v:0) / 16x16
# ==========================================
slime_pixels = [
    [0,0,0,0,0,0,12,12,12,12,0,0,0,0,0,0],
    [0,0,0,0,0,12,12,12,12,12,12,0,0,0,0,0],
    [0,0,0,0,12,12,12,12,12,12,12,12,0,0,0,0],
    [0,0,0,12,12,12,12,12,12,12,12,12,12,0,0,0],
    [0,0,12,12,7,7,12,12,12,12,7,7,12,12,0,0],
    [0,0,12,12,1,7,12,12,12,12,1,7,12,12,0,0],
    [0,12,12,12,7,7,12,12,12,12,7,7,12,12,12,0],
    [0,12,12,12,12,12,12,12,12,12,12,12,12,12,12,0],
    [0,12,12,12,12,12,8,8,8,8,12,12,12,12,12,0],
    [0,12,12,12,12,12,12,12,12,12,12,12,12,12,12,0],
    [0,12,12,12,12,12,12,12,12,12,12,12,12,12,12,0],
    [0,0,12,12,12,12,12,12,12,12,12,12,12,12,0,0],
    [0,0,0,12,12,12,12,12,12,12,12,12,12,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
for y, row in enumerate(slime_pixels):
    for x, col in enumerate(row):
        pyxel.images[0].pset(16 + x, y, col)

# ==========================================
# 3. 魔王 (u:32, v:0) / 16x16
# ==========================================
boss_pixels = [
    [0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0],
    [0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0],
    [0,0,2,2,0,0,8,8,8,8,0,0,2,2,0,0],
    [0,0,0,2,8,8,8,8,8,8,8,8,2,0,0,0],
    [0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0],
    [0,0,8,8,10,7,8,8,8,8,10,7,8,8,0,0],
    [0,0,8,8,10,10,8,8,8,8,10,10,8,8,0,0],
    [0,8,8,8,8,8,8,8,8,8,8,8,8,8,8,0],
    [0,8,8,8,7,0,7,0,7,0,7,0,8,8,8,0],
    [0,0,8,8,8,7,7,7,7,7,7,8,8,8,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,0,0,0],
    [0,0,2,2,2,2,2,2,2,2,2,2,2,2,0,0],
    [0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0],
    [0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0],
    [0,0,2,2,2,2,2,0,0,2,2,2,2,2,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]
for y, row in enumerate(boss_pixels):
    for x, col in enumerate(row):
        pyxel.images[0].pset(32 + x, y, col)

# ==========================================
# 4. マップチップ (u:0, 16, 32 / v:16)
# ==========================================
grass_pixels = [[3]*16 for _ in range(16)]
path_pixels = [[9]*16 for _ in range(16)]
tree_pixels = [[11]*16 for _ in range(16)]

for y, row in enumerate(grass_pixels):
    for x, col in enumerate(row):
        pyxel.images[0].pset(x, 16 + y, col)

for y, row in enumerate(path_pixels):
    for x, col in enumerate(row):
        pyxel.images[0].pset(16 + x, 16 + y, col)

for y, row in enumerate(tree_pixels):
    for x, col in enumerate(row):
        pyxel.images[0].pset(32 + x, 16 + y, col)

# リソースファイルとして保存
pyxel.save("my_resource.pyxres")
print("✅ 'my_resource.pyxres' の生成が完了しました！")
```

### 実行コマンド
```bash
python make_res.py
```
実行後、フォルダ内に `my_resource.pyxres` が作成されたことを確認してください。

---

## 🛠️ 3. メインプログラムの作成 (`main.py`)

`main.py` にゲーム全体のコードを記述します。コードをステップごとに理解しながら作成していきましょう。

### STEP 1: 定数・フォントの初期化とマップデータ

画面サイズ（256×192）、16×16のタイルサイズ、5つのゲームシーン（状態）を定義します。

```python
import pyxel
import random
import json
import os
import PyxelUniversalFont as puf

# 美咲フォント（8x8ドット）の初期化
WRITER = puf.Writer("misaki_gothic.ttf")

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 192
TILE_SIZE = 16

# シーン（状態管理）定数
SCENE_TITLE = 0     # タイトル画面
SCENE_MAP = 1       # マップ移動
SCENE_BATTLE = 2    # 戦闘実行
SCENE_RESULT = 3    # 勝利結果表示
SCENE_GAMEOVER = 4  # ゲームオーバー

# 16列 x 9行 のマップデータ（0:草原, 1:道, 2:木/壁）
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
```

---

### STEP 2: ゲーム本体クラスと初期化処理

`RPGApp` クラスを作成し、1日目に作成した `player` 辞書データと `monsters.json` の読み込み処理を組み込みます。

```python
class RPGApp:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Pyxel RPG")

        if os.path.exists("my_resource.pyxres"):
            pyxel.load("my_resource.pyxres")

        self.monsters_master = self.load_monsters()
        self.init_game()
        self.scene = SCENE_TITLE

        pyxel.run(self.update, self.draw)

    def init_game(self):
        """ゲームデータの初期化（再スタート用）"""
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
        """外部JSONファイルからのモンスターデータ読み込み"""
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
```

---

### STEP 3: 更新ロジック (`update`)

メインのステートマシン（シーン分岐）とマップ移動・衝突判定処理を実装します。

```python
    def update(self):
        if self.scene == SCENE_TITLE:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.init_game()
                self.scene = SCENE_MAP
                self.msg = "矢印キーでマップを歩こう！"

        elif self.scene == SCENE_MAP:
            self.update_map()

        elif self.scene == SCENE_BATTLE:
            self.update_battle()

        elif self.scene == SCENE_RESULT:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = SCENE_MAP
                self.msg = ""

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

        # マップ配列上の座標計算（上部ステータスUI分の20pxを引いて計算）
        tile_x = new_x // TILE_SIZE
        tile_y = (new_y - 20) // TILE_SIZE

        # 「木（値=2）」以外であれば移動を許可
        if 0 <= tile_y < len(MAP_DATA) and 0 <= tile_x < len(MAP_DATA[0]):
            if MAP_DATA[tile_y][tile_x] != 2:
                self.player["x"], self.player["y"] = new_x, new_y
            else:
                moved = False

        if moved:
            self.msg = ""
            # 15% の確率でランダムエンカウント
            if random.random() < 0.15:
                self.start_battle()
```

---

### STEP 4: ターン制バトルロジック (`update_battle`)

1日目に作成したバトルロジックを、メッセージ送りと交互ターン（`player_turn` → `player_msg` → `enemy_msg`）で管理します。

```python
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
        # 1. プレイヤーコマンド選択
        if self.battle_turn == "player_turn":
            if pyxel.btnp(pyxel.KEY_1):
                damage = self.player["atk"] + random.randint(-2, 3)
                self.current_monster["hp"] -= damage
                self.msg = f"{self.player['name']}の こうげき！ {damage}のダメージ！"

                if self.current_monster["hp"] <= 0:
                    self.current_monster["hp"] = 0
                    self.msg = f"{self.current_monster['name']}を たおした！"
                    self.scene = SCENE_RESULT
                    return

                self.battle_turn = "player_msg"

            elif pyxel.btnp(pyxel.KEY_2):
                if self.player["potions"] > 0:
                    self.player["potions"] -= 1
                    self.player["hp"] = min(self.player["max_hp"], self.player["hp"] + 25)
                    self.msg = "ポーションをつかった！ HPがかいふくした！"
                    self.battle_turn = "player_msg"
                else:
                    self.msg = "ポーションが ない！"

            elif pyxel.btnp(pyxel.KEY_3):
                if random.random() < 0.6:
                    self.msg = "うまく にげだした！"
                    self.scene = SCENE_MAP
                else:
                    self.msg = "にげきれなかった！"
                    self.battle_turn = "player_msg"

        # 2. プレイヤー行動結果表示 ➔ SPACEキーで敵の攻撃へ
        elif self.battle_turn == "player_msg":
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                m_damage = self.current_monster["atk"] + random.randint(-1, 2)
                self.player["hp"] -= m_damage
                self.msg = f"{self.current_monster['name']}の こうげき！ {m_damage}のダメージ！"

                if self.player["hp"] <= 0:
                    self.player["hp"] = 0
                    self.scene = SCENE_GAMEOVER
                    self.msg = "ゆうしゃは たおれてしまった..."
                    return

                self.battle_turn = "enemy_msg"

        # 3. 敵の行動結果表示 ➔ SPACEキーでコマンド選択へ復帰
        elif self.battle_turn == "enemy_msg":
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.msg = ""
                self.battle_turn = "player_turn"
```

---

### STEP 5: 画面描画処理 (`draw`)

美咲フォントでの日本語テキスト表示と、`(SPACE)` Promptのチカチカ点滅アニメーションを含む描画ロジックを実装します。

```python
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

        # 最下部メッセージ枠の描画
        if self.msg and self.scene != SCENE_TITLE:
            pyxel.rectb(0, 168, WINDOW_WIDTH, 24, 7)
            WRITER.draw(8, 176, self.msg, 8, 7)

            # SPACEキー入力待ちの際に (SPACE) を点滅表示
            is_waiting_space = (
                self.scene == SCENE_RESULT or 
                (self.scene == SCENE_BATTLE and self.battle_turn in ("player_msg", "enemy_msg"))
            )
            if is_waiting_space and (pyxel.frame_count // 20) % 2 == 0:
                WRITER.draw(190, 176, "(SPACE)", 8, 10)

    def draw_title(self):
        """タイトル画面描画"""
        WRITER.draw(100, 60, "パイセル ＲＰＧ", 8, 10)
        if (pyxel.frame_count // 30) % 2 == 0:
            WRITER.draw(80, 120, "- PRESS SPACE TO START -", 8, 7)

    def draw_gameover(self):
        """ゲームオーバー画面描画"""
        WRITER.draw(110, 60, "GAME OVER", 8, 8)
        if (pyxel.frame_count // 30) % 2 == 0:
            WRITER.draw(80, 120, "- PRESS SPACE TO TITLE -", 8, 7)

    def draw_map(self):
        """マップ画面描画"""
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

        # 上部ステータスバー
        pyxel.rect(0, 0, WINDOW_WIDTH, 24, 0)
        WRITER.draw(8, 8, f"HP: {self.player['hp']}/{self.player['max_hp']}", 8, 11)
        WRITER.draw(100, 8, f"薬: {self.player['potions']}", 8, 10)
        WRITER.draw(180, 8, f"EXP: {self.player['exp']}", 8, 9)

        # プレイヤー描画
        pyxel.blt(self.player["x"], self.player["y"], 0, 0, 0, TILE_SIZE, TILE_SIZE, 0)

    def draw_battle(self):
        """バトル画面描画"""
        pyxel.rectb(8, 8, WINDOW_WIDTH - 16, 152, 7)

        m = self.current_monster
        # モンスターを scale=2 (32x32px) で迫力のある拡大描画
        pyxel.blt(112, 28, 0, m["u"], m["v"], m["w"], m["h"], 0, scale=2)

        WRITER.draw(20, 24, f"てき: {m['name']}", 8, 7)
        WRITER.draw(20, 36, f"HP: {max(0, m['hp'])}/{m['max_hp']}", 8, 8)
        WRITER.draw(20, 80, f"ゆうしゃ: {self.player['name']}", 8, 7)
        WRITER.draw(20, 92, f"HP: {self.player['hp']}/{self.player['max_hp']}", 8, 11)

        # プレイヤーの入力待ちターン時のみコマンド枠を表示
        if self.scene == SCENE_BATTLE and self.battle_turn == "player_turn":
            pyxel.rect(16, 128, 224, 20, 1)
            WRITER.draw(24, 134, "[1] たたかう   [2] くすり   [3] にげる", 8, 7)


if __name__ == "__main__":
    RPGApp()
```

---

## 🎮 4. 動作確認と遊んでみよう

完成したら、ターミナルで実行して動作を確認しましょう！

```bash
python main.py
```

### チェックリスト
- [ ] タイトル画面で `PRESS SPACE TO START` が点滅表示されるか？
- [ ] 矢印キーでマップを歩き回り、木のタイル（壁）で正しく止まるか？
- [ ] 草原や道を歩いているとバトル画面に切り替わるか？
- [ ] バトル画面でモンスターのドット絵が2倍の大きさで表示されているか？
- [ ] 攻撃実行後、`(SPACE)` が黄色く点滅し、スペースキーで敵の反撃が進むか？
- [ ] 勇者のHPが0になったらゲームオーバー画面になり、タイトルへ戻れるか？

---

## 🚀 5. 発展課題（チャレンジ！）

早く完成した人は、以下の機能拡張にチャレンジしてみましょう！

1. **新しいモンスターを追加しよう**  
   `monsters.json` に新しいモンスター（ドラゴンなど）のステータスデータを追加してみましょう。
2. **ポーションの回復量を調整しよう**  
   `update_battle` 内のポーション回復量や、モンスターの攻撃力バランスを変更してゲームの難易度を調整してみましょう！