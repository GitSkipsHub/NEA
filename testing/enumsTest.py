from bff.enums import (BattingStyle, BowlingStyle, PlayerRole, TimePeriod,
                       HowOut, MatchType, MatchFormat, Venue, TossResult, Result)

print(PlayerRole.get_value("WICKET_KEEPER"))

print(PlayerRole.get_key("BATTER"))

print(HowOut.get_key("FIELD OBSTRUCTION"))

print(TossResult.get_value("LOST_BOWL"))

print(Result.list_values())

print(PlayerRole.list_values())

print(MatchFormat.get_value("FORTY_OVERS"))