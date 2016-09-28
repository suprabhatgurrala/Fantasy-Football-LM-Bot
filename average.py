# #Script to calculate the score for Team Average
import re

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
        if team is not 'AVG':
            total += week_scores_dict[team]
            count += 1
    return round(total / count, 2)


def average_team_updated(week, league_id = 565232):
    scores = week_scores(week, league_id)
    actual_score = scores['AVG']
    average_score = week_average(scores)
    if abs(average_score - actual_score) < 0.1:
        print("Team Average has an accurate score of " + str(actual_score))
    else:
        print("Team Average does not have an accurate score. It should be " + str(average_score))

print(week_average(week_scores(3)))
print(average_team_updated(3))
