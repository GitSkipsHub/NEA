from bff.enums import (BowlingStyle, BattingStyle, PlayerRole)

#ENUM METHODS TEST

#TEST 1
print(BowlingStyle.get_value("LAOS"))

#TEST 2
print(BattingStyle.get_key("LEFT HAND"))

#TEST 3
print(PlayerRole.list_values())

#TEST 4
print(PlayerRole.get_key("bowler"))

#TEST 5
print(PlayerRole.get_value("INVALID_ROLE"))


