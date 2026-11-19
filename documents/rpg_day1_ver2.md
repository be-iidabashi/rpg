
---

# 🎮 Day 1 ハンズオンテキスト：Python基礎 & CUIテキストRPGを作ろう！

ようこそ！1日目のテーマは **「プログラミングの仕組み（ロジック）をマスターする」** です。

今日はターミナル（黒い画面）上でコマンドを入力してモンスターと戦う「CUIテキストRPG」を制作します。

今日作成するプレイヤーデータやモンスターデータの仕組みは、**そのまま2日目のPyxel（ドット絵GUI画面）に引き継がれます！**

---

## 📂 本日作成・使用するファイル

* `main.py` ：RPGの全プログラムを書くメインファイル
* `monsters_cli.json` ：モンスターのデータを保存する外部ファイル

---

## 【ステップ0】環境確認と最初のプログラム（10分）

まずは開発環境（VS Codeなど）が正しく動くか確認しましょう。

1. 作業フォルダを開き、新規ファイル `main.py` を作成します。
2. 以下のコードを入力してください。

```python
print("=== RPG開発スタート！ ===")

```

3. ターミナルを開き、以下のコマンドで実行してみましょう。

```bash
python main.py

```

ターミナルに `=== RPG開発スタート！ ===` と表示されれば準備完了です！

---

## 【ステップ1】勇者のステータス（辞書型 `dict`）を作成する（25分）

ゲームの主人公である「勇者」のステータスを作ります。

Pythonでは、複数のデータをまとめるために **「辞書型（`dict`）」** という仕組みを使います。

### 1. コードの記述 (`main.py`)

`main.py` を以下のように書き換えます。

```python
# 勇者のステータスを辞書型で定義
player = {
    "name": "勇者",
    "hp": 50,
    "max_hp": 50,
    "atk": 10,
    "potions": 3,
    "exp": 0
}

# ステータスの表示
print("--- 勇者のステータス ---")
print(f"名前: {player['name']}")
print(f"HP  : {player['hp']} / {player['max_hp']}")
print(f"攻撃力: {player['atk']}")
print(f"ポーション: {player['potions']}個")
print("------------------------")

```

### 💡 プログラミングのポイント

* **辞書型 (`dict`)**：`"キー": 値` のペアでデータを管理します。
* **`player["hp"]`** のようにキー名を指定することで、必要な値をピンポイントで取り出したり書き換えたりできます。

---

## 【ステップ2】1対1のバトルシーンを単体で作って遊ぶ（70分）

ここが最初の山場です！

全体を作る前に、まずは「モンスター1体と戦って勝ち負けが決まるバトル機能」だけを単体で作成して動かしてみましょう。

### 1. コードの記述 (`main.py`)

`main.py` の末尾に以下のバトル処理を追加します。

```python
import random

# テスト用のモンスターデータ（直書き）
monster = {
    "name": "スライム",
    "hp": 20,
    "max_hp": 20,
    "atk": 5,
    "exp": 10
}

print(f"\nあ、あくまの {monster['name']} が あらわれた！")

# バトルのループ開始
while True:
    print(f"\n【{player['name']} HP:{player['hp']}/{player['max_hp']}】 vs 【{monster['name']} HP:{monster['hp']}/{monster['max_hp']}】")
    print("1: たたかう | 2: くすり | 3: にげる")
    choice = input("どうする？ (1-3): ")

    # 1: たたかう
    if choice == "1":
        damage = player["atk"] + random.randint(-2, 3)
        monster["hp"] -= damage
        print(f"⚔️ {player['name']}の こうげき！ {monster['name']}に {damage}のダメージ！")

        # モンスターを倒した判定
        if monster["hp"] <= 0:
            print(f"🎉 {monster['name']}を たおした！")
            player["exp"] += monster["exp"]
            print(f"経験値を {monster['exp']} ゲット！ (トータル: {player['exp']})")
            break

        # モンスターの反撃
        m_damage = monster["atk"] + random.randint(-1, 2)
        player["hp"] -= m_damage
        print(f"💥 {monster['name']}の こうげき！ {player['name']}は {m_damage}のダメージ！")

    # 2: くすり
    elif choice == "2":
        if player["potions"] > 0:
            player["potions"] -= 1
            heal = 25
            player["hp"] = min(player["max_hp"], player["hp"] + heal)
            print(f"🧪 ポーションをつかった！ HPが {heal} 回復した！（残り {player['potions']}個）")
        else:
            print("❌ ポーションが もう ない！")
            continue

    # 3: にげる
    elif choice == "3":
        if random.random() < 0.6:
            print("🏃 うまく にげだした！")
            break
        else:
            print("💦 にげきれなかった！")
            # 逃げ失敗時も反撃を受ける
            m_damage = monster["atk"] + random.randint(-1, 2)
            player["hp"] -= m_damage
            print(f"💥 {monster['name']}の こうげき！ {player['name']}は {m_damage}のダメージ！")

    else:
        print("1〜3の数字を入力してください。")
        continue

    # 勇者が倒れた判定
    if player["hp"] <= 0:
        print(f"\n💀 {player['name']}は たおれてしまった...")
        print("=== GAME OVER ===")
        break

```

