import streamlit as st

# -------------------------------------------------------------------------
# 1. FIFA WORLD RANKING POINTS DATA
# -------------------------------------------------------------------------
FIFA_SCORES = {
    "🇦🇷 Argentina": 1877.27, 
    "🇪🇸 Spain": 1874.71, 
    "🇫🇷 France": 1870.70, 
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England": 1828.02,
    "🇵🇹 Portugal": 1767.85, 
    "🇧🇷 Brazil": 1765.86, 
    "🇲🇦 Morocco": 1755.10, 
    "🇳🇱 Netherlands": 1753.57,
    "🇧🇪 Belgium": 1742.24,
    "🇩🇪 Germany": 1735.77,
    "🇭🇷 Croatia": 1714.87,
    "🇨🇴 Colombia": 1698.35,
    "🇲🇽 Mexico": 1687.48,
    "🇸🇳 Senegal": 1684.07,
    "🇺🇾 Uruguay": 1673.07,
    "🇺🇸 USA": 1671.23,
    "🇯🇵 Japan": 1661.58,
    "🇨🇭 Switzerland": 1650.06,
    "🇮🇷 Iran": 1619.58,
    "🇹🇷 Turkiye": 1605.73,
    "🇪🇨 Ecuador": 1598.52,
    "🇦🇹 Austria": 1597.40,
    "🇰🇷 Korea Republic": 1591.63,
    "🇦🇺 Australia": 1579.34,
    "🇩🇿 Algeria": 1571.03,
    "🇪🇬 Egypt": 1562.37,
    "🇨🇦 Canada": 1559.48,
    "🇳🇴 Norway": 1557.44,
    "🇨🇮 Ivory Coast": 1540.87,
    "🇵🇦 Panama": 1539.16,
    "🇸🇪 Sweden": 1509.79,
    "🇨🇿 Czechia": 1505.74,
    "🇵🇾 Paraguay": 1505.35,
    "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland": 1503.34,
    "🇹🇳 Tunisia": 1476.41,
    "🇨🇩 Congo DR": 1747.43,
    "🇺🇿 Uzbekistan": 1458.20,
    "🇶🇦 Qatar": 1450.31,
    "🇮🇶 Iraq": 1446.28,
    "🇿🇦 South Africa": 1428.38,
    "🇸🇦 Saudi Arabia": 1423.88,
    "🇯🇴 Jordan": 1387.74,
    "🇧🇦 Bosnia and Herzegovina": 1387.22,
    "🇨🇻 Cabo Verde": 1371.11,
    "🇬🇭 Ghana": 1346.88,
    "🇨🇼 Curacao": 1294.77,
    "🇭🇹 Haiti": 1293.10,
    "🇳🇿 New Zealand": 1275.58
}

