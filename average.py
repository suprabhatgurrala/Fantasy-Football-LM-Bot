# #Script to calculate the score for Team Average
import re
import sys

from bs4 import BeautifulSoup
import urllib.request


def data(url):
    r = urllib.request.urlopen(url).read()
    return BeautifulSoup(r, "html.parser")


def week_scores(week, league_id = 565232):
    url = "http://games.espn.go.com/ffl/scoreboard?leagueId=" + str(league_id) + "&scoringPeriodId=" + str(week)
    soup = data(url)
    matchup_tables = soup.find_all("table", {"class": "ptsBased matchup"})
    scores = {}
    for table in matchup_tables:
        for row in table:
            team = row.find("span", {"class": re.compile("abbrev")})
            score = row.find("td", {"class": re.compile("score")})
            if score is not None and team is not None:
                team_name = team.text
                team_name = re.sub('[()]', '', team_name)
                scores[team_name] = float(score['title'])
    return scores


def week_average(week_scores_dict):
    total = 0
    count = 0
    for team in week_scores_dict:
        if team != 'AVG':
            total += week_scores_dict[team]
            count += 1
    return round(total / count, 2)


def average_team_updated(week, league_id = 565232):
    scores = week_scores(week, league_id)
    actual_score = scores['AVG']
    average_score = week_average(scores)
    if abs(average_score - actual_score) < 0.1:
        print("Accurate. Team Average score: " + str(actual_score) + " Calculated average score: " + str(average_score))
    else:
        print("Not accurate. Team Average score: " + str(actual_score) + " Calculated average score: "
              + str(average_score))

sys_args = sys.argv

if sys_args is not None:
    num_args = len(sys_args)
    if num_args == 2:
        week = sys_args[1]
        print(average_team_updated(week))
    elif num_args == 3:
        week = sys_args[1]
        league_id = sys_args[2]
        print(average_team_updated(week_scores(week, league_id)))
    else:
        print("Provide the week as an argument.")