### 💡 プログラミングのポイント

* **`while True:`** ：勝負がつくまで何度もコマンド選択を繰り返す「ゲームループ」です。
* **`break`** ：モンスターを倒す、逃げ切る、またはHPが0になるとループを抜けてバトルを終了します。
* **`random.randint(a, b)`** ：攻撃力にランダムなブレ（乱数）を与えてバトルを面白くしています。

プログラムを実行し、実際にコマンドを入力して勝敗が決まるまで遊べるか試してみましょう！

---

## 【ステップ3】モンスターデータをJSONファイルに分離する（40分）

ステップ2ではモンスターデータをプログラム内に直接書きましたが、これではモンスターの種類を増やすのが大変です。

モンスターのデータを外部の **JSONファイル (`monsters_cli.json`)** に分けましょう！

### 1. `monsters_cli.json` の作成

`main.py` と同じフォルダに `monsters_cli.json` を作成し、以下を記述します。

```json
[
  {
    "name": "スライム",
    "hp": 20,
    "max_hp": 20,
    "atk": 5,
    "exp": 10
  },
  {
    "name": "ゴブリン",
    "hp": 35,
    "max_hp": 35,
    "atk": 8,
    "exp": 25
  },
  {
    "name": "魔王",
    "hp": 80,
    "max_hp": 80,
    "atk": 15,
    "exp": 100
  }
]

```

### 2. `main.py` でJSONを読み込む関数の作成

`main.py` の冒頭に JSON 読み込み関数 `load_monsters()` を追加します。

```python
import json
import random

def load_monsters():
    """外部のJSONファイルからモンスター一覧を読み込む関数"""
    try:
        with open("monsters_cli.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"JSON読み込みエラー: {e}")
        # ファイルがない場合のバックアップデータ
        return [{"name": "スライム", "hp": 20, "max_hp": 20, "atk": 5, "exp": 10}]

```

プログラムからデータを切り離すことで、**コードを1行も変えずにモンスターの種類や強さを自由に調整できるようになります！**

---

## 【ステップ4】冒険のメインループとエンカウントを統合する（45分）

最後に、ステップ2で作ったバトル処理を関数化（`battle()`）し、マップ探索とランダムエンカウントを行う全体ループ（`main()`）に統合します！

### 📄 `main.py` の完成版コード

`main.py` 全体を以下の完成コードに差し替えて実行してみましょう。

