import pandas as pd
import random

# CSVファイルから選手データとフォーメーションデータを読み込む
players_data = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\sennsyu.csv")
team1_formation = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\サッカーコート - BA.csv")
team2_formation = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\サッカーコート - RE.csv")

# チームIDを使ってチームごとに選手データを分割
team1_players = players_data[players_data['チームID'] == "チーム1"]
team2_players = players_data[players_data['チームID'] == "チーム2"]

# チーム戦術を設定（ポゼッションとカウンター）
team1_strategy = "ポゼッション"
team2_strategy = "カウンター"

# チームデータを設定
team_stats1 = {'過去の勝率': 0.89, '試合数': 9, '得点数': 28, '失点数': 9, '平均支配率': 68.0}
team_stats2 = {'過去の勝率': 0.65, '試合数': 12, '得点数': 28, '失点数': 15, '平均支配率': 52.0}

# 90分間試合をシミュレーションする関数
def simulate_90_minute_match(player_data_team1, player_data_team2, team1_data, team2_data, team1_strategy, team2_strategy):
    movement_log = []
    team_in_possession = player_data_team1  # Start with Team 1 in possession
    current_zone = 'midfield'
    time_elapsed = 0
    team1_score = 0
    team2_score = 0

    # Kickoff by Roberto Lewandowski to start the game
    movement_log.append(f"{time_elapsed}min: キックオフ！！ ロベルト・レヴァンドフスキ")

    for interval in range(1, 10):  # 10 intervals to represent 90 minutes (10 min each)
        time_elapsed = interval * 10

        # 3〜5回のアクションを各インターバル内で設定し、アクションの頻度を増やす
        actions_in_interval = random.randint(3, 5)
        
        for _ in range(actions_in_interval):
            if current_zone == 'midfield':
                if team_in_possession is player_data_team1:
                    pass_success_chance = 0.8 if team1_strategy == "ポゼッション" else 0.5

                    midfielders_team1 = player_data_team1[player_data_team1['ポジション'].isin(['MF', 'LMF', 'CMF', 'DMF', 'RMF'])]
                    if not midfielders_team1.empty:
                        midfielder = random.choice(midfielders_team1.to_dict('records'))
                        
                        if random.random() < pass_success_chance:
                            movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} がチーム内でパスを回しました。")
                        else:
                            movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} のパスが失敗し、ボールがチーム2に渡りました。")
                            team_in_possession = player_data_team2  # パス失敗で攻守交替

                    # 前線にパスをして攻撃に移行する確率を上げる
                    if random.random() < 0.6:
                        current_zone = 'forward'
                        movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} が前線にパスを出しました。")
                        continue

                else:
                    pass_success_chance = 0.65 if team2_strategy == "カウンター" else 0.5

                    midfielders_team2 = player_data_team2[player_data_team2['ポジション'].isin(['MF', 'LMF', 'CMF', 'DMF', 'RMF'])]
                    if not midfielders_team2.empty:
                        midfielder = random.choice(midfielders_team2.to_dict('records'))
                        
                        if random.random() < (midfielder['ドリブル'] / 100):
                            movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} がドリブル成功しました。")
                            
                            defenders_team1 = player_data_team1[player_data_team1['ポジション'].isin(['DF', 'LSB', 'RSB', 'CB'])]
                            if not defenders_team1.empty:
                                defender = random.choice(defenders_team1.to_dict('records'))
                                intercept_chance = defender['ディフェンスセンス'] / 200  # インターセプト率を低く設定
                                if random.random() < intercept_chance:
                                    movement_log.append(f"{time_elapsed}min: {defender['選手名']} がインターセプトしました。")
                                    team_in_possession = player_data_team1  # ボールを奪取
                                    current_zone = 'midfield'
                                    continue
                                
                        if random.random() < pass_success_chance:
                            current_zone = 'forward'
                            movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} が前線にパスを出しました。")
                            continue

            elif current_zone == 'forward':
                forwards_team2 = player_data_team2[player_data_team2['ポジション'] == 'FW']
                if not forwards_team2.empty:
                    shooter = random.choice(forwards_team2.to_dict('records'))
                    
                    if random.random() < 0.8:
                        if random.random() < (shooter['決定力'] / 100):
                            team2_score += 1
                            movement_log.append(f"{time_elapsed}min: ゴール！ {shooter['選手名']} がシュートを決めました！ チーム2が得点しました。")
                            current_zone = 'midfield'
                            team_in_possession = player_data_team1
                            movement_log.append(f"{time_elapsed}min: チーム1のロベルト・レヴァンドフスキによるキックオフで試合再開。")
                        else:
                            movement_log.append(f"{time_elapsed}min: {shooter['選手名']} のシュートは失敗しました。")
                            current_zone = 'midfield'
                            team_in_possession = player_data_team1
                    else:
                        pass_success_chance = (shooter['グラウンダーパス'] + shooter['フライパス']) / 150
                        if random.random() < pass_success_chance:
                            movement_log.append(f"{time_elapsed}min: {shooter['選手名']} がフォワードゾーンでパス成功。攻撃継続中。")
                        else:
                            movement_log.append(f"{time_elapsed}min: {shooter['選手名']} のフォワードゾーンでのパスが失敗しました。")
                            current_zone = 'midfield'
                            team_in_possession = player_data_team1

    movement_log.append(f"試合終了！90分間の試合が終了しました。 最終スコア: チーム1 {team1_score} - チーム2 {team2_score}")
    return movement_log

# 実行例
results = simulate_90_minute_match(team1_players, team2_players, team_stats1, team_stats2, team1_strategy, team2_strategy)
for line in results:
    print(line)
