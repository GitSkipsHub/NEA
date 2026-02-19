from bff.enums import (BowlingStyle, BattingStyle, PlayerRole, TimePeriod, HowOut, MatchType, MatchFormat, Venue, TossResult, Result)

print(BowlingStyle.get_value("LAOS"))

print(BattingStyle.get_key("LEFT HAND"))

print(PlayerRole.list_values())

print(TimePeriod.get_value("L12M"))

print(HowOut.get_key("FIELD OBSTRUCTION"))

print(MatchType.list_values())

print(MatchFormat.get_value("FORTY_OVERS"))

print(Venue.get_key("HOME"))

print(Result.list_values())

print(TossResult.get_value("WON_BAT"))