```python
import json
import random

# --- 1. データ読み込み処理 ---
def load_monsters():
    try:
        with open("monsters_cli.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return [{"name": "スライム", "hp": 20, "max_hp": 20, "atk": 5, "exp": 10}]


# --- 2. バトル処理（関数化） ---
def battle(player, monster_data):
    # 出現したモンスターの辞書データを複製して生成
    monster = dict(monster_data)
    print(f"\nあ、あくまの {monster['name']} が あらわれた！")

    while True:
        print(f"\n【{player['name']} HP:{player['hp']}/{player['max_hp']}】 vs 【{monster['name']} HP:{monster['hp']}/{monster['max_hp']}】")
        print("1: たたかう | 2: くすり | 3: にげる")
        choice = input("どうする？ (1-3): ")

        if choice == "1":
            damage = player["atk"] + random.randint(-2, 3)
            monster["hp"] -= damage
            print(f"⚔️ {player['name']}の こうげき！ {monster['name']}に {damage}のダメージ！")

            if monster["hp"] <= 0:
                print(f"🎉 {monster['name']}を たおした！")
                player["exp"] += monster["exp"]
                print(f"経験値を {monster['exp']} ゲット！ (トータル: {player['exp']})")
                return True  # 勝利

            m_damage = monster["atk"] + random.randint(-1, 2)
            player["hp"] -= m_damage
            print(f"💥 {monster['name']}の こうげき！ {player['name']}は {m_damage}のダメージ！")

        elif choice == "2":
            if player["potions"] > 0:
                player["potions"] -= 1
                heal = 25
                player["hp"] = min(player["max_hp"], player["hp"] + heal)
                print(f"🧪 ポーションをつかった！ HPが {heal} 回復した！（残り {player['potions']}個）")
            else:
                print("❌ ポーションが もう ない！")
                continue

        elif choice == "3":
            if random.random() < 0.6:
                print("🏃 うまく にげだした！")
                return True  # 逃走成功
            else:
                print("💦 にげきれなかった！")
                m_damage = monster["atk"] + random.randint(-1, 2)
                player["hp"] -= m_damage
                print(f"💥 {monster['name']}の こうげき！ {player['name']}は {m_damage}のダメージ！")

        else:
            print("1〜3の数字を入力してください。")
            continue

        if player["hp"] <= 0:
            print(f"\n💀 {player['name']}は たおれてしまった...")
            print("=== GAME OVER ===")
            return False  # ゲームオーバー


# --- 3. メイン処理（冒険のループ） ---
def main():
    print("==================================")
    print("     Python CLI RPG へ ようこそ！  ")
    print("==================================")

    player = {
        "name": "勇者",
        "hp": 50,
        "max_hp": 50,
        "atk": 10,
        "potions": 3,
        "exp": 0
    }

    monsters_list = load_monsters()

    while True:
        print(f"\n【冒険中】 HP:{player['hp']}/{player['max_hp']} | ポーション:{player['potions']} | 経験値:{player['exp']}")
        print("1: たんさくする | 2: ステータスをみる | 3: 冒険をやめる")
        menu = input("コマンドを選んでください (1-3): ")

        if menu == "1":
            print("\n🚶 勇者は ダンジョンを 歩き回った...")
            # 50%の確率でモンスターとエンカウント
            if random.random() < 0.5:
                # ランダムに敵を1体選ぶ
                m_data = random.choice(monsters_list)
                is_alive = battle(player, m_data)
                
                # 敗北したらゲームオーバー（メインループ終了）
                if not is_alive:
                    break
            else:
                print("🍃 なにも おこらなかった。")

        elif menu == "2":
            print("\n--- 勇者のステータス ---")
            print(f"名前: {player['name']}")
            print(f"HP  : {player['hp']} / {player['max_hp']}")
            print(f"攻撃力: {player['atk']}")
            print(f"所持ポーション: {player['potions']}個")
            print(f"獲得経験値: {player['exp']} EXP")
            print("------------------------")

        elif menu == "3":
            print("\n👋 冒険を終了しました。お疲れ様でした！")
            break

        else:
            print("1〜3を選択してください。")


if __name__ == "__main__":
    main()

```

---

## 🎉 1日目のまとめ

お疲れ様でした！これで**CUIテキストRPGが完成**しました！

本日の学習で身につけたこと：

1. **辞書型 (`dict`)** によるステータス管理
2. **`while` ループ と `if` 分岐** によるゲームのロジック構築
3. **`json` ファイル** を使ったプログラムとデータの分離
4. **関数の定義（`def`）** とデータの受け渡し

明日の **2日目（Pyxel編）** では、今日作成した `player` 辞書や `monsters` JSONの仕組みを **そのまま使いながら、ドット絵のマップを歩き回る2DグラフィックRPGへと進化** させます！お楽しみに！

---