import math

# Current formula: level = floor((xp/100)^(1/1.5))
def current_level_from_xp(xp):
    if xp <= 0:
        return 0
    return math.floor(math.pow(xp / 100, 1 / 1.5))

def current_xp_for_level(level):
    if level <= 0:
        return 0
    return int(math.pow(level * 100, 1.5))

# Print some sample values to understand the current system
print('Current XP/Level System:')
print('Level | XP Needed | XP Range')
print('------|-----------|----------')
for level in range(0, 21):
    xp_needed = current_xp_for_level(level)
    print(f'{level:5} | {xp_needed:9} | ', end='')
    if level > 0:
        prev_xp = current_xp_for_level(level-1)
        print(f'{prev_xp:,} - {xp_needed:,}')
    else:
        print('0 - 0')

# Test inverse calculation
print('\nTesting inverse calculation:')
for level in [1, 5, 10, 15, 20]:
    xp_needed = current_xp_for_level(level)
    calculated_level = current_level_from_xp(xp_needed)
    print(f'Level {level}: XP needed={xp_needed}, Calculated back={calculated_level}, Match: {level==calculated_level}')