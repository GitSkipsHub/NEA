from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
import bcrypt

from bff.enum import (BattingStyle, BowlingStyle, PlayerRole, TimePeriod,
                      HowOut, MatchType, MatchFormat, Venue, TossResult, Result)

#Create classes selected team and team generator

@dataclass
class Account:
    username: str
    password: str
    hashed_password: str
    created_date: datetime = field(default_factory=datetime.now)

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    @staticmethod
    def verify_password(password: str, hash_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))

@dataclass
class Player:
    #Player Details
    username: str
    first_name: str
    last_name: str
    date_of_birth: str
    player_role: PlayerRole
    batting_style: BattingStyle
    bowling_style: BowlingStyle
    #Player Stats Initialised
    matches: int = 0
    innings: int = 0
    runs_scored: int = 0
    balls: int = 0
    fours: int = 0
    sixes: int = 0
    overs: float = 0.0
    maidens: int = 0
    runs_conceded: int = 0
    wickets: int = 0
    wides: int = 0
    no_balls: int = 0
    catches: int = 0
    runouts: int = 0
    stumpings: int = 0
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


    def to_database(self) -> Dict: #Turns Python Object to Dictionary --> Key: Value
        return{
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "player_role": self.player_role,
            "batting_style": self.batting_style,
            "bowling_style": self.bowling_style,
            "matches": self.matches,
            "innings": self.innings,
            "runs_scored": self.runs_scored,
            "balls": self.balls ,
            "fours": self.fours,
            "sixes": self.sixes,
            "overs": self.overs,
            "maidens": self.maidens,
            "runs_conceded": self.runs_conceded,
            "wickets": self.wickets,
            "wides": self.wides,
            "no_balls": self.no_balls,
            "catches": self.catches,
            "runouts": self.runouts,
            "stumpings": self.stumpings,
            "created_date": self.created_date,
            "last_updated": self.last_updated
        }

    @staticmethod
    def from_database(data: Dict) -> 'Player': #Gets Player Data from Database and converts to Player object
        return Player(
            username=data.get("username"),
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            date_of_birth=data.get("dateOfBirth"),
            player_role=PlayerRole[data.get("playerRole")],
            batting_style=BattingStyle[data.get("battingStyle")],
            bowling_style=BowlingStyle[data.get("bowlingStyle")],
            matches=data.get("matches", 0),
            innings=data.get("innings", 0),
            runs_scored=data.get("runs_scored", 0),
            balls=data.get("balls", 0),
            fours=data.get("fours, 0"),
            sixes=data.get("sixes", 0),
            overs=data.get("overs", 0),
            maidens=data.get("maidens", 0),
            runs_conceded=data.get("runs_conceded", 0),
            wickets=data.get("wickets", 0),
            wides=data.get("wides", 0),
            no_balls=data.get("no_balls", 0),
            catches=data.get("catches", 0),
            stumpings=data.get("stumpings", 0),
            runouts=data.get("runouts", 0),
        )

@dataclass
class Batting:
    player_id: str
    player_name: str
    pos: int
    howOut: HowOut
    fielder: int
    bowler: int
    runs: int
    balls: int
    fours: int
    sixes: int

@dataclass
class Bowling:
    player_id: str
    player_name: str
    pos: int
    overs: float
    maidens: int
    runs: int
    wickets: int
    wides: int
    noBalls: int

@dataclass
class Fielding:
    player_id: str
    player_name: str
    catches: int
    runouts: int
    stumpings: int

@dataclass
class Scorecard:
    subtotal: int
    extras: int
    total: int
    byes_conceded: int
    leg_byes_conceded: int
    penalties_conceded: int
    batting_overs: float
    bowling_overs: float
    batting: List[Batting]
    bowling: List[Bowling]
    fielding: List[Fielding]

@dataclass
class Match:
    username: str
    match_date: datetime
    match_format: MatchFormat
    match_type: MatchType
    venue: Venue
    ground_name: str
    opposition: str
    toss: TossResult
    result: Result
    period: TimePeriod
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    scorecard = Scorecard


    def to_database(self) -> Dict:
        return{
            "username": self.username,
            "match_data": self.match_date,
            "match_format": self.match_format,
            "match_type": self.match_type,
            "venue": self.venue,
            "ground_name": self.ground_name,
            "opposition": self.opposition,
            "toss": self.toss,
            "result": self.result,
            "period": self.period,
            "created_date": self.created_date,
            "last_updated": self.last_updated,
            "scorecard": {
                "subtotal": self.scorecard.subtotal,
                "extras": self.scorecard.extras,
                "total": self.scorecard.total,
                "byes_conceded": self.scorecard.byes_conceded,
                "leg_byes_conceded": self.scorecard.leg_byes_conceded,
                "penalties_conceded": self.scorecard.penalties_conceded,
                "batting_overs": self.scorecard.batting_overs,
                "bowling_overs": self.scorecard.bowling_overs,
                "batting": [vars(b) for b in self.scorecard.batting],
                "bowling": [vars(b) for b in self.scorecard.bowling],
                "fielding": [vars(f) for f in self.scorecard.fielding]
            }
        }

    @staticmethod
    def from_database(data: Dict) -> 'Match':
        return Match(
            username=data.get("username"),
            match_date=data.get("match_date"),
            match_format=MatchFormat[data.get("match_format")],
            match_type=MatchType[data.get("match_type")],
            venue=Venue[data.get("venue")],
            ground_name=data.get("ground_name"),
            opposition=data.get("opposition"),
            toss=TossResult[data.get("TossResult")],
            result=Result[data.get("result")],
            period=TimePeriod[data.get("period")],

            #Return Scorecard + Batting, Bowling, Fielding??

        )


@dataclass
class SelectedTeam:
    username: str
    players: List[Dict]
    created_date: datetime = field(default_factory=datetime.now)


    #players



