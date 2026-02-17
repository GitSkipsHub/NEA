from dataclasses import dataclass, field, fields, asdict
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any
import bcrypt


@dataclass
class Account:
    username: str
    hashed_password: str
    created_date: datetime = field(default_factory=datetime.now)

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    @staticmethod
    def verify_password(password: str, hash_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data:Dict[str, Any]) -> 'Account':
        data = dict(data)
        data.pop("_id", None)
        return cls(**data)

@dataclass
class Player:
    #Player Details
    player_id: str
    username: str
    first_name: str
    last_name: str
    date_of_birth: str
    player_role: str
    batting_style: str
    bowling_style: str
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

    def to_dict(self) -> Dict[str, Any]: #Turns Python Object to Dictionary --> Key: Value
        d = asdict(self)
        d.pop("player_id", None)
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player': #Gets Player Data from Database and converts to Player object
        data = dict(data)
        data["player_id"] = str(data.pop("_id"))
        return cls(**data)

@dataclass
class Batting:
    player_id: str
    player_name: str
    pos: int
    how_out: str
    fielder: str
    bowler: str
    runs_scored: int
    balls: int
    fours: int
    sixes: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data:Dict[str, Any]) -> 'Batting':
        data = dict(data)
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

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data:Dict[str, Any]) -> 'Bowling':
        return cls(**data)

@dataclass
class Fielding:
    player_id: str
    player_name: str
    catches: int
    runouts: int
    stumpings: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data:Dict[str, Any]) -> 'Fielding':
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

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["batting"] = [x.to_dict() for x in self.batting]
        d["bowling"] = [x.to_dict() for x in self.bowling]
        d["fielding"] = [x.to_dict() for x in self.fielding]
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Scorecard':
        data = dict(data)
        data["batting"] = [Batting.from_dict(x) for x in data.get("batting", [])]
        data["bowling"] = [Bowling.from_dict(x) for x in data.get("bowling", [])]
        data["fielding"] = [Fielding.from_dict(x) for x in data.get("fielding", [])]
        return cls(**data)

@dataclass
class Match:
    match_id: str
    username: str
    match_date: str
    match_format: str
    match_type: str
    venue: str
    ground_name: str
    opposition: str
    result: str
    toss_result: str = ""
    team_players: list = field(default_factory=list)
    captain_id: str = ""
    wk_id: str = ""
    scorecard: Optional[Scorecard] = None
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["scorecard"] = self.scorecard.to_dict() if self.scorecard else None
        d.pop("match_id", None)
        return d

    @classmethod
    def from_dict(cls, data: Dict) -> 'Match':
        data = dict(data)
        data["match_id"] = str(data.pop("_id", ""))
        sc = data.get("scorecard")
        data["scorecard"] = Scorecard.from_dict(sc) if isinstance(sc, dict) else None
        allowed = {f.name for f in fields(cls)}
        cleaned = {k: v for k, v in data.items() if k in allowed}
        return cls(**cleaned)


@dataclass
class TeamGenerator:
    time_period: str
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
    player_role: str
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
        data = dict(data)
        return cls(**data)