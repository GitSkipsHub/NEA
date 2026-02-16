from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Tuple
import bcrypt

from bff.enums import (BattingStyle, BowlingStyle, PlayerRole, TimePeriod,
                       HowOut, MatchType, MatchFormat, Venue, TossResult, Result)

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

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data:Dict) -> 'Account':
        return cls(**data)

@dataclass
class Player:
    #Player Details
    username: str
    player_id: str
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
    #Logs
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict: #Turns Python Object to Dictionary --> Key: Value
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Player': #Gets Player Data from Database and converts to Player object
        return cls(**data)

@dataclass
class Batting:
    player_id: str
    player_name: str
    pos: int
    how_out: HowOut
    fielder: str
    bowler: str
    runs_scored: int
    balls: int
    fours: int
    sixes: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data:Dict) -> 'Batting':
        return cls(**data)

@dataclass
class Bowling:
    player_id: str
    player_name: str
    pos: int
    overs: float
    maidens: int
    runs_conceded: int
    wickets: int
    wides: int
    no_balls: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data:Dict) -> 'Bowling':
        return cls(**data)

@dataclass
class Fielding:
    player_id: str
    player_name: str
    catches: int
    runouts: int
    stumpings: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data:Dict) -> 'Fielding':
        return cls(**data)

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

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data:Dict) -> 'Scorecard':
        data["batting"]=[Batting.from_dict(x) for x in data["batting"]]
        data["bowling"]=[Bowling.from_dict(x) for x in data["bowling"]]
        data["fielding"]=[Fielding.from_dict(x) for x in data["fielding"]]
        return cls(**data)

@dataclass
class Match:
    username: str
    match_id: str
    match_date: datetime
    match_format: MatchFormat
    match_type: MatchType
    venue: Venue
    ground_name: str
    opposition: str
    toss: TossResult
    result: Result
    scorecard: Scorecard
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Match':
        data["scorecard"] = Scorecard.from_dict(data["scorecard"])
        return cls(**data)

@dataclass
class TeamGenerator:
    time_period: TimePeriod
    no_of_batters: int
    no_of_pacers: int
    no_of_spinners: int
    no_of_all_rounders: int
    no_of_wicketkeepers: int

    def validate_team_composition(self) -> Tuple[bool, str] :
        total = (self.no_of_batters +
                 self.no_of_pacers +
                 self.no_of_spinners +
                 self.no_of_all_rounders
                 + self.no_of_wicketkeepers)

        if total != 11:
            return False, "WARNING Team must have exactly 11 players"

        if self.no_of_batters < 4:
            return False, "WARNING Team Imbalanced - 4 Batters Recommended"

        bowlers = self.no_of_pacers + self.no_of_spinners
        if bowlers < 3:
            return False, "WARNING Team Imbalanced - 3 Bowlers Recommended"

        if self.no_of_all_rounders < 3:
            return False, "WARNING Team Imbalanced - 3 All-Rounders Recommended"

        if self.no_of_wicketkeepers != 1:
            return False, "WARNING Team must have 1 Wicket Keeper"

        return True, ""

@dataclass
class SelectedTeam:
    username: str
    team_id: str
    player_name: str
    player_role: PlayerRole
    matches: int
    batting_runs: int
    batting_avg: float
    batting_sr: float
    overs: float
    bowling_runs: float
    wickets: float
    economy_rate: float
    bowling_avg: float
    bowling_sr: float
    catches: int
    stumpings: int
    runouts: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data:Dict) -> 'SelectedTeam':
        return cls(**data)






