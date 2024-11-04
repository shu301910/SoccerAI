import pandas as pd
import random

# 絶対パスを指定してCSVファイルを読み込む
players_data_path = r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\sennsyu.csv"
formation_data_path = r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\サッカーコート - シート3.csv"

# データの読み込み
players_data = pd.read_csv(players_data_path)
formation_data = pd.read_csv(formation_data_path)

# チームIDを使ってチームごとに選手データを分割
team1_players = players_data[players_data['チームID'] == "チーム1"]
team2_players = players_data[players_data['チームID'] == "チーム2"]

# チーム戦術を設定（ポゼッションとカウンター）
team1_strategy = "ポゼッション"
team2_strategy = "カウンター"

# 90分間試合をシミュレーションする関数
def simulate_match_with_zones(player_data_team1, player_data_team2, team1_strategy, team2_strategy):
    movement_log = []
    team_in_possession = player_data_team1  # Team1からボール保持スタート
    current_zone = 'midfield'
    team1_score = 0
    team2_score = 0

    movement_log.append("キックオフ！ Team1がボールを持って試合が始まります")

    for interval in range(1, 10):  # 90分を10分区切りに
        # 各10分区切りで3〜5回のアクション
        actions_in_interval = random.randint(3, 5)
        for _ in range(actions_in_interval):
            if current_zone == 'midfield':
                if team_in_possession is player_data_team1:
                    pass_success_chance = 0.8 if team1_strategy == "ポゼッション" else 0.5
                    midfielders_team1 = player_data_team1[player_data_team1['ポジション'].str.contains('MF')]
                    if not midfielders_team1.empty:
                        midfielder = random.choice(midfielders_team1.to_dict('records'))
                        if random.random() < pass_success_chance:
                            movement_log.append(f"Team1 {midfielder['選手名']} がパスを成功させました")
                        else:
                            movement_log.append(f"Team1 {midfielder['選手名']} のパスが失敗し、Team2がボールを奪取")
                            team_in_possession = player_data_team2
                        if random.random() < 0.6:
                            current_zone = 'forward'
                            movement_log.append("Team1が前線にパスを送ります")
                else:
                    pass_success_chance = 0.65 if team2_strategy == "カウンター" else 0.5
                    midfielders_team2 = player_data_team2[player_data_team2['ポジション'].str.contains('MF')]
                    if not midfielders_team2.empty:
                        midfielder = random.choice(midfielders_team2.to_dict('records'))
                        if random.random() < pass_success_chance:
                            movement_log.append(f"Team2 {midfielder['選手名']} がパスを成功させました")
                            current_zone = 'forward'
                        else:
                            movement_log.append(f"Team2 {midfielder['選手名']} のパスが失敗し、Team1がボールを奪取")
                            team_in_possession = player_data_team1

            elif current_zone == 'forward':
                if team_in_possession is player_data_team1:
                    # Team1のフォワードを 'FW'、'CF'、'ST' などのポジションで検索
                    forwards_team1 = player_data_team1[player_data_team1['ポジション'].isin(['FW', 'CF', 'ST'])]
                    if not forwards_team1.empty:
                        shooter = random.choice(forwards_team1.to_dict('records'))
                        shot_chance = (shooter['決定力']*0.7) / 100
                        if random.random() < shot_chance:
                            team1_score += 1
                            movement_log.append(f"ゴール！ Team1 {shooter['選手名']} が得点！")
                            team_in_possession = player_data_team2
                            current_zone = 'midfield'
                        else:
                            movement_log.append(f"{shooter['選手名']} のシュートが外れました")
                            current_zone = 'midfield'
                    else:
                        movement_log.append("Team1にフォワードがいないため、攻撃を行えませんでした。")
                        team_in_possession = player_data_team2
                        current_zone = 'midfield'

                else:
                    # Team2のフォワードを 'FW'、'CF'、'ST' などのポジションで検索
                    forwards_team2 = player_data_team2[player_data_team2['ポジション'].isin(['FW', 'CF', 'ST'])]
                    if not forwards_team2.empty:
                        shooter = random.choice(forwards_team2.to_dict('records'))
                        shot_chance = (shooter['決定力']*0.7) / 100
                        if random.random() < shot_chance:
                            team2_score += 1
                            movement_log.append(f"ゴール！ Team2 {shooter['選手名']} が得点！")
                            team_in_possession = player_data_team1
                            current_zone = 'midfield'
                        else:
                            movement_log.append(f"{shooter['選手名']} のシュートが外れました")
                            current_zone = 'midfield'
                    else:
                        movement_log.append("Team2にフォワードがいないため、攻撃を行えませんでした。")
                        team_in_possession = player_data_team1
                        current_zone = 'midfield'

    movement_log.append(f"試合終了。最終スコア: Team1 {team1_score} - Team2 {team2_score}")
    return movement_log

# 実行例
results = simulate_match_with_zones(team1_players, team2_players, team1_strategy, team2_strategy)
for line in results:
    print(line)
