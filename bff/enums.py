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
        for member in cls:
            if member.value == value:
                return member.name
        raise ValueError(f"{value} is not a valid {cls.__name__} value.") #If given value does not exist within the enum

    @classmethod
    def list_values(cls):
        # Loops through every item (enum option) in the class and collects them into a list.
        return[key.value for key in cls]
        # Returns list containing all values defined in the class

#PLAYER ROLE & TYPE ENUMS
class PlayerRole(BaseEnum):
    BATTER = "BATTER"
    BOWLER = "BOWLER"
    ALL_ROUNDER = "ALL ROUNDER"
    WICKET_KEEPER = "WICKET-KEEPER"

class BattingStyle(BaseEnum):
    LEFT_HAND = "LEFT HAND"
    RIGHT_HAND = "RIGHT HAND"

class BowlingStyle(BaseEnum):
    LEFT_ARM_PACE = "LEFT ARM PACE"
    RIGHT_ARM_PACE = "RIGHT ARM PACE"
    LEFT_ARM_OFF_SPIN = "LEFT ARM OFF SPIN"
    LEFT_ARM_LEG_SPIN = "LEFT ARM LEG SPIN"
    RIGHT_ARM_OFF_SPIN = "RIGHT ARM OFF SPIN"
    RIGHT_ARM_LEG_SPIN = "RIGHT ARM LEG SPIN"



#PERFORMANCE METRIC ENUMS

class BatterMetric(BaseEnum):
    RUNS = "RUNS"
    BATTING_AVERAGE = "BATTING AVERAGE"
    BATTING_STRIKE_RATE = "STRIKE RATE"

class BowlerMetric(BaseEnum):
    WICKETS = "WICKETS"
    BOWLING_AVERAGE = "BOWLING AVERAGE"
    BOWLING_STRIKE_RATE = "STRIKE RATE"
# ALL ROUNDER RE-USES BOTH BATTER & BOWLER METRICS FOR ITS ENUMS

class WicketKeeperMetric(BaseEnum):
    DISMISSALS = "DISMISSALS"
    #BATTING AVERAGE FROM BATTING METRIC RE-USED

class TimePeriod(BaseEnum):
    LAST_MONTH = "LAST MONTH"
    LAST_THREE_MONTHS = "LAST 3 MONTHS"
    LAST_FIVE_MONTHS = "LAST 5 MONTHS"
    LAST_YEAR = "LAST YEAR"

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
