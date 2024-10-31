import pandas as pd
import random

# 列名のリストを定義
column_names = ['選手名', 'ポジション', 'オフェンスセンス', 'ボールコントロール', 'ドリブル', 'ボールキープ', 
                'グラウンダーパス', 'フライパス', '決定力', 'ヘディング', 'プレースキック', 'カーブ', 
                'スピード', '瞬発力', 'キック力', 'ジャンプ', 'フィジカルコンタクト', 'ボディバランス', 
                'スタミナ', 'ディフェンスセンス', '守備意識', 'ボール奪取', 'アグレッシブネス']

# CSVファイルからデータを読み込む
team1_players = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\sennsyu - チーム1.csv", names=column_names, header=None)
team2_players = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\sennsyu - チーム2.csv", names=column_names, header=None)

# データ型を数値に変換
for col in column_names[2:]:
    team1_players[col] = pd.to_numeric(team1_players[col], errors='coerce')
    team2_players[col] = pd.to_numeric(team2_players[col], errors='coerce')

# チームの統計データを定義
team_stats1 = {'過去の勝率': 0.89, '試合数': 9, '得点数': 28, '失点数': 9, '平均支配率': 68.0}
team_stats2 = {'過去の勝率': 0.65, '試合数': 12, '得点数': 28, '失点数': 15, '平均支配率': 52.0}

# チームのスタイルに応じて強さを計算
def calculate_strength(player_data, team_style="possession"):
    attack, defense = 0, 0
    for _, player in player_data.iterrows():
        attack += player['オフェンスセンス'] + player['ボールコントロール'] + player['決定力']
        defense += player['ディフェンスセンス'] + player['守備意識'] + player['ボール奪取']
    if team_style == "possession":
        attack *= 1.2  # ポゼッションの強化
    elif team_style == "counter":
        defense *= 1.2  # カウンター時の守備強化
    return attack, defense

# パスの進行を追跡する関数
def simulate_pass(team_name, success_rate=0.75, max_passes=4):
    passes = 0
    while passes < max_passes:
        if random.random() < success_rate:
            print(f"{team_name}がパスを成功させた！")
            passes += 1
        else:
            print(f"{team_name}のパスが失敗し、相手チームにボールが奪われた！")
            return False
    print(f"{team_name}がゴールに近づいた！")
    return True

# 試合シミュレーションを実行
def simulate_match(team1, team2, players1, players2, duration=90, step=10):
    team1_attack, team1_defense = calculate_strength(players1, "possession")
    team2_attack, team2_defense = calculate_strength(players2, "counter")

    team1_goals, team2_goals = 0, 0

    for minute in range(0, duration + 1, step):
        team1_chance = (team1_attack * 1.1) / ((team1_attack * 1.1) + (team2_defense * 0.9))
        team2_chance = (team2_attack * 1.1) / ((team2_attack * 1.1) + (team1_defense * 0.9))

        if random.random() < team1_chance:
            print(f"{minute}分: チーム1が攻撃中！")
            if simulate_pass("チーム1"):
                if random.random() < 0.25:  # ゴールの確率を少し上げる
                    team1_goals += 1
                    print(f"チーム1がゴール！現在のスコア - チーム1: {team1_goals}, チーム2: {team2_goals}")
        
        elif random.random() < team2_chance:
            print(f"{minute}分: チーム2が反撃中！")
            if simulate_pass("チーム2"):
                if random.random() < 0.25:
                    team2_goals += 1
                    print(f"チーム2がゴール！現在のスコア - チーム1: {team1_goals}, チーム2: {team2_goals}")
        
        else:
            print(f"{minute}分: 中盤でのボール奪い合い、特に動きなし。")

    print(f"試合終了 - 最終スコア: チーム1 {team1_goals} - チーム2 {team2_goals}")
    if team1_goals > team2_goals:
        print("チーム1の勝利！")
    elif team2_goals > team1_goals:
        print("チーム2の勝利！")
    else:
        print("引き分け！")

# シミュレーションの実行
simulate_match(team_stats1, team_stats2, team1_players, team2_players)