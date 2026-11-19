# 1日目ハンズオン教材：Pythonの基本とCUIテキストRPG開発

本日は、Pythonの基本構文を学びながら、ターミナル（CUI）上で動く本格的な「テキスト選択型RPG」を構築します。
本日作成するプレイヤーのデータ構造やモンスターのJSONデータ、ダメージ計算ロジックは、**2日目のPyxel（GUI）開発でそのまま再利用**します！

---

## 🎯 本日のゴール

- 変数・条件分岐（`if`）・繰り返し（`while`）・関数（`def`）の基本を理解する
- 辞書型（`dict`）を使って、プレイヤーのステータスを管理する
- `json` モジュールを使って、外部ファイルからモンスターデータを読み込む
- ターミナル上でコマンド（[1]たたかう [2]くすり [3]にげる）を入力して遊べるテキストRPGを完成させる

---

## 📂 1. 事前準備とファイル構成

本日の作業用に `rpg` フォルダを作成し、その中に以下のファイルを作成・準備します。

```text
rpg/
├── main_cui.py      # 本日作成するPythonプログラム
└── monsters.json    # モンスターのステータスデータ（JSON形式）
```

---

## 📜 2. モンスターデータの作成 (`monsters.json`)

まずは、ゲームに登場するモンスターのデータを記述した `monsters.json` を作成します。
（2日目のドット絵表示位置 `u, v, w, h` 情報もあらかじめ含めておきます）

```json
[
  {
    "name": "スライム",
    "hp": 20,
    "max_hp": 20,
    "atk": 5,
    "exp": 10,
    "u": 16,
    "v": 0,
    "w": 16,
    "h": 16
  },
  {
    "name": "魔王",
    "hp": 80,
    "max_hp": 80,
    "atk": 15,
    "exp": 100,
    "u": 32,
    "v": 0,
    "w": 16,
    "h": 16
  }
]
```

---

## 🛠️ 3. メインプログラムの作成 (`main_cui.py`)

ステップ順にコードを追加・理解していきましょう。

### STEP 1: モジュール読み込みとJSONデータの読み込み関数

標準ライブラリの `random`（乱数生成）、`json`（ファイル読み込み）、`os`（ファイル存在チェック）を使用します。

```python
import random
import json
import os

def load_monsters():
    """monsters.json からモンスター一覧を読み込む関数"""
    if os.path.exists("monsters.json"):
        try:
            with open("monsters.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"JSON読み込みエラー: {e}")
            
    # ファイルがない場合の予備データ（バックアップ）
    return [
        {"name": "スライム", "hp": 20, "max_hp": 20, "atk": 5, "exp": 10},
        {"name": "魔王", "hp": 80, "max_hp": 80, "atk": 15, "exp": 100}
    ]
```

---

### STEP 2: プレイヤーデータの定義と基本関数の作成

辞書型（`dict`）を使って、勇者のステータスを定義します。

```python
# プレイヤーのステータス（辞書型）
player = {
    "name": "勇者",
    "hp": 50,
    "max_hp": 50,
    "atk": 10,
    "potions": 3,
    "exp": 0
}

def print_status(player, monster):
    """現在のステータスを表示する関数"""
    print("\n----------------------------------------")
    print(f"【{monster['name']}】 HP: {monster['hp']}/{monster['max_hp']}")
    print(f"【{player['name']}】   HP: {player['hp']}/{player['max_hp']} | ポーション: {player['potions']}個 | EXP: {player['exp']}")
    print("----------------------------------------")
```

---

### STEP 3: バトル処理のメインループ構築

`while` ループを使い、どちらかのHPが0になるまで対戦を繰り返すロジックを記述します。