# Complete structural tournament database categorized by stage subtabs
INITIAL_MATCHES = [
# --- MATCHDAY 1 ---
    {"match_id": 1, "stage": "Matchday 1", "info": "Group A", "team_a": "🇲🇽 Mexico", "team_b": "🇿🇦 South Africa", "date": "June 12, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 2, "stage": "Matchday 1", "info": "Group A", "team_a": "🇰🇷 Korea Republic", "team_b": "🇨🇿 Czechia", "date": "June 12, 2026", "time": "9:00AM (UTC+7)"},
    {"match_id": 3, "stage": "Matchday 1", "info": "Group B", "team_a": "🇨🇦 Canada", "team_b": "🇧🇦 Bosnia and Herzegovina", "date": "June 13, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 4, "stage": "Matchday 1", "info": "Group D", "team_a": "🇺🇸 USA", "team_b": "🇵🇾 Paraguay", "date": "June 13, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 5, "stage": "Matchday 1", "info": "Group B", "team_a": "🇶🇦 Qatar", "team_b": "🇨🇭 Switzerland", "date": "June 14, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 6, "stage": "Matchday 1", "info": "Group C", "team_a": "🇧🇷 Brazil", "team_b": "🇲🇦 Morocco", "date": "June 14, 2026", "time": "5:00AM (UTC+7)"},
    {"match_id": 7, "stage": "Matchday 1", "info": "Group C", "team_a": "🇭🇹 Haiti", "team_b": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland", "date": "June 14, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 8, "stage": "Matchday 1", "info": "Group D", "team_a": "🇦🇺 Australia", "team_b": "🇹🇷 Turkiye", "date": "June 14, 2026", "time": "11:00AM (UTC+7)"},
    {"match_id": 9, "stage": "Matchday 1", "info": "Group E", "team_a": "🇩🇪 Germany", "team_b": "🇨🇼 Curacao", "date": "June 15, 2026", "time": "12:00AM (UTC+7)"},
    {"match_id": 10, "stage": "Matchday 1", "info": "Group F", "team_a": "🇳🇱 Netherlands", "team_b": "🇯🇵 Japan", "date": "June 15, 2026", "time": "3:00AM (UTC+7)"},
    {"match_id": 11, "stage": "Matchday 1", "info": "Group E", "team_a": "🇨🇮 Ivory Coast", "team_b": "🇪🇨 Ecuador", "date": "June 15, 2026", "time": "6:00AM (UTC+7)"},
    {"match_id": 12, "stage": "Matchday 1", "info": "Group F", "team_a": "🇸🇪 Sweden", "team_b": "🇹🇳 Tunisia", "date": "June 15, 2026", "time": "9:00AM (UTC+7)"},
    {"match_id": 13, "stage": "Matchday 1", "info": "Group H", "team_a": "🇪🇸 Spain", "team_b": "🇨🇻 Cabo Verde", "date": "June 15, 2026", "time": "11:00PM (UTC+7)"},
    {"match_id": 14, "stage": "Matchday 1", "info": "Group G", "team_a": "🇧🇪 Belgium", "team_b": "🇪🇬 Egypt", "date": "June 16, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 15, "stage": "Matchday 1", "info": "Group H", "team_a": "🇸🇦 Saudi Arabia", "team_b": "🇺🇾 Uruguay", "date": "June 16, 2026", "time": "5:00AM (UTC+7)"},
    {"match_id": 16, "stage": "Matchday 1", "info": "Group G", "team_a": "🇮🇷 Iran", "team_b": "🇳🇿 New Zealand", "date": "June 16, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 17, "stage": "Matchday 1", "info": "Group I", "team_a": "🇫🇷 France", "team_b": "🇸🇳 Senegal", "date": "June 17, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 18, "stage": "Matchday 1", "info": "Group I", "team_a": "🇮🇶 Iraq", "team_b": "🇳🇴 Norway", "date": "June 17, 2026", "time": "5:00AM (UTC+7)"},
    {"match_id": 19, "stage": "Matchday 1", "info": "Group J", "team_a": "🇦🇷 Argentina", "team_b": "🇩🇿 Algeria", "date": "June 17, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 20, "stage": "Matchday 1", "info": "Group J", "team_a": "🇦🇹 Austria", "team_b": "🇯🇴 Jordan", "date": "June 17, 2026", "time": "11:00AM (UTC+7)"},
    {"match_id": 21, "stage": "Matchday 1", "info": "Group K", "team_a": "🇵🇹 Portugal", "team_b": "🇨🇩 Congo DR", "date": "June 18, 2026", "time": "12:00AM (UTC+7)"},
    {"match_id": 22, "stage": "Matchday 1", "info": "Group L", "team_a": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England", "team_b": "🇭🇷 Croatia", "date": "June 18, 2026", "time": "3:00AM (UTC+7)"},
    {"match_id": 23, "stage": "Matchday 1", "info": "Group L", "team_a": "🇬🇭 Ghana", "team_b": "🇵🇦 Panama", "date": "June 18, 2026", "time": "6:00AM (UTC+7)"},
    {"match_id": 24, "stage": "Matchday 1", "info": "Group K", "team_a": "🇺🇿 Uzbekistan", "team_b": "🇨🇴 Colombia", "date": "June 18, 2026", "time": "9:00AM (UTC+7)"},
    
    # --- MATCHDAY 2 ---
    {"match_id": 25, "stage": "Matchday 2", "info": "Group A", "team_a": "🇨🇿 Czechia", "team_b": "🇿🇦 South Africa", "date": "June 18, 2026", "time": "11:00PM (UTC+7)"},
    {"match_id": 26, "stage": "Matchday 2", "info": "Group B", "team_a": "🇨🇭 Switzerland", "team_b": "🇧🇦 Bosnia and Herzegovina", "date": "June 19, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 27, "stage": "Matchday 2", "info": "Group B", "team_a": "🇨🇦 Canada", "team_b": "🇶🇦 Qatar", "date": "June 19, 2026", "time": "5:00AM (UTC+7)"},
    {"match_id": 28, "stage": "Matchday 2", "info": "Group A", "team_a": "🇲🇽 Mexico", "team_b": "🇰🇷 Korea Republic", "date": "June 19, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 29, "stage": "Matchday 2", "info": "Group D", "team_a": "🇺🇸 USA", "team_b": "🇦🇺 Australia", "date": "June 20, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 30, "stage": "Matchday 2", "info": "Group C", "team_a": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland", "team_b": "🇲🇦 Morocco", "date": "June 20, 2026", "time": "5:00AM (UTC+7)"},
    {"match_id": 31, "stage": "Matchday 2", "info": "Group C", "team_a": "🇧🇷 Brazil", "team_b": "🇭🇹 Haiti", "date": "June 20, 2026", "time": "7:30AM (UTC+7)"},
    {"match_id": 32, "stage": "Matchday 2", "info": "Group D", "team_a": "🇹🇷 Turkiye", "team_b": "🇵🇾 Paraguay", "date": "June 20, 2026", "time": "10:00AM (UTC+7)"},
    {"match_id": 33, "stage": "Matchday 2", "info": "Group F", "team_a": "🇳🇱 Netherlands", "team_b": "🇸🇪 Sweden", "date": "June 21, 2026", "time": "12:00AM (UTC+7)"},
    {"match_id": 34, "stage": "Matchday 2", "info": "Group E", "team_a": "🇩🇪 Germany", "team_b": "🇨🇮 Ivory Coast", "date": "June 21, 2026", "time": "3:00AM (UTC+7)"},
    {"match_id": 35, "stage": "Matchday 2", "info": "Group E", "team_a": "🇪🇨 Ecuador", "team_b": "🇨🇼 Curacao", "date": "June 21, 2026", "time": "7:00AM (UTC+7)"},
    {"match_id": 36, "stage": "Matchday 2", "info": "Group F", "team_a": "🇹🇳 Tunisia", "team_b": "🇯🇵 Japan", "date": "June 21, 2026", "time": "11:00AM (UTC+7)"},
    {"match_id": 37, "stage": "Matchday 2", "info": "Group H", "team_a": "🇪🇸 Spain", "team_b": "🇸🇦 Saudi Arabia", "date": "June 21, 2026", "time": "11:00PM (UTC+7)"},
    {"match_id": 38, "stage": "Matchday 2", "info": "Group G", "team_a": "🇧🇪 Belgium", "team_b": "🇮🇷 Iran", "date": "June 22, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 39, "stage": "Matchday 2", "info": "Group H", "team_a": "🇺🇾 Uruguay", "team_b": "🇨🇻 Cabo Verde", "date": "June 22, 2026", "time": "5:00AM (UTC+7)"},
    {"match_id": 40, "stage": "Matchday 2", "info": "Group G", "team_a": "🇳🇿 New Zealand", "team_b": "🇪🇬 Egypt", "date": "June 22, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 41, "stage": "Matchday 2", "info": "Group J", "team_a": "🇦🇷 Argentina", "team_b": "🇦🇹 Austria", "date": "June 23, 2026", "time": "12:00AM (UTC+7)"},
    {"match_id": 42, "stage": "Matchday 2", "info": "Group I", "team_a": "🇫🇷 France", "team_b": "🇮🇶 Iraq", "date": "June 23, 2026", "time": "4:00AM (UTC+7)"},
    {"match_id": 43, "stage": "Matchday 2", "info": "Group I", "team_a": "🇳🇴 Norway", "team_b": "🇸🇳 Senegal", "date": "June 23, 2026", "time": "7:00AM (UTC+7)"},
    {"match_id": 44, "stage": "Matchday 2", "info": "Group J", "team_a": "🇯🇴 Jordan", "team_b": "🇩🇿 Algeria", "date": "June 23, 2026", "time": "10:00AM (UTC+7)"},
    {"match_id": 45, "stage": "Matchday 2", "info": "Group K", "team_a": "🇵🇹 Portugal", "team_b": "🇺🇿 Uzbekistan", "date": "June 24, 2026", "time": "12:00AM (UTC+7)"},
    {"match_id": 46, "stage": "Matchday 2", "info": "Group L", "team_a": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England", "team_b": "🇬🇭 Ghana", "date": "June 24, 2026", "time": "3:00AM (UTC+7)"},
    {"match_id": 47, "stage": "Matchday 2", "info": "Group K", "team_a": "🇵🇦 Panama", "team_b": "🇭🇷 Croatia", "date": "June 24, 2026", "time": "6:00AM (UTC+7)"},
    {"match_id": 48, "stage": "Matchday 2", "info": "Group L", "team_a": "🇨🇴 Colombia", "team_b": "🇨🇩 Congo DR", "date": "June 24, 2026", "time": "9:00AM (UTC+7)"},
    
    # --- MATCHDAY 3 ---
    {"match_id": 49, "stage": "Matchday 3", "info": "Group B", "team_a": "🇧🇦 Bosnia and Herzegovina", "team_b": "🇶🇦 Qatar", "date": "June 25, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 50, "stage": "Matchday 3", "info": "Group B", "team_a": "🇨🇭 Switzerland", "team_b": "🇨🇦 Canada", "date": "June 25, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 51, "stage": "Matchday 3", "info": "Group C", "team_a": "🇲🇦 Morocco", "team_b": "🇭🇹 Haiti", "date": "June 25, 2026", "time": "5:00AM (UTC+7)"},
    {"match_id": 52, "stage": "Matchday 3", "info": "Group C", "team_a": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland", "team_b": "🇧🇷 Brazil", "date": "June 25, 2026", "time": "5:00AM (UTC+7)"},
    {"match_id": 53, "stage": "Matchday 3", "info": "Group A", "team_a": "🇨🇿 Czechia", "team_b": "🇲🇽 Mexico", "date": "June 25, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 54, "stage": "Matchday 3", "info": "Group A", "team_a": "🇿🇦 South Africa", "team_b": "🇰🇷 Korea Republic", "date": "June 25, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 55, "stage": "Matchday 3", "info": "Group E", "team_a": "🇨🇼 Curacao", "team_b": "🇨🇮 Ivory Coast", "date": "June 26, 2026", "time": "3:00AM (UTC+7)"},
    {"match_id": 56, "stage": "Matchday 3", "info": "Group E", "team_a": "🇪🇨 Ecuador", "team_b": "🇩🇪 Germany", "date": "June 26, 2026", "time": "3:00AM (UTC+7)"},
    {"match_id": 57, "stage": "Matchday 3", "info": "Group F", "team_a": "🇯🇵 Japan", "team_b": "🇸🇪 Sweden", "date": "June 26, 2026", "time": "6:00AM (UTC+7)"},
    {"match_id": 58, "stage": "Matchday 3", "info": "Group F", "team_a": "🇹🇳 Tunisia", "team_b": "🇳🇱 Netherlands", "date": "June 26, 2026", "time": "6:00AM (UTC+7)"},
    {"match_id": 59, "stage": "Matchday 3", "info": "Group D", "team_a": "🇵🇾 Paraguay", "team_b": "🇦🇺 Australia", "date": "June 26, 2026", "time": "9:00AM (UTC+7)"},
    {"match_id": 60, "stage": "Matchday 3", "info": "Group D", "team_a": "🇹🇷 Turkiye", "team_b": "🇺🇸 USA", "date": "June 26, 2026", "time": "9:00AM (UTC+7)"},
    {"match_id": 61, "stage": "Matchday 3", "info": "Group I", "team_a": "🇳🇴 Norway", "team_b": "🇫🇷 France", "date": "June 27, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 62, "stage": "Matchday 3", "info": "Group I", "team_a": "🇸🇳 Senegal", "team_b": "🇮🇶 Iraq", "date": "June 27, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 63, "stage": "Matchday 3", "info": "Group H", "team_a": "🇨🇻 Cabo Verde", "team_b": "🇸🇦 Saudi Arabia", "date": "June 27, 2026", "time": "7:00AM (UTC+7)"},
    {"match_id": 64, "stage": "Matchday 3", "info": "Group H", "team_a": "🇺🇾 Uruguay", "team_b": "🇪🇸 Spain", "date": "June 27, 2026", "time": "7:00AM (UTC+7)"},
    {"match_id": 65, "stage": "Matchday 3", "info": "Group G", "team_a": "🇪🇬 Egypt", "team_b": "🇮🇷 Iran", "date": "June 27, 2026", "time": "10:00AM (UTC+7)"},
    {"match_id": 66, "stage": "Matchday 3", "info": "Group G", "team_a": "🇳🇿 New Zealand", "team_b": "🇧🇪 Belgium", "date": "June 27, 2026", "time": "10:00AM (UTC+7)"},
    {"match_id": 67, "stage": "Matchday 3", "info": "Group L", "team_a": "🇭🇷 Croatia", "team_b": "🇬🇭 Ghana", "date": "June 28, 2026", "time": "4:00AM (UTC+7)"},
    {"match_id": 68, "stage": "Matchday 3", "info": "Group L", "team_a": "🇵🇦 Panama", "team_b": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England", "date": "June 28, 2026", "time": "4:00AM (UTC+7)"},
    {"match_id": 69, "stage": "Matchday 3", "info": "Group K", "team_a": "🇨🇴 Colombia", "team_b": "🇵🇹 Portugal", "date": "June 28, 2026", "time": "6:30AM (UTC+7)"},
    {"match_id": 70, "stage": "Matchday 3", "info": "Group K", "team_a": "🇨🇩 Congo DR", "team_b": "🇺🇿 Uzbekistan", "date": "June 28, 2026", "time": "6:30AM (UTC+7)"},
    {"match_id": 71, "stage": "Matchday 3", "info": "Group J", "team_a": "🇩🇿 Algeria", "team_b": "🇦🇹 Austria", "date": "June 28, 2026", "time": "9:00AM (UTC+7)"},
    {"match_id": 72, "stage": "Matchday 3", "info": "Group J", "team_a": "🇯🇴 Jordan", "team_b": "🇦🇷 Argentina", "date": "June 28, 2026", "time": "9:00AM (UTC+7)"},
    
    # --- ROUND OF 32 ---
    {"match_id": 73, "stage": "Round of 32", "info": "Round of 32 Match 1", "team_a": "Runner-up Group A", "team_b": "Runner-up Group B", "date": "June 29, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 74, "stage": "Round of 32", "info": "Round of 32 Match 2", "team_a": "Winner Group C", "team_b": "Runner-up Group F", "date": "June 30, 2026", "time": "12:00AM (UTC+7)"},
    {"match_id": 75, "stage": "Round of 32", "info": "Round of 32 Match 3", "team_a": "Winner Group E", "team_b": "3rd Group A/B/C/D/F", "date": "June 30, 2026", "time": "3:30AM (UTC+7)"},
    {"match_id": 76, "stage": "Round of 32", "info": "Round of 32 Match 4", "team_a": "Winner Group F", "team_b": "Runner-up Group C", "date": "June 30, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 77, "stage": "Round of 32", "info": "Round of 32 Match 5", "team_a": "Runner-up Group E", "team_b": "Runner-up Group I", "date": "July 1, 2026", "time": "12:00AM (UTC+7)"},
    {"match_id": 78, "stage": "Round of 32", "info": "Round of 32 Match 6", "team_a": "Winner Group I", "team_b": "3rd Group C/D/F/G/H", "date": "July 1, 2026", "time": "4:00AM (UTC+7)"},
    {"match_id": 79, "stage": "Round of 32", "info": "Round of 32 Match 7", "team_a": "Winner Group A", "team_b": "3rd Group C/E/F/H/I", "date": "July 1, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 80, "stage": "Round of 32", "info": "Round of 32 Match 8", "team_a": "Winner Group L", "team_b": "3rd Group E/H/I/J/K", "date": "July 1, 2026", "time": "11:00PM (UTC+7)"},
    {"match_id": 81, "stage": "Round of 32", "info": "Round of 32 Match 9", "team_a": "Winner Group G", "team_b": "3rd Group A/E/H/I/J", "date": "July 2, 2026", "time": "3:00AM (UTC+7)"},
    {"match_id": 82, "stage": "Round of 32", "info": "Round of 32 Match 10", "team_a": "Winner Group D", "team_b": "3rd Group B/E/F/I/J", "date": "July 2, 2026", "time": "7:00AM (UTC+7)"},
    {"match_id": 83, "stage": "Round of 32", "info": "Round of 32 Match 11", "team_a": "Winner Group H", "team_b": "Runner-up Group J", "date": "July 3, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 84, "stage": "Round of 32", "info": "Round of 32 Match 12", "team_a": "Runner-up Group K", "team_b": "Runner-up Group L", "date": "July 3, 2026", "time": "6:00AM (UTC+7)"},
    {"match_id": 85, "stage": "Round of 32", "info": "Round of 32 Match 13", "team_a": "Winner Group B", "team_b": "3rd Group E/F/G/I/J", "date": "July 3, 2026", "time": "10:00AM (UTC+7)"},
    {"match_id": 86, "stage": "Round of 32", "info": "Round of 32 Match 14", "team_a": "Runner-up Group D", "team_b": "Runner-up Group G", "date": "July 4, 2026", "time": "1:00AM (UTC+7)"},
    {"match_id": 87, "stage": "Round of 32", "info": "Round of 32 Match 15", "team_a": "Winner Group J", "team_b": "Runner-up Group H", "date": "July 4, 2026", "time": "5:00AM (UTC+7)"},
    {"match_id": 88, "stage": "Round of 32", "info": "Round of 32 Match 16", "team_a": "Winner Group K", "team_b": "3rd Group D/E/I/J/L", "date": "July 4, 2026", "time": "8:30AM (UTC+7)"},
    
    # --- ROUND OF 16 ---
    {"match_id": 89, "stage": "Round of 16", "info": "Round of 16 Match 1", "team_a": "Winner R32 Match 1", "team_b": "Winner R32 Match 4", "date": "July 5, 2026", "time": "12:00AM (UTC+7)"},
    {"match_id": 90, "stage": "Round of 16", "info": "Round of 16 Match 2", "team_a": "Winner R32 Match 3", "team_b": "Winner R32 Match 6", "date": "July 5, 2026", "time": "4:00AM (UTC+7)"},
    {"match_id": 91, "stage": "Round of 16", "info": "Round of 16 Match 3", "team_a": "Winner R32 Match 2", "team_b": "Winner R32 Match 5", "date": "July 6, 2026", "time": "3:00AM (UTC+7)"},
    {"match_id": 92, "stage": "Round of 16", "info": "Round of 16 Match 4", "team_a": "Winner R32 Match 7", "team_b": "Winner R32 Match 8", "date": "July 6, 2026", "time": "7:00AM (UTC+7)"},
    {"match_id": 93, "stage": "Round of 16", "info": "Round of 16 Match 5", "team_a": "Winner R32 Match 12", "team_b": "Winner R32 Match 11", "date": "July 7, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 94, "stage": "Round of 16", "info": "Round of 16 Match 6", "team_a": "Winner R32 Match 10", "team_b": "Winner R32 Match 9", "date": "July 7, 2026", "time": "7:00AM (UTC+7)"},
    {"match_id": 95, "stage": "Round of 16", "info": "Round of 16 Match 7", "team_a": "Winner R32 Match 15", "team_b": "Winner R32 Match 14", "date": "July 7, 2026", "time": "11:00PM (UTC+7)"},
    {"match_id": 96, "stage": "Round of 16", "info": "Round of 16 Match 8", "team_a": "Winner R32 Match 13", "team_b": "Winner R32 Match 16", "date": "July 8, 2026", "time": "3:00AM (UTC+7)"},
    
    # --- QUARTERFINALS ---
    {"match_id": 97, "stage": "Quarterfinals", "info": "Quarterfinals Match 1", "team_a": "Winner R16 Match 1", "team_b": "Winner R16 Match 2", "date": "July 10, 2026", "time": "3:00AM (UTC+7)"},
    {"match_id": 98, "stage": "Quarterfinals", "info": "Quarterfinals Match 2", "team_a": "Winner R16 Match 5", "team_b": "Winner R16 Match 6", "date": "July 11, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 99, "stage": "Quarterfinals", "info": "Quarterfinals Match 3", "team_a": "Winner R16 Match 3", "team_b": "Winner R16 Match 4", "date": "July 12, 2026", "time": "4:00AM (UTC+7)"},
    {"match_id": 100, "stage": "Quarterfinals", "info": "Quarterfinals Match 4", "team_a": "Winner R16 Match 7", "team_b": "Winner R16 Match 8", "date": "July 12, 2026", "time": "8:00AM (UTC+7)"},
    
    # --- SEMIFINALS ---
    {"match_id": 101, "stage": "Semifinals", "info": "Semifinals Match 1", "team_a": "Winner QF Match 1", "team_b": "Winner QF Match 2", "date": "July 15, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 102, "stage": "Semifinals", "info": "Semifinals Match 2", "team_a": "Winner QF Match 3", "team_b": "Winner QF Match 4", "date": "July 16, 2026", "time": "2:00AM (UTC+7)"},
    
    # --- 3RD PLACE MATCH ---
    {"match_id": 103, "stage": "3rd Place Match", "info": "Bronze Final", "team_a": "Loser SF Match 1", "team_b": "Loser SF Match 2", "date": "July 19, 2026", "time": "4:00AM (UTC+7)"},
    
    # --- FINAL ---
    {"match_id": 104, "stage": "Final", "info": "World Cup Final", "team_a": "Winner SF Match 1", "team_b": "Winner SF Match 2", "date": "July 20, 2026", "time": "2:00AM (UTC+7)"}
]

# -------------------------------------------------------------------------
# 2. SEAMLESS ODDS CALCULATION LOGIC
# -------------------------------------------------------------------------
def calculate_odds(team_a, team_b):
    # If it's a knockout placeholder (e.g., "Winner Group A"), give a balanced 1500.0 score
    rating_a = FIFA_SCORES.get(team_a, 1500.0)
    rating_b = FIFA_SCORES.get(team_b, 1500.0)
    
    total_rating = rating_a + rating_b
    prob_a = rating_a / total_rating
    prob_b = rating_b / total_rating
    
    win_prob_a = prob_a * 0.8
    win_prob_b = prob_b * 0.8
    draw_prob = 0.20
    
    odds_a = round(1 / win_prob_a, 2)
    odds_b = round(1 / win_prob_b, 2)
    odds_draw = round(1 / draw_prob, 2)
    
    return odds_a, odds_draw, odds_b

# -------------------------------------------------------------------------
# 3. APP INITIALIZATION & APP STATE
# -------------------------------------------------------------------------
if 'balance' not in st.session_state:
    st.session_state.balance = 670.0

if 'matches' not in st.session_state:
    st.session_state.matches = INITIAL_MATCHES.copy()

if 'bets' not in st.session_state:
    st.session_state.bets = {}

if 'settled_results' not in st.session_state:
    st.session_state.settled_results = {}

if 'reset_cycle' not in st.session_state:
    st.session_state.reset_cycle = 0

# -------------------------------------------------------------------------
# 4. TOP HEADER LAYOUT (BRANDING & METRIC)
# -------------------------------------------------------------------------
header_left, header_right = st.columns([2, 1])

with header_left:
    st.title("💸 PayGone")
    st.caption("_Where your money goes... until you guess right!_")
    st.caption("**BEFORE SUBMITTING YOUR BET, CHECK YOUR BALANCE.**")

with header_right:
    st.metric(label="Wallet Balance", value=f"${st.session_state.balance:.2f}")

st.divider()

# Main Upper Tabs
tab1, tab2 = st.tabs(["📊 Matches & Betting", "⚙️ Admin Control Panel"])

# -------------------------------------------------------------------------
# TAB 1: USER INTERFACE (BETTING W/ SUBTABS)
# -------------------------------------------------------------------------
with tab1:
    cycle = st.session_state.reset_cycle
    
    # 🌟 NEW: Subtabs array mapping directly to match stages
    subtab_list = ["Matchday 1", "Matchday 2", "Matchday 3", "Round of 32", "Round of 16", "Quarterfinals", "Semifinals", "3rd Place Match", "Final"]
    subtabs = st.tabs(subtab_list)
    
    # Process each subtab layer independently
    for index, stage_name in enumerate(subtab_list):
        with subtabs[index]:
            st.header(f"Tournament Stage: {stage_name}")
            
            # Filter matches belonging exclusively to this subtab stage
            stage_matches = [m for m in st.session_state.matches if m['stage'] == stage_name]
            
            if not stage_matches:
                st.info("No fixtures available for this block stage.")
                
            for m in stage_matches:
                match_id = m['match_id']
                team_a, team_b = m['team_a'], m['team_b']
                
                odds_a, odds_draw, odds_b = calculate_odds(team_a, team_b)
                odds_map = {team_a: odds_a, "Draw": odds_draw, team_b: odds_b}
                
                # Render Clean Schedule View requested
                st.write(f"### {m['info']} — {team_a} vs. {team_b}")
                st.write(f"📅 **Date:** {m['date']} | ⏰ **Time:** {m['time']}")
                
                # Scenario A: Finished Match Layout
                if match_id in st.session_state.settled_results:
                    final_outcome = st.session_state.settled_results[match_id]
                    
                    if match_id in st.session_state.bets:
                        user_bet = st.session_state.bets[match_id]
                        if user_bet['choice'] == final_outcome:
                            st.success(f"✅ Result: **{final_outcome}** | **WIN 🎉** (+${user_bet['amount'] * user_bet['odds']:.2f})")
                        else:
                            st.error(f"✅ Result: **{final_outcome}** | **LOSE ❌** (-${user_bet['amount']:.2f})")
                    else:
                        st.info(f"✅ Result: **{final_outcome}** | No bet placed.")
                    
                # Scenario B: Open for Bets Layout
                else:
                    st.write(f"**PayGone Live Odds:** {team_a}: **{odds_a}** | Draw: **{odds_draw}** | {team_b}: **{odds_b}**")
                    
                    choice = st.radio("Pick an outcome:", [team_a, "Draw", team_b], key=f"pick_{match_id}_c{cycle}", horizontal=True)
                    
                    if st.session_state.balance < 1.0:
                        st.error("📉 You're broke! Go to the Admin Control Panel and reset the platform to get your cash back.")
                    else:
                        default_bet = min(10.0, float(st.session_state.balance))
                        bet_amount = st.number_input(
                            "Betting Amount ($)", 
                            min_value=1.0, 
                            max_value=float(st.session_state.balance), 
                            value=default_bet, 
                            key=f"amt_{match_id}_c{cycle}"
                        )
                        
                        if match_id in st.session_state.bets:
                            current_bet = st.session_state.bets[match_id]
                            st.info(f"🔒 Bet Locked: ${current_bet['amount']} on **{current_bet['choice']}**")
                        else:
                            if st.button("Submit PayGone Bet", key=f"btn_{match_id}_c{cycle}"):
                                st.session_state.bets[match_id] = {
                                    "choice": choice,
                                    "amount": bet_amount,
                                    "odds": odds_map[choice]
                                }
                                st.session_state.balance -= bet_amount
                                st.success(f"Bet registered successfully!")
                                st.rerun()
                            
                st.divider()

# -------------------------------------------------------------------------
# TAB 2: ADMIN INTERFACE (SETTLING & THE PLATFORM RESET)
# -------------------------------------------------------------------------
with tab2:
    st.header("PayGone Engine Settings")
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == "master":
        st.success("Authorized access granted.")
        
        # --- SYSTEM RESET ENGINE ---
        st.subheader("🧹 System Reset")
        st.write("Wipe all active user data, restore balances, and reset the schedule.")
        
        if st.button("🔴 Reset PayGone Platform", type="primary"):
            st.session_state.balance = 1000.0
            st.session_state.bets = {}
            st.session_state.settled_results = {}
            st.session_state.matches = INITIAL_MATCHES.copy()
            st.session_state.reset_cycle += 1 
            st.toast("Platform successfully restored to defaults!", icon="🔄")
            st.rerun()
            
        st.divider()
        
        # --- SETTLE MATCHES ---
        st.subheader("🏁 Resolve Live Matches")
        open_fixtures = [m for m in st.session_state.matches if m['match_id'] not in st.session_state.settled_results]
        
        if not open_fixtures:
            st.info("All scheduled matches have been completed.")
            
        for m in open_fixtures:
            match_id = m['match_id']
            team_a, team_b = m['team_a'], m['team_b']
            
            st.write(f"**Resolve [{m['stage']}]:** {team_a} vs {team_b}")
            actual_result = st.selectbox("Select Official Winner:", [team_a, "Draw", team_b], key=f"admin_res_{match_id}_c{cycle}")
            
            if st.button("Publish Official Result", key=f"admin_btn_{match_id}_c{cycle}"):
                st.session_state.settled_results[match_id] = actual_result
                
                if match_id in st.session_state.bets:
                    user_bet = st.session_state.bets[match_id]
                    
                    if user_bet['choice'] == actual_result:
                        winnings = user_bet['amount'] * user_bet['odds']
                        st.session_state.balance += winnings
                        st.toast(f"User won! Payout: ${winnings:.2f}", icon="💰")
                    else:
                        st.toast(f"User lost.", icon="❌")
                        
                st.rerun()
    elif password:
        st.error("Invalid passcode combination.")