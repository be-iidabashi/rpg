import random
import time
import json
import os

# ==========================================
# 演出用ヘルパー関数
# ==========================================
def slow_print(text, delay=0.03):
    """1文字ずつドラマチックに表示する"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def print_line():
    print("-" * 40)


# ==========================================
# データ読み込み処理
# ==========================================
def load_monsters():
    """モンスターデータをJSONから読み込む（ファイルがなければデフォルトを使用）"""
    default_data = [
        {"name": "スライム", "hp": 20, "max_hp": 20, "atk": 6, "exp": 10},
        {"name": "ゴブリン", "hp": 35, "max_hp": 35, "atk": 10, "exp": 25},
        {"name": "オーク", "hp": 50, "max_hp": 50, "atk": 15, "exp": 45},
        {"name": "ドラゴン（BOSS）", "hp": 100, "max_hp": 100, "atk": 22, "exp": 100}
    ]
    
    # cli_monsters.json が同階層にあれば読み込む
    if os.path.exists("cli_monsters.json"):
        try:
            with open("cli_monsters.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
            
    return default_data


# ==========================================
# バトルロジック
# ==========================================
def battle(player, monster):
    """1対1の戦闘処理（プレイヤー勝利でTrue, 敗北/逃亡でFalse）"""
    print_line()
    slow_print(f"あやしい けはいい！ {monster['name']} が あらわれた！")
    print_line()
    time.sleep(0.5)

    while player["hp"] > 0 and monster["hp"] > 0:
        # ステータス表示
        print(f"\n【{player['name']}】 HP: {player['hp']}/{player['max_hp']} | ポーション: {player['potions']}個")
        print(f"【{monster['name']}】 HP: {monster['hp']}/{monster['max_hp']}")
        print_line()
        
        # コマンド選択
        print("行動を選んでください:")
        print("1: たたかう")
        print("2: ポーションを使う（HP30回復）")
        print("3: にげる")
        choice = input(">> ")
        print_line()

        # --- 1: たたかう ---
        if choice == "1":
            # プレイヤーの攻撃（ランダムでブレを持たせる）
            damage = player["atk"] + random.randint(-2, 3)
            # 15%の確率でクリティカル
            if random.random() < 0.15:
                damage = int(damage * 1.5)
                slow_print(f"★ かいしんの いちげき！ {monster['name']} に {damage} のダメージ！")
            else:
                slow_print(f"{player['name']} の こうげき！ {monster['name']} に {damage} のダメージ！")
            
            monster["hp"] -= damage

            # モンスター撃破判定
            if monster["hp"] <= 0:
                slow_print(f"\n{monster['name']} を たおした！")
                slow_print(f"けいけんち {monster['exp']} pt を かくとく！")
                player["exp"] += monster["exp"]
                return True

        # --- 2: 回復 ---
        elif choice == "2":
            if player["potions"] > 0:
                heal = 30
                player["hp"] = min(player["max_hp"], player["hp"] + heal)
                player["potions"] -= 1
                slow_print(f"{player['name']} は ポーションを つかった！ HPが {heal} かいふくした！")
            else:
                slow_print("ポーションを もっていない！ ターンを むだにした！")

        # --- 3: にげる ---
        elif choice == "3":
            if random.random() < 0.5:
                slow_print(f"{player['name']} は うまく にげだした！")
                return False
            else:
                slow_print(f"{player['name']} は にげだそうとしたが つかまってしまった！")

        else:
            slow_print("ただしい コマンドを 入力してください。")
            continue

        # --- モンスターの反撃 ---
        time.sleep(0.5)
        m_damage = monster["atk"] + random.randint(-1, 2)
        
        # 10%の確率で攻撃がミス
        if random.random() < 0.10:
            slow_print(f"{monster['name']} の こうげき！ しかし こうげきは はずれた！")
        else:
            slow_print(f"{monster['name']} の こうげき！ {player['name']} は {m_damage} のダメージを うけた！")
            player["hp"] -= m_damage

        # プレイヤー敗北判定
        if player["hp"] <= 0:
            slow_print(f"\n{player['name']} は たおれてしまった…")
            return False

        time.sleep(0.5)


# ==========================================
# メインゲームループ
# ==========================================
def main():
    print_line()
    slow_print("=== コマンドLINE ダンジョンへ ようこそ！ ===")
    print_line()
    
    player_name = input("勇者の なまえを 入力してください: ").strip()
    if not player_name:
        player_name = "ゆうしゃ"

    # プレイヤーの初期ステータス
    player = {
        "name": player_name,
        "hp": 50,
        "max_hp": 50,
        "atk": 10,
        "potions": 3,
        "exp": 0
    }

    monsters = load_monsters()
    slow_print(f"\nようこそ、{player['name']}！ 全 {len(monsters)} 階の ダンジョンに いどみます！\n")
    time.sleep(1)

    # ダンジョン攻略ループ
    for i, monster_data in enumerate(monsters, 1):
        slow_print(f"\n【 {i} 階層目 に しんにゅう… 】")
        time.sleep(0.8)

        # 辞書のディープコピー（モンスターのHP初期化のため）
        current_monster = monster_data.copy()
        
        # バトル実行
        victory = battle(player, current_monster)

        if not victory:
            if player["hp"] <= 0:
                print_line()
                slow_print("【 GAME OVER 】 冒険は ここで おわってしまった…")
                print_line()
                return
            else:
                slow_print("ダンジョンから 脱出しました。")
                break

        # 階層クリアごとのボーナス処理
        if i < len(monsters):
            slow_print("\nクリアボーナス！ HPが 15 かいふくし、ポーションを 1個 ゲットした！")
            player["hp"] = min(player["max_hp"], player["hp"] + 15)
            player["potions"] += 1
            time.sleep(1)

    # 全クリア判定
    if player["hp"] > 0 and i == len(monsters):
        print_line()
        slow_print("★☆★ CONGRATULATIONS! ★☆★")
        slow_print(f"{player['name']} は 見事に ダンジョンを はおうした！")
        slow_print(f"最終かくとく けいけんち: {player['exp']} pt")
        print_line()

if __name__ == "__main__":
    main()