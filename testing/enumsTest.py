from bff.enums import (BowlingStyle, BattingStyle, PlayerRole)

#ENUM METHODS TEST

#TEST 1
print(BowlingStyle.get_value("LAOS"))

#TEST 2
print(BattingStyle.get_key("LEFT HAND"))

#TEST 3
print(PlayerRole.list_values())

#TEST 4
try:
    print(PlayerRole.get_key("bowler"))
except ValueError as e:
    print(f"VALUE ERROR: {e}")


#TEST 5
try:
    print(PlayerRole.get_value("INVALID_ROLE"))
except ValueError as e:
    print(f"VALUE ERROR: {e}")

print(PlayerRole.WKT_KEEPER.value)







