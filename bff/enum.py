from enum import Enum

#---PLAYER ROLE & TYPE ENUMS---#

class PlayerRole(Enum):
    BATTER = "BATTER"
    BOWLER = "BOWLER"
    ALL_ROUNDER = "ALL ROUNDER"
    WICKET_KEEPER = "WICKET-KEEPER"

    @classmethod # Allows the method to be called on the class itself, not just on an instance.
    def list_values(cls):
        # Loops through every item (member) in the class (e.g. each enum option)
        # and collects them into a list.
        return[role.value for role in cls]
        # Returns a list containing all values defined in the class.

class BattingStyle(Enum):
    LEFT_HAND = "LH"
    RIGHT_HAND = "RH"

    @classmethod
    def list_values(cls):
        return[bat_style.value for bat_style in cls]


class BowlingStyle(Enum):
    PACE = "PACE"
    SPIN = "SPIN"

    @classmethod
    def list_values(cls):
        return[bowl_style.value for bowl_style in cls]


class PaceBowlingStyle(Enum):
    LEFT_ARM_PACE = "LEFT ARM PACE"
    RIGHT_ARM_PACE = "RIGHT ARM PACE"

    @classmethod
    def list_values(cls):
        return[pbowl_style for pbowl_style in cls]

class SpinBowlingStyle(Enum):
    LEFT_ARM_OFF_SPIN = "LEFT ARM OFF SPIN"
    LEFT_ARM_LEG_SPIN = "LEFT ARM LEG SPIN"
    RIGHT_ARM_OFF_SPIN = "RIGHT ARM OFF SPIN"
    RIGHT_ARM_LEG_SPIN = "RIGHT ARM LEG SPIN"

    @classmethod
    def list_values(cls):
        return[sbowl_style for sbowl_style in cls]







#---PERFORMANCE METRIC ENUMS---#

class BatterMetric(Enum):
    RUNS = "RUNS"
    BATTING_AVERAGE = "BATTING AVERAGE"
    BATTING_STRIKE_RATE = "STRIKE RATE"

    @classmethod
    def list_values(cls):
        return[batter_metric for batter_metric in cls]

class BowlerMetric(Enum):
    WICKETS = "WICKETS"
    BOWLING_AVERAGE = "BOWLING AVERAGE"
    BOWLING_STRIKE_RATE = "STRIKE RATE"

    @classmethod
    def list_values(cls):
        return[bowler_metric for bowler_metric in cls]


# ALL ROUNDER RE-USES BOTH BATTER & BOWLER METRICS FOR ITS ENUMS


class WicketKeeperMetric(Enum):
    DISMISSALS = "DISMISSALS"
    #BATTING AVERAGE FROM BATTING METRIC RE-USED
    @classmethod
    def list_values(cls):
        return[wk_metric for wk_metric in cls]


class TimePeriod(Enum):
    LAST_MONTH = "LAST MONTH"
    LAST_THREE_MONTHS = "LAST 3 MONTHS"
    LAST_FIVE_MONTHS = "LAST 5 MONTHS"

    @classmethod
    def list_values(cls):
        return[time_period for time_period in cls]









#---MATCH FILTER ENUMS---#

class MatchType(Enum):
    LEAGUE = "LEAGUE"
    CUP = "CUP"
    FRIENDLY = "FRIENDLY"

    @classmethod
    def list_values(cls):
        return[match_type for match_type in cls]


class MatchFormat(Enum):
    T20 = "T20"
    FORTY_OVERS = "40 OVERS"
    ODI = "ODI (50 OVERS)"

    @classmethod
    def list_values(cls):
        return[match_format for match_format in cls]

class Venue(Enum):
    HOME = "HOME"
    AWAY = "AWAY"
    NEUTRAL = "NEUTRAL"

    @classmethod
    def list_values(cls):
        return[venue for venue in cls]









#---MATCH RECORD ENUMS---#

class HowOut(Enum):
    BOWLED = "BOWLED"
    LBW = "LBW"
    CAUGHT = "CAUGHT"
    RUNOUT = "RUNOUT"
    STUMPED = "STUMPED"
    NOt_OUT = "NOT OUT"
    RETIRED = "RETIRED"
    HIT_WICKET = "HIT WICKET"
    TIMED_OUT = "TIMED OUT"
    FIELD_OBSTRUCTION = "FIELD OBSTRUCTION"
    OTHER = "OTHER"

    @classmethod
    def list_values(cls):
        return[how_out for how_out in cls ]


