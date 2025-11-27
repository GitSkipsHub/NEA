import math

def convert_overs_to_balls(over):
    split = math.modf(over)
    total_balls = (split[0]*10) + (split[1]*6)
    return int(total_balls)

def batting_average(total_runs_scored, total_innings, not_outs):
    bat_average = round(total_runs_scored/(total_innings-not_outs), 2)
    return bat_average

def batting_sr(total_runs_scored, total_balls_faced):
    bat_sr = round(total_runs_scored/total_balls_faced, 2)
    return bat_sr

def bowling_average(total_runs_conceded, total_wickets):
    bowl_average = round(total_runs_conceded/total_wickets, 2)
    return bowl_average

def bowling_sr(total_balls_bowled, total_wickets):
    bowl_sr = round(total_balls_bowled/total_wickets, 2)
    return bowl_sr

def economy_rate(total_runs_conceded, overs):
    econ_rate = round(total_runs_conceded/overs, 2)
    return econ_rate








