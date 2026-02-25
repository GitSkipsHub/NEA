from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, List, Any
import bcrypt



class Account:
    def __init__(self, username: str, hashed_password: str, created_date: datetime = datetime.now()):
        self.username = username
        self.hashed_password = hashed_password
        self.created_date = created_date

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    @staticmethod
    def verify_password(password: str, hash_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))

    def to_dict(self) -> Dict[str, Any]: #Converst object into dictionary to store in MongoDB
        return {
            "username": self.username,
            "hashed_password": self.hashed_password,
            "created_date": self.created_date
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Account": #Converst MongoDB dictionary into object to be used in GUI
        return cls(
            username=data.get("username", ""),
            hashed_password=data.get("hashed_password", ""),
            created_date=data.get("created_date", datetime.now())
        )

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
    toss_result: str
    team_players: List[Dict[str, Any]] = field(default_factory=list)
    batting_scorecard: List[Dict[str, Any]] = field(default_factory=list)
    bowling_scorecard: List[Dict[str, Any]] = field(default_factory=list)
    fielding_scorecard: List[Dict[str, Any]] = field(default_factory=list)
    batting_summary: Dict[str, Any] = field(default_factory=dict)
    fielding_extras: Dict[str, Any] = field(default_factory=dict)
    captain_id: str = ""
    wk_id: str = ""
    # scorecard: Optional[Scorecard] = None
    created_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        d = asdict(self)
        d.pop("match_id", None)
        return d

    @classmethod
    def from_dict(cls, data: Dict) -> 'Match':
        data["match_id"] = str(data.pop("_id", ""))
        return cls(**data)