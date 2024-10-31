import pandas as pd
import random

# CSVファイルから選手データとフォーメーションデータを読み込む
team1_players = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\sennsyu - チーム1.csv")
team2_players = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\sennsyu - チーム2.csv")
team1_formation = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\サッカーコート - BA.csv")
team2_formation = pd.read_csv(r"C:\Users\kshus\OneDrive\ドキュメント\GitHub\SoccerAI\TEST2\サッカーコート - RE.csv")

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

# 90分間試合をシミュレーションする関数
def simulate_90_minute_match(player_data_team1, player_data_team2, team1_data, team2_data):
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
                    # チーム1のミッドフィールダーがパスを試みる
                    midfielders_team1 = player_data_team1[player_data_team1['ポジション'].isin(['MF', 'LMF', 'CMF', 'DMF', 'RMF'])]
                    if not midfielders_team1.empty:
                        midfielder = random.choice(midfielders_team1.to_dict('records'))
                        
                        # 味方同士のパスを少なめにし、ある程度で攻撃に移行
                        pass_success_chance = (midfielder['グラウンダーパス'] + midfielder['フライパス']) / 180
                        if random.random() < pass_success_chance:
                            movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} がチーム内でパスを回しました。")
                        else:
                            movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} のパスが失敗し、ボールがチーム2に渡りました。")
                            team_in_possession = player_data_team2  # パス失敗で攻守交替

                    # 一定確率で前線にパスして攻撃
                    if random.random() < 0.5:
                        current_zone = 'forward'
                        movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} が前線にパスを出しました。")
                        continue  # 必ず次のループへ進む

                else:
                    # チーム2のミッドフィールダーの行動
                    midfielders_team2 = player_data_team2[player_data_team2['ポジション'].isin(['MF', 'LMF', 'CMF', 'DMF', 'RMF'])]
                    if not midfielders_team2.empty:
                        midfielder = random.choice(midfielders_team2.to_dict('records'))
                        
                        if random.random() < (midfielder['ドリブル'] / 100):
                            movement_log.append(f"{time_elapsed}min: {midfielder['選手名']} がドリブル成功しました。")
                            
                            # チーム1のディフェンダーがインターセプトを試みる
                            defenders_team1 = player_data_team1[player_data_team1['ポジション'].isin(['DF', 'LSB', 'RSB', 'CB'])]
                            if not defenders_team1.empty:
                                defender = random.choice(defenders_team1.to_dict('records'))
                                intercept_chance = defender['ディフェンスセンス'] / 150
                                if random.random() < intercept_chance:
                                    movement_log.append(f"{time_elapsed}min: {defender['選手名']} がインターセプトしました。")
                                    team_in_possession = player_data_team1  # ボールを奪取
                                    current_zone = 'midfield'
                                    continue

            elif current_zone == 'forward':
                # フォワードゾーンでの行動を制御（シュート or パス）
                forwards_team2 = player_data_team2[player_data_team2['ポジション'] == 'FW']
                if not forwards_team2.empty:
                    shooter = random.choice(forwards_team2.to_dict('records'))
                    
                    # シュートするかパスするかをランダムに選択
                    if random.random() < 0.8:  # 80%の確率でシュートを試みる
                        if random.random() < (shooter['決定力'] / 100):  # シュート成功
                            team2_score += 1
                            movement_log.append(f"{time_elapsed}min: ゴール！ {shooter['選手名']} がシュートを決めました！ チーム2が得点しました。")
                            # ゴール後、チーム1がキックオフで再開
                            current_zone = 'midfield'
                            team_in_possession = player_data_team1
                            movement_log.append(f"{time_elapsed}min: チーム1のロベルト・レヴァンドフスキによるキックオフで試合再開。")
                        else:
                            movement_log.append(f"{time_elapsed}min: {shooter['選手名']} のシュートは失敗しました。")
                            current_zone = 'midfield'
                            team_in_possession = player_data_team1  # 攻守交替
                    else:
                        # パスを選択した場合、フォワードゾーンでパスを試みる
                        pass_success_chance = (shooter['グラウンダーパス'] + shooter['フライパス']) / 200
                        if random.random() < pass_success_chance:
                            movement_log.append(f"{time_elapsed}min: {shooter['選手名']} がフォワードゾーンでパス成功。攻撃継続中。")
                        else:
                            movement_log.append(f"{time_elapsed}min: {shooter['選手名']} のフォワードゾーンでのパスが失敗しました。")
                            current_zone = 'midfield'
                            team_in_possession = player_data_team1  # 攻守交替

    # 試合終了メッセージ
    movement_log.append(f"試合終了！90分間の試合が終了しました。 最終スコア: チーム1 {team1_score} - チーム2 {team2_score}")
    return movement_log

# 実行例
results = simulate_90_minute_match(team1_players, team2_players, team_stats1, team_stats2)
for line in results:
    print(line)
