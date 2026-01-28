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
        return{
            "player_id": self.player_id,
            "player_name": self.player_name,
            "pos": self.pos,
            "overs": self.overs,
            "maidens": self.maidens,
            "runs_conceded": self.runs_conceded,
            "wickets": self.wickets,
            "wides": self.wides,
            "no_balls": self.no_balls
        }
    @classmethod
    def from_dict(cls, data:Dict) -> 'Bowling':
        return cls(
            player_id=data.get("player_id"),
            player_name=data.get("player_name"),
            pos=data.get("pos"),
            overs=data.get("overs"),
            maidens=data.get("maidens"),
            runs_conceded=data.get("runs_conceded"),
            wickets=data.get("wickets"),
            wides=data.get("wides"),
            no_balls=data.get("no_balls"),
        )

@dataclass
class Fielding:
    player_id: str
    player_name: str
    catches: int
    runouts: int
    stumpings: int

    def to_dict(self):
        return{
            "player_id": self.player_id,
            "player_name": self.player_name,
            "catches": self.catches,
            "runouts": self.runouts,
            "stumpings": self.stumpings
        }

    @classmethod
    def from_dict(cls, data:Dict) -> 'Fielding':
        return cls(
            player_id=data.get("player_id"),
            player_name=data.get("player_name"),
            catches=data.get("catches"),
            runouts=data.get("runouts"),
            stumpings=data.get("stumpings")
        )

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
        return{
            "subtotal": self.subtotal,
            "extras": self.extras,
            "total": self.total,
            "byes_conceded": self.byes_conceded,
            "leg_byes_conceded": self.leg_byes_conceded,
            "penalties_conceded": self.penalties_conceded,
            "batting_overs": self.batting_overs,
            "bowling_overs": self.bowling_overs,
            "batting": [b.to_dict() for b in self.batting],
            "bowling": [b.to_dict() for b in self.bowling],
            "fielding": [f.to_dict() for f in self.fielding]
        }

    @classmethod
    def from_dict(cls, data:Dict) -> 'Scorecard':
        return cls(
            subtotal=data.get("subtotal"),
            extras=data.get("extras"),
            total=data.get("total"),
            byes_conceded=data.get("byes_conceded"),
            leg_byes_conceded=data.get("leg_byes_conceded"),
            penalties_conceded=data.get("penalties_conceded"),
            batting_overs=data.get("batting_overs"),
            bowling_overs=data.get("bowling_overs"),
            batting=[Batting.from_dict(x) for x in data.get("batting")],
            bowling=[Bowling.from_dict(x) for x in data.get("bowling")],
            fielding=[Fielding.from_dict(x) for x in data.get("fielding")]
        )

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
        return{
            "username": self.username,
            "match_id": self.match_id,
            "match_date": self.match_date,
            "match_format": self.match_format,
            "match_type": self.match_type,
            "venue": self.venue,
            "ground_name": self.ground_name,
            "opposition": self.opposition,
            "toss": self.toss,
            "result": self.result,
            "scorecard": self.scorecard.to_dict(),
            "created_date": self.created_date,
            "last_updated": self.last_updated,

        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Match':
        return cls(
            username=data.get("username"),
            match_id=data.get("match_id"),
            match_date=data.get("match_date"),
            match_format=MatchFormat[data.get("match_format")],
            match_type=MatchType[data.get("match_type")],
            venue=Venue[data.get("venue")],
            ground_name=data.get("ground_name"),
            opposition=data.get("opposition"),
            toss=TossResult[data.get("toss")],
            result=Result[data.get("result")],
            scorecard=Scorecard.from_dict(data.get("scorecard")),
            created_date=data.get("created_date"),
            last_updated=data.get("last_updated"),
        )

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
        return {
            "username": self.username,
            "team_id": self.team_id,
            "player_name": self.player_name,
            "player_role": self.player_role,
            "matches":  self.matches,
            "batting_runs": self.batting_runs,
            "batting_avg": self.batting_avg,
            "batting_sr": self.batting_sr,
            "overs": self.overs,
            "bowling_runs": self.bowling_runs,
            "wickets": self.wickets,
            "economy_rate": self.economy_rate,
            "bowling_avg": self.bowling_avg,
            "bowling_sr": self.bowling_sr,
            "catches": self.catches,
            "stumpings": self.stumpings,
            "runouts": self.runouts,
        }

    @classmethod
    def from_dict(cls, data:Dict) -> 'SelectedTeam':
        return cls(
            username=data.get("username"),
            team_id=data.get("team_id"),
            player_name=data.get("player_name"),
            player_role=PlayerRole[data.get("player_role")],
            matches=data.get("matches"),
            batting_runs=data.get("batting_runs"),
            batting_avg=data.get("batting_avg"),
            batting_sr=data.get("batting_sr"),
            overs=data.get("overs"),
            bowling_runs=data.get("bowling_runs"),
            wickets=data.get("wickets"),
            economy_rate=data.get("economy_rate"),
            bowling_avg=data.get("bowling_avg"),
            bowling_sr=data.get("bowling_sr"),
            catches=data.get("catches"),
            stumpings=data.get("stumpings"),
            runouts=data.get("runouts"),
        )