```python
def battle():
    monsters_master = load_monsters()
    # 出現するモンスターをランダムに選出（コピーして使用）
    monster_data = random.choice(monsters_master)
    monster = monster_data.copy()

    print(f"\nあやしい けはいが する...！")
    print(f"【{monster['name']}】が あらわれた！")

    # 戦闘メインループ
    while player["hp"] > 0 and monster["hp"] > 0:
        print_status(player, monster)
        print("コマンドを選んでください:")
        print("[1] たたかう  [2] くすり  [3] にげる")
        
        command = input(">> ")

        # 1. たたかう
        if command == "1":
            damage = player["atk"] + random.randint(-2, 3)
            monster["hp"] -= damage
            print(f"\n⚔️  {player['name']}の こうげき！ {monster['name']}に {damage} のダメージ！")

            # 敵を倒したか判定
            if monster["hp"] <= 0:
                monster["hp"] = 0
                print(f"\n🎉 {monster['name']}を たおした！")
                player["exp"] += monster["exp"]
                print(f"経験値を {monster['exp']} 獲得した！（合計: {player['exp']}）")
                break

            # 敵の反撃
            m_damage = monster["atk"] + random.randint(-1, 2)
            player["hp"] -= m_damage
            print(f"💥 {monster['name']}の こうげき！ {player['name']}は {m_damage} のダメージをうけた！")

        # 2. くすり
        elif command == "2":
            if player["potions"] > 0:
                player["potions"] -= 1
                heal = 25
                player["hp"] = min(player["max_hp"], player["hp"] + heal)
                print(f"\n🧪 ポーションをつかった！ HPが {heal} 回復した！")
                
                # 薬を使っても敵のターンは経過する
                m_damage = monster["atk"] + random.randint(-1, 2)
                player["hp"] -= m_damage
                print(f"💥 {monster['name']}の こうげき！ {player['name']}は {m_damage} のダメージをうけた！")
            else:
                print("\n❌ ポーションが もう ない！")

        # 3. にげる
        elif command == "3":
            if random.random() < 0.6:
                print("\n💨 うまく にげだした！")
                return
            else:
                print("\n❌ にげきれなかった！")
                m_damage = monster["atk"] + random.randint(-1, 2)
                player["hp"] -= m_damage
                print(f"💥 {monster['name']}の こうげき！ {player['name']}は {m_damage} のダメージをうけた！")

        else:
            print("\n⚠️ 1, 2, 3 の数字を入力してください。")

    # 勝敗判定
    if player["hp"] <= 0:
        player["hp"] = 0
        print(f"\n💀 {player['name']}は たおれてしまった...")
        print("--- GAME OVER ---")
```

---

### STEP 4: 全体ゲームループの実装

連続して冒険を遊べるようにメインプログラムを開始します。

```python
def main():
    print("========================================")
    print("      Python テキスト RPG へ ようこそ！  ")
    print("========================================")

    while True:
        if player["hp"] <= 0:
            break

        print("\nどうしますか？")
        print("[1] たんさくする  [2] ステータスをみる  [3] おわる")
        choice = input(">> ")

        if choice == "1":
            battle()
        elif choice == "2":
            print(f"\n--- {player['name']} の ステータス ---")
            print(f"HP: {player['hp']}/{player['max_hp']}")
            print(f"攻撃力: {player['atk']}")
            print(f"所持ポーション: {player['potions']}個")
            print(f"獲得経験値: {player['exp']}")
        elif choice == "3":
            print("\n冒険を終了します。おつかれさまでした！")
            break
        else:
            print("\n⚠️ 1, 2, 3 の数字を入力してください。")

if __name__ == "__main__":
    main()
```

---

## 🎮 4. 動作確認と遊んでみよう

ファイルを保存したら、ターミナルで実行してみましょう！

```bash
python main_cui.py
```

### チェックリスト

- [ ] `monsters.json` から「スライム」や「魔王」が正しく呼び出されるか？
- [ ] `[1] たたかう` を選んだ際、ダメージ計算と敵の反撃が交互に行われるか？
- [ ] `[2] くすり` を使った際、HPの上限（`max_hp`）を超えずに回復するか？
- [ ] 敵を倒した際、経験値（`exp`）が正しく加算されるか？

---

## 💡 明日（2日目）へのつながり

今日作成した以下の部分は、**明日Pyxelでつくる2DレトロRPGにそのまま移植**されます！

1. **`player` 辞書データ** ➔ 画面上のUI表示や移動位置（`x`, `y`）の追加
2. **`monsters.json` のデータ** ➔ 2Dドット絵の切り出し位置（`u`, `v`）として利用
3. **ダメージ計算・反撃処理** ➔ キー入力＆画面上のターン制テキスト送り（`(SPACE)`）へ応用

お疲れ様でした！明日はこのプログラムに「ドット絵・マップ移動・日本語フォント表示」をつけて、本物のレトロゲームを完成させましょう！