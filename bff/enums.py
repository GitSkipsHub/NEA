from enum import Enum

class BaseEnum(Enum):

    @classmethod #Method called on the class itself, not just on an instance.
    def get_value(cls, key: str): #Retrieve the enumeration value based on its key name
        try:
            return cls[key].value
        except KeyError:
            raise ValueError(f"{key} is not a valid {cls.__name__} key") #If given key does not exist within enum

    @classmethod
    def get_key(cls, value: str): #Retrieve the enumeration key name based on its value
        try:
            return cls(value).name
        except:
            raise ValueError(f"{value} is not a valid {cls.__name__} value.") #If given value does not exist within the enum

    @classmethod
    def list_values(cls): #cls denotes which specific enum it is e.g. PlayerRole, TimePeriod etc.
        # Loops through every item (enum option) in the class and collects them into a list.
        return[key.value for key in cls]
        # Returns list containing all values defined in the class

#PLAYER ROLE & TYPE ENUMS
class PlayerRole(BaseEnum):
    BATTER = "BATTER"
    BOWLER = "BOWLER"
    ALL_ROUNDER = "ALL ROUNDER"
    WKT_KEEPER = "WICKET-KEEPER BATTER"

class BattingStyle(BaseEnum):
    RH = "RIGHT HAND"
    LH = "LEFT HAND"

class BowlingStyle(BaseEnum):
    RAP = "RIGHT ARM PACE"
    RAOS = "RIGHT ARM OFF SPIN"
    RALS = "RIGHT ARM LEG SPIN"
    LAP = "LEFT ARM PACE"
    LAOS = "LEFT ARM OFF SPIN"
    LALS = "LEFT ARM LEG SPIN"
    NONE = "NONE"



#PERFORMANCE METRIC ENUMS

class BatterMetric(BaseEnum):
    RUNS = "RUNS"
    BAT_AVG = "BATTING AVERAGE"
    BAT_SR = "STRIKE RATE"

class BowlerMetric(BaseEnum):
    WICKETS = "WICKETS"
    BOWL_AVG = "BOWLING AVERAGE"
    BOWL_SR = "STRIKE RATE"
# ALL ROUNDER RE-USES BOTH BATTER & BOWLER METRICS FOR ITS ENUMS

class WicketKeeperMetric(BaseEnum):
    DISMISSALS = "DISMISSALS"
    #BATTING AVERAGE FROM BATTING METRIC RE-USED

class TimePeriod(BaseEnum):
    LM = "LAST MONTH"
    L3M = "LAST 3 MONTHS"
    L6M = "LAST 6 MONTHS"
    L12M = "LAST YEAR"

#---MATCH FILTER ENUMS---#
class MatchType(BaseEnum):
    LEAGUE = "LEAGUE"
    CUP = "CUP"
    FRIENDLY = "FRIENDLY"

class MatchFormat(BaseEnum):
    T20 = "T20"
    FORTY_OVERS = "40 OVERS"
    ODI = "ODI (50 OVERS)"

class Venue(BaseEnum):
    HOME = "HOME"
    AWAY = "AWAY"
    NEUTRAL = "NEUTRAL"

#MATCH RECORD ENUMS
class HowOut(BaseEnum):
    BOWLED = "BOWLED"
    LBW = "LBW"
    CAUGHT = "CAUGHT"
    RUNOUT = "RUNOUT"
    STUMPED = "STUMPED"
    NOT_OUT = "NOT OUT"
    RETIRED = "RETIRED"
    HIT_WICKET = "HIT WICKET"
    TIMED_OUT = "TIMED OUT"
    FIELD_OBSTRUCTION = "FIELD OBSTRUCTION"
    DID_NOT_BAT = "DID NOT BAT"
    OTHER = "OTHER"

class TossResult(BaseEnum):
    LOST_BOWL = "LOST THE TOSS & BOWLED"
    LOST_BAT = "LOST THE TOSS & BATTED"
    WON_BOWL = "WON THE TOSS & BOWLED"
    WON_BAT = "WON THE TOSS & BATTED"

class Result(BaseEnum):
    WON = "WON"
    LOST = "LOST"
    TIE = "TIE"
    ABANDONED = "ABANDONED"
    CANCELLED = "CANCELLED"
    NO_RESULT = "NO RESULT"
