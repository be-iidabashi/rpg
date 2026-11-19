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