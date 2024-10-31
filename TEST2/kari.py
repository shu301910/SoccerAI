import pandas as pd
import random

# CSVファイルから選手データとフォーメーションデータを読み込む
team1_players = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\sennsyu - チーム1.csv")
team2_players = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\sennsyu - チーム2.csv")
team1_formation = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\HomeTeam.csv")
team2_formation = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\AweyTeam.csv")

# チームデータを設定
team_stats1 = {
    '過去の勝率': 0.89,
    '試合数': 9,
    '得点数': 28,
    '失点数': 9,
    '平均支配率': 68.0
}

team_stats2 = {
    '過去の勝率': 0.65,
    '試合数': 12,
    '得点数': 28,
    '失点数': 15,
    '平均支配率': 52.0
}

# チームの強さを計算する関数
def calculate_team_strength(player_data, team_data):
    attack_strength = 0
    defense_strength = 0
    stamina_total = 0

    for _, player in player_data.iterrows():
        attack_strength += player['オフェンスセンス'] + player['ボールコントロール'] + player['決定力']
        defense_strength += player['ディフェンスセンス'] + player['守備意識'] + player['ボール奪取']
        stamina_total += player['スタミナ']
    
    team_past_performance = team_data['過去の勝率']
    team_attack_bonus = team_past_performance * 10
    team_defense_bonus = team_past_performance * 10
    
    attack_strength += team_attack_bonus
    defense_strength += team_defense_bonus
    
    return attack_strength, defense_strength, stamina_total

# 90分間試合をシミュレーションする関数
def simulate_90_minute_match(player_data_team1, player_data_team2, team1_data, team2_data, kickoff_player_name):
    movement_log = []
    team_in_possession = player_data_team2  # Start with Team 2 in possession
    current_zone = 'midfield'
    time_elapsed = 0
    team1_score = 0
    team2_score = 0

    # Record kickoff by the specified player
    movement_log.append(f"{time_elapsed}min: キックオフ！！ {kickoff_player_name}.")

    for interval in range(1, 10):  # 10 intervals to represent 90 minutes (10 min each)
        time_elapsed = interval * 10

        # 2〜3回のアクションを各インターバル内で設定
        actions_in_interval = random.randint(2, 3)
        
        for _ in range(actions_in_interval):
            if current_zone == 'midfield':
                # チーム2のミッドフィールダーが存在するか確認してから選択
                midfielders_team2 = player_data_team2[player_data_team2['ポジション'].isin(['MF', 'LMF', 'CMF', 'DMF', 'RMF'])]
                if not midfielders_team2.empty:
                    midfielder = random.choice(midfielders_team2.to_dict('records'))
                else:
                    continue

                if random.random() < (midfielder['ドリブル'] / 100):  # Dribble success
                    movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} ドリブル成功しました。")

                    # チーム1のディフェンダーからインターセプトを試みる
                    defenders_team1 = player_data_team1[player_data_team1['ポジション'].isin(['DF', 'LSB', 'RSB', 'CB'])]
                    if not defenders_team1.empty:
                        defender = random.choice(defenders_team1.to_dict('records'))
                        if random.random() < (defender['ディフェンスセンス'] / 100):
                            movement_log.append(f"{time_elapsed}min: {defender['選手名']} がインターセプトしました。")
                            team_in_possession = player_data_team1  # ボールを奪取
                            current_zone = 'midfield'
                            continue

                    if random.random() < 0.6:  # 60% chance to attempt a forward pass
                        current_zone = 'forward'
                        movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} が前線にパスを出しました。")

                else:
                    movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} がドリブル失敗してボールを失いました。")
                    team_in_possession = player_data_team1
                    continue

            elif current_zone == 'forward':
                # Forward attempts shot if in forward zone
                forwards_team2 = player_data_team2[player_data_team2['ポジション'] == 'FW']
                if not forwards_team2.empty:
                    shooter = random.choice(forwards_team2.to_dict('records'))
                    if random.random() < (shooter['決定力'] / 100):  # Shot success
                        team2_score += 1
                        movement_log.append(f"{time_elapsed}min: ゴール！ {shooter['選手名']} がシュートを決めました！ チーム2が得点しました。")
                        current_zone = 'midfield'
                        team_in_possession = player_data_team1  # ボールが再スタート
                    else:
                        movement_log.append(f"{time_elapsed}min: {shooter['選手名']} のシュートは失敗しました。")
                        current_zone = 'midfield'
                        team_in_possession = player_data_team1 if team_in_possession is player_data_team2 else player_data_team2

    movement_log.append(f"試合終了！90分間の試合が終了しました。 最終スコア: チーム1 {team1_score} - チーム2 {team2_score}")
    return movement_log

# 実行例
results = simulate_90_minute_match(team1_players, team2_players, team_stats1, team_stats2, "ラウタロ・マルティネス")
for line in results:
    print(line)
