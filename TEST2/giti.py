# Adjust the function to ensure it simulates exactly 90 minutes
def simulate_match_90min_with_result(team1, team2, kickoff_player_name, total_intervals=9, interval_duration=10):
    movement_log = []
    team1_goals, team2_goals = 0, 0  # Goal counters for each team
    team_in_possession = team2  # Start with Team 2 (counter-attack team) in possession
    current_zone = 'midfield'  # Start in midfield
    time_elapsed = 0  # Total game time in minutes

    # Initialize kickoff by specified player
    movement_log.append(f"Kickoff by {kickoff_player_name}.")

    for interval in range(total_intervals):  # Total of 9 intervals (90 minutes / 10 minutes each)
        actions_in_interval = random.randint(3, 5)  # Define actions per interval
        for _ in range(actions_in_interval):
            # Midfield actions: Possession team emphasizes passing, counter team focuses on fast transitions
            if current_zone == 'midfield':
                if team_in_possession == team1:  # Possession strategy for Team 1
                    midfielder = random.choice([p for p in team_in_possession if 'MF' in p['ポジション']])
                    if 'グラウンダーパス' in midfielder and random.random() < (midfielder['グラウンダーパス'] / 100):  # Possession focus: pass success rate
                        movement_log.append(f"{time_elapsed}min: {midfielder['名前']} successfully passes in midfield.")

                        # Opposing team's interception attempt
                        defenders = [p for p in team2 if 'DF' in p['ポジション']]
                        if defenders and 'ディフェンスセンス' in defenders[0] and random.random() < (defenders[0]['ディフェンスセンス'] / 100):  # Interception based on defense skill
                            defender = random.choice(defenders)
                            movement_log.append(f"{time_elapsed}min: {defender['名前']} intercepts and initiates a counter-attack.")
                            team_in_possession = team2  # Switch to counter team in possession
                            current_zone = 'forward'
                            continue

                        # Move to forward zone if possession is maintained
                        if random.random() < 0.5:  # Higher chance to progress to forward area
                            current_zone = 'forward'
                            movement_log.append(f"{time_elapsed}min: {midfielder['名前']} advances play to forward zone.")
                    else:
                        movement_log.append(f"{time_elapsed}min: {midfielder['名前']}'s pass failed, possession lost.")
                        team_in_possession = team2  # Switch possession to counter team

                elif team_in_possession == team2:  # Counter-attack strategy for Team 2
                    midfielder = random.choice([p for p in team_in_possession if 'MF' in p['ポジション']])
                    if 'スピード' in midfielder and random.random() < (midfielder['スピード'] / 100):  # Counter focus: speed and quick passes
                        movement_log.append(f"{time_elapsed}min: {midfielder['名前']} quickly moves the ball forward on counter.")
                        current_zone = 'forward'
                    else:
                        movement_log.append(f"{time_elapsed}min: {midfielder['名前']}'s counter attempt halted, possession switches.")
                        team_in_possession = team1  # Possession returns to Team 1
                        current_zone = 'midfield'

            elif current_zone == 'forward':
                # Possession team creates shooting opportunities
                forwards = [p for p in team_in_possession if 'FW' in p['ポジション']]
                if forwards:
                    shooter = random.choice(forwards)
                    if '決定力' in shooter and random.random() < (shooter['決定力'] / 100):  # Shot success based on finishing skill
                        movement_log.append(f"{time_elapsed}min: Goal by {shooter['名前']}!")
                        if team_in_possession == team1:
                            team1_goals += 1
                        else:
                            team2_goals += 1
                        current_zone = 'midfield'  # Reset to midfield after goal
                        team_in_possession = team2 if team_in_possession == team1 else team1  # Switch possession
                        continue  # Move to next action

                    else:
                        # Shot saved, reset to midfield
                        movement_log.append(f"{time_elapsed}min: {shooter['名前']}'s shot was saved.")
                        current_zone = 'midfield'
                        team_in_possession = team1 if team_in_possession == team2 else team2  # Switch possession

        # Increment total time by the interval duration
        time_elapsed += interval_duration
        if time_elapsed >= 90:  # End simulation at 90 minutes
            break

    # Append final score to the log
    movement_log.append(f"Final Score: Team 1 {team1_goals} - {team2_goals} Team 2")
    if team1_goals > team2_goals:
        movement_log.append("Team 1 wins!")
    elif team2_goals > team1_goals:
        movement_log.append("Team 2 wins!")
    else:
        movement_log.append("The match ends in a draw.")

    return movement_log

# Run the adjusted simulation for 90 minutes
simulation_90min_with_result = simulate_match_90min_with_result(team1_players, team2_players, "ラウタロ・マルティネス")
simulation_90min_with_result
