from bff.enums import (BowlingStyle, BattingStyle, PlayerRole, TimePeriod, HowOut, MatchType, MatchFormat, Venue, TossResult, Result)


#BASIC ENUMS TEST

#TEST 1
role = PlayerRole.WKT_KEEPER
print(role)
print(role.value)
print(role.name)

#TEST 2
role_from_key = PlayerRole["BOWLER"]
print(role_from_key)

#TEST 3
try:
    print(PlayerRole["bowler"])
except KeyError:
    print("INVALID KEY --> bowler IS NOT AN ENUM KEY")

#TEST 4
try:
    invalid_role = PlayerRole["INVALID"]
except KeyError:
    print("INVALID KEY --> INVALID IS NOT AN ENUM KEY")



#TEST 5
for prole in PlayerRole:
    print(f"{prole.name} == {prole.value}")



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