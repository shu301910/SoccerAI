import pandas as pd
import random

# CSVファイルからデータを読み込む
team1_data = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\team1.csv")
team2_data = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\team2.csv")

# チーム1のデータ例を表示
print("チーム1の選手データ:")
print(team1_data)

# チーム2のデータ例を表示
print("チーム2の選手データ:")
print(team2_data)

# チーム1のデータを更新
team_stats1 = {
    '過去の勝率': 0.89,     # 勝率89%
    '試合数': 9,            # 試合数9
    '得点数': 28,           # 28得点
    '失点数': 9,            # 9失点
    '平均支配率': 68.0      # 平均支配率68%
}

# チーム2のデータを更新
team_stats2 = {
    '過去の勝率': 0.65,     # 勝率65%
    '試合数': 12,           # 試合数12
    '得点数': 28,           # 28得点
    '失点数': 15,           # 15失点
    '平均支配率': 52.0      # 平均支配率54%
}

# チームの強さを計算する関数
def calculate_team_strength(player_data, team_data):
    attack_strength = 0
    defense_strength = 0
    stamina_total = 0

    # 選手データのループ処理
    for index, player in player_data.iterrows():
        attack_strength += player['オフェンスセンス'] + player['ボールコントロール'] + player['決定力']
        defense_strength += player['ディフェンスセンス'] + player['守備意識'] + player['ボール奪取']
        stamina_total += player['スタミナ']
    
    # チームデータを考慮
    team_past_performance = team_data['過去の勝率']
    team_attack_bonus = team_past_performance * 10  # 勝率に応じたボーナス
    team_defense_bonus = team_past_performance * 10  # 勝率に応じた守備ボーナス
    
    attack_strength += team_attack_bonus
    defense_strength += team_defense_bonus
    
    return attack_strength, defense_strength, stamina_total

# 天気を考慮した試合結果シミュレーション
def simulate_match_with_weather(team1_data, team2_data, player_data_team1, player_data_team2, weather):
    # 天候による影響を設定
    weather_effects = {
        '晴れ': {'attack_multiplier': 1.0, 'defense_multiplier': 1.0, 'stamina_multiplier': 1.0},
        '雨': {'attack_multiplier': 0.9, 'defense_multiplier': 1.1, 'stamina_multiplier': 0.9},
        '曇り': {'attack_multiplier': 0.95, 'defense_multiplier': 1.05, 'stamina_multiplier': 0.95}
    }

    weather_effect = weather_effects[weather]

    # 各チームの強さを計算
    team1_attack, team1_defense, team1_stamina = calculate_team_strength(player_data_team1, team1_data)
    team2_attack, team2_defense, team2_stamina = calculate_team_strength(player_data_team2, team2_data)

    # 天候による影響を適用
    team1_attack *= weather_effect['attack_multiplier']
    team1_defense *= weather_effect['defense_multiplier']
    team1_stamina *= weather_effect['stamina_multiplier']

    team2_attack *= weather_effect['attack_multiplier']
    team2_defense *= weather_effect['defense_multiplier']
    team2_stamina *= weather_effect['stamina_multiplier']

    # 勝率計算、各チームの得点を0から5の範囲に収める
    team1_goals = max(0, min(5, round((team1_attack - team2_defense) / 100 + random.uniform(-1, 1))))
    team2_goals = max(0, min(5, round((team2_attack - team1_defense) / 100 + random.uniform(-1, 1))))

    # 結果出力
    print(f"天候: {weather}")
    print(f"チーム1 {team1_goals} - {team2_goals} チーム2")

    if team1_goals > team2_goals:
        print(f"勝者: チーム1")
    elif team2_goals > team1_goals:
        print(f"勝者: チーム2")
    else:
        print("引き分け")

# 天気をランダムに設定するためにリストを作成
weather_conditions = ['晴れ'] * 5 + ['曇り'] * 3 + ['雨'] * 2  # 晴れが出やすい

# ランダムに天候を選択
random_weather = random.choice(weather_conditions)

# シミュレーションを実行
simulate_match_with_weather(team_stats1, team_stats2, team1_data, team2_data, random_weather)
