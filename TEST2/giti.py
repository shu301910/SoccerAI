import pandas as pd
import random

# CSVからチームデータの読み込み
team1_data = pd.read_csv(C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\HomeTeam.xlsx)
team2_data = pd.read_csv(C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\AweyTeam.xlsx)

# チームの統計データ
team_stats1 = {'過去の勝率': 0.89, '試合数': 9, '得点数': 28, '失点数': 9, '平均支配率': 68.0}
team_stats2 = {'過去の勝率': 0.65, '試合数': 12, '得点数': 28, '失点数': 15, '平均支配率': 52.0}

# ランダムに能力を上昇
def random_boost_team_ability(team_data, boost_value=2):
    for index, player in team_data.iterrows():
        if random.random() < 0.5:  # 50%の確率で+2
            team_data.loc[index, 'オフェンスセンス'] += boost_value
            team_data.loc[index, 'ディフェンスセンス'] += boost_value
            team_data.loc[index, 'スタミナ'] += boost_value
    return team_data

# ポゼッションとカウンタースタイルを反映
def calculate_team_strength(player_data, team_data, style="possession"):
    attack_strength = 0
    defense_strength = 0
    stamina_total = 0

    for index, player in player_data.iterrows():
        attack_strength += player['オフェンスセンス'] + player['ボールコントロール'] + player['決定力']
        defense_strength += player['ディフェンスセンス'] + player['守備意識'] + player['ボール奪取']
        stamina_total += player['スタミナ']
    
    team_past_performance = team_data['過去の勝率']
    if style == "possession":
        attack_strength *= 1.1
        defense_strength *= 0.9
    elif style == "counter":
        attack_strength *= 0.9
        defense_strength *= 1.1
    
    team_attack_bonus = team_past_performance * 10
    team_defense_bonus = team_past_performance * 10
    attack_strength += team_attack_bonus
    defense_strength += team_defense_bonus

    return attack_strength, defense_strength, stamina_total

# シミュレーション実行関数
def simulate_match(team1_data, team2_data, player_data_team1, player_data_team2, duration=90, increment=10):
    team1_data_boosted = random_boost_team_ability(player_data_team1)
    team2_data_boosted = random_boost_team_ability(player_data_team2)

    team1_attack, team1_defense, team1_stamina = calculate_team_strength(team1_data_boosted, team1_data, "possession")
    team2_attack, team2_defense, team2_stamina = calculate_team_strength(team2_data_boosted, team2_data, "counter")

    team1_goals = 0
    team2_goals = 0

    for minute in range(0, duration + 1, increment):
        team1_event_chance = team1_attack / (team1_attack + team2_defense)
        team2_event_chance = team2_attack / (team2_attack + team1_defense)

        if random.random() < team1_event_chance:
            team1_goals += 1 if random.random() < 0.05 else 0
            print(f"{minute}分: チーム1が攻撃し得点のチャンス！現在のスコア チーム1 {team1_goals} - チーム2 {team2_goals}")
        elif random.random() < team2_event_chance:
            team2_goals += 1 if random.random() < 0.05 else 0
            print(f"{minute}分: チーム2が反撃し得点のチャンス！現在のスコア チーム1 {team1_goals} - チーム2 {team2_goals}")
        else:
            print(f"{minute}分: 両チームが中盤でボールを奪い合い、特に大きな動きはなし。")

    # 最終結果出力
    print(f"試合終了 - 最終スコア: チーム1 {team1_goals} - チーム2 {team2_goals}")
    if team1_goals > team2_goals:
        print("チーム1の勝利！")
    elif team2_goals > team1_goals:
        print("チーム2の勝利！")
    else:
        print("引き分け！")

# 実行
simulate_match(team_stats1, team_stats2, team1_data, team2_data)
