import streamlit as st
import json
import os

# -------------------------------------------------------------------------
# DATABASE PATHS & UTILITIES
# -------------------------------------------------------------------------
RESULTS_FILE = "global_settled_results.json"
REQUESTS_FILE = "global_balance_requests.json"

def load_global_results():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r") as f:
                data = json.load(f)
                return {int(k): v for k, v in data.items()}
        except:
            return {}
    return {}

def save_global_results(results_dict):
    with open(RESULTS_FILE, "w") as f:
        json.dump(results_dict, f)

def load_balance_requests():
    if os.path.exists(REQUESTS_FILE):
        try:
            with open(REQUESTS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_balance_requests(requests_list):
    with open(REQUESTS_FILE, "w") as f:
        json.dump(requests_list, f)

def get_user_file(username):
    safe_name = "".join(c for c in username if c.isalnum() or c in (' ', '_', '-')).strip()
    return f"user_{safe_name.lower()}.json"

def load_user_data(username):
    filename = get_user_file(username)
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                data["bets"] = {int(k): v for k, v in data.get("bets", {}).items()}
                data["processed_payouts"] = [int(x) for x in data.get("processed_payouts", [])]
                return data
        except:
            pass
    return {"password": None, "balance": 1000.0, "bets": {}, "processed_payouts": []}

def save_user_data(username, password, balance, bets, processed_payouts):
    filename = get_user_file(username)
    data = {
        "password": password,
        "balance": balance,
        "bets": bets,
        "processed_payouts": list(processed_payouts)
    }
    with open(filename, "w") as f:
        json.dump(data, f)

# -------------------------------------------------------------------------
# 1. FIFA WORLD RANKING POINTS DATA
# -------------------------------------------------------------------------
FIFA_SCORES = {
    "🇲🇽 Mexico": 1687.48, "🇿🇦 South Africa": 1428.38, "🇰🇷 Korea Republic": 1591.63, "🇨🇿 Czechia": 1505.74,
    "🇨🇦 Canada": 1559.48, "🇧🇦 Bosnia and Herzegovina": 1387.22, "🇺🇸 USA": 1671.23, "🇵🇾 Paraguay": 1505.35,
    "🇶🇦 Qatar": 1450.31, "🇨🇭 Switzerland": 1650.06, "🇧🇷 Brazil": 1765.86, "🇲🇦 Morocco": 1755.10,
    "🇭🇹 Haiti": 1293.10, "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland": 1503.34, "🇦🇺 Australia": 1579.34, "🇹🇷 Turkiye": 1605.73,
    "🇩🇪 Germany": 1735.77, "🇨🇼 Curacao": 1294.77, "🇳🇱 Netherlands": 1753.57, "🇯🇵 Japan": 1661.58,
    "🇨🇮 Ivory Coast": 1540.87, "🇪🇨 Ecuador": 1598.52, "🇸🇪 Sweden": 1509.79, "🇹🇳 Tunisia": 1476.41,
    "🇪🇸 Spain": 1874.71, "🇨🇻 Cabo Verde": 1371.11, "🇧🇪 Belgium": 1742.24, "🇪🇬 Egypt": 1562.37,
    "🇸🇦 Saudi Arabia": 1423.88, "🇺🇾 Uruguay": 1673.07, "🇮🇷 Iran": 1619.58, "🇳🇿 New Zealand": 1275.58,
    "🇫🇷 France": 1870.70, "🇸🇳 Senegal": 1684.07, "🇮🇶 Iraq": 1446.28, "🇳🇴 Norway": 1557.44,
    "🇦🇷 Argentina": 1877.27, "🇩🇿 Algeria": 1571.03, "🇦🇹 Austria": 1597.40, "🇯🇴 Jordan": 1387.74,
    "🇵🇹 Portugal": 1767.85, "🇨🇩 Congo DR": 1747.43, "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England": 1828.02, "🇭🇷 Croatia": 1714.87,
    "🇬🇭 Ghana": 1346.88, "🇵🇦 Panama": 1539.16, "🇺🇿 Uzbekistan": 1458.20, "🇨🇴 Colombia": 1698.35
}

INITIAL_MATCHES = [
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
    {"match_id": 38, "stage": "Matchday 2", "info": "Group G", "team_a": "🇧🇪 Belgium", "team_b": "🇪🇬 Egypt", "date": "June 22, 2026", "time": "2:00AM (UTC+7)"},
    {"match_id": 39, "stage": "Matchday 2", "info": "Group H", "team_a": "🇺🇾 Uruguay", "team_b": "🇨🇻 Cabo Verde", "date": "June 22, 2026", "time": "5:00AM (UTC+7)"},
    {"match_id": 40, "stage": "Matchday 2", "info": "Group G", "team_a": "🇳🇿 New Zealand", "team_b": "🇮🇷 Iran", "date": "June 22, 2026", "time": "8:00AM (UTC+7)"},
    {"match_id": 41, "stage": "Matchday 2", "info": "Group J", "team_a": "🇦🇷 Argentina", "team_b": "🇦🇹 Austria", "date": "June 23, 2026", "time": "12:00AM (UTC+7)"},
    {"match_id": 42, "stage": "Matchday 2", "info": "Group I", "team_a": "🇫🇷 France", "team_b": "🇮🇶 Iraq", "date": "June 23, 2026", "time": "4:00AM (UTC+7)"},
    {"match_id": 43, "stage": "Matchday 2", "info": "Group I", "team_a": "🇳🇴 Norway", "team_b": "🇸🇳 Senegal", "date": "June 23, 2026", "time": "7:00AM (UTC+7)"},
    {"match_id": 44, "stage": "Matchday 2", "info": "Group J", "team_a": "🇯🇴 Jordan", "team_b": "🇩🇿 Algeria", "date": "June 23, 2026", "time": "10:00AM (UTC+7)"},
    {"match_id": 45, "stage": "Matchday 2", "info": "Group K", "team_a": "🇵🇹 Portugal", "team_b": "🇺🇿 Uzbekistan", "date": "June 24, 2026", "time": "12:00AM (UTC+7)"},
    {"match_id": 46, "stage": "Matchday 2", "info": "Group L", "team_a": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England", "team_b": "🇬🇭 Ghana", "date": "June 24, 2026", "time": "3:00AM (UTC+7)"},
    {"match_id": 47, "stage": "Matchday 2", "info": "Group K", "team_a": "🇵🇦 Panama", "team_b": "🇭🇷 Croatia", "date": "June 24, 2026", "time": "6:00AM (UTC+7)"},
    {"match_id": 48, "stage": "Matchday 2", "info": "Group L", "team_a": "🇨🇴 Colombia", "team_b": "🇨🇩 Congo DR", "date": "June 24, 2026", "time": "9:00AM (UTC+7)"},
    
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
    {"match_id": 65, "stage": "Matchday 3", "info": "Group G", "team_a": "🇪🇬 Egypt", "team_b": "🇳🇿 New Zealand", "date": "June 27, 2026", "time": "10:00AM (UTC+7)"},
    {"match_id": 66, "stage": "Matchday 3", "info": "Group G", "team_a": "🇮🇷 Iran", "team_b": "🇧🇪 Belgium", "date": "June 27, 2026", "time": "10:00AM (UTC+7)"},
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

def calculate_odds(team_a, team_b):
    rating_a = FIFA_SCORES.get(team_a, 1500.0)
    rating_b = FIFA_SCORES.get(team_b, 1500.0)
    total_rating = rating_a + rating_b
    prob_a = rating_a / total_rating
    prob_b = rating_b / total_rating
    win_prob_a = prob_a * 0.8
    win_prob_b = prob_b * 0.8
    draw_prob = 0.20
    return round(1 / win_prob_a, 2), round(1 / draw_prob, 2), round(1 / win_prob_b, 2)

# -------------------------------------------------------------------------
# 2. PROFILE SIGN-IN STEP
# -------------------------------------------------------------------------
APP_TITLE = "PAYGONE - FIFA WORLD CUP 2026 BETTING SIMULATOR"

if "current_user" not in st.session_state:
    st.title(f"💸 {APP_TITLE}")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("### 👤 Player Profile Sign-In")
        username_input = st.text_input("Profile Name:", value="").strip()
        password_input = st.text_input("Profile Password Key:", type="password", value="").strip()
        submit_login = st.button("Enter")
        
    if submit_login:
        if not username_input or not password_input:
            st.error("⚠️ Both Profile Name and Password are required.")
        else:
            user_profile = load_user_data(username_input)
            if user_profile.get("password") is not None:
                if user_profile["password"] != password_input:
                    st.error("❌ Incorrect profile password!")
                    st.stop()
            else:
                user_profile["password"] = password_input
                save_user_data(username_input, password_input, user_profile["balance"], user_profile["bets"], user_profile["processed_payouts"])

            st.session_state.current_user = username_input
            st.session_state.user_password = password_input
            st.session_state.balance = user_profile["balance"]
            st.session_state.bets = user_profile["bets"]
            st.session_state.processed_payouts = list(user_profile["processed_payouts"])
            st.session_state.matches = INITIAL_MATCHES.copy()
            st.session_state.reset_cycle = 0
            st.rerun()
    else:
        st.stop()

# --- REAL-TIME WALLET PAYOUT UPDATE PATTERN ---
username_input = st.session_state.current_user
user_password = st.session_state.user_password
global_results = load_global_results()
payout_happened = False

for match_id, user_bet in list(st.session_state.bets.items()):
    if match_id in global_results and match_id not in st.session_state.processed_payouts:
        actual_winner = global_results[match_id]
        if user_bet['choice'] == actual_winner:
            st.session_state.balance += (user_bet['amount'] * user_bet['odds'])
        st.session_state.processed_payouts.append(match_id)
        payout_happened = True

if payout_happened:
    save_user_data(username_input, user_password, st.session_state.balance, st.session_state.bets, st.session_state.processed_payouts)

cycle = st.session_state.reset_cycle

# -------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION CONTROLS
# -------------------------------------------------------------------------
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
            font-size: 22px !important;
            font-weight: bold !important;
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] label[data-testid="stRadioOption"] p {
            font-size: 20px !important;
            font-weight: 500 !important;
        }
        [data-testid="stSidebar"] gap {
            gap: 15px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.write(f"Logged in as: **{username_input.upper()}**")
    menu_selection = st.radio("Navigate System:", ["🕹️ Hub", "💰 Balance"], index=0)
    
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    with st.expander("🛠️"):
        admin_password = st.text_input("Access Token Key", type="password")
        if admin_password == "master":
            st.caption("Admin Mode")
            
            # --- ADMIN ACTION: BALANCE REQUESTS APPROVAL SECTION ---
            st.markdown("#### 📥 Balance Request Queue")
            pending_requests = load_balance_requests()
            if not pending_requests:
                st.info("No balance reloads awaiting validation.")
            else:
                for idx, req in enumerate(pending_requests):
                    st.write(f"**Player:** {req['user'].upper()} | **Amount:** ${req['amount']:.2f}")
                    col_app, col_rej = st.columns(2)
                    if col_app.button("Approve", key=f"app_{idx}"):
                        target_user = req['user']
                        t_data = load_user_data(target_user)
                        t_data["balance"] += req['amount']
                        save_user_data(target_user, t_data["password"], t_data["balance"], t_data["bets"], t_data["processed_payouts"])
                        
                        # If current admin session is also the requestor, update local session tracking dynamically
                        if target_user.lower() == username_input.lower():
                            st.session_state.balance = t_data["balance"]
                            
                        pending_requests.pop(idx)
                        save_balance_requests(pending_requests)
                        st.rerun()
                        
                    if col_rej.button("Reject", key=f"rej_{idx}"):
                        pending_requests.pop(idx)
                        save_balance_requests(pending_requests)
                        st.rerun()
            st.divider()
            
            if st.button("🔴 Reset Loaded Wallet Data", type="primary"):
                st.session_state.balance = 1000.0
                st.session_state.bets = {}
                st.session_state.processed_payouts = []
                save_user_data(username_input, user_password, 1000.0, {}, [])
                st.session_state.reset_cycle += 1
                st.rerun()
            if st.button("🚨 Wipe All Match Results GLOBALLY"):
                save_global_results({})
                st.rerun()
            
            st.divider()
            open_fixtures = [m for m in st.session_state.matches if m['match_id'] not in global_results]
            for m in open_fixtures:
                match_id = m['match_id']
                actual_result = st.selectbox(f"Winner: {m['team_a']} vs {m['team_b']}", [m['team_a'], "Draw", m['team_b']], key=f"admin_res_{match_id}_c{cycle}")
                if st.button("Publish Result", key=f"admin_btn_{match_id}_c{cycle}"):
                    current_live_results = load_global_results()
                    current_live_results[match_id] = actual_result
                    save_global_results(current_live_results)
                    st.rerun()

# -------------------------------------------------------------------------
# 4. MAIN LAYOUT CONTAINER
# -------------------------------------------------------------------------
st.markdown(f"## 🏆 {APP_TITLE}")

if menu_selection == "🕹️ Hub":
    st.title("🕹️ Betting Hub")
    
    # --- DYNAMIC BALANCE METRIC DISPLAY IN HUB ---
    st.metric(label="Your Current Balance", value=f"${st.session_state.balance:.2f}")
    
    st.caption("Select a tournament tier tab below to browse match listings. Minimum bet requirement: **$100.00**.")
    st.divider()

    subtab_list = ["Matchday 1", "Matchday 2", "Matchday 3", "Round of 32", "Round of 16", "Quarterfinals", "Semifinals", "3rd Place Match", "Final"]
    subtabs = st.tabs(subtab_list)

    for index, stage_name in enumerate(subtab_list):
        with subtabs[index]:
            stage_matches = [m for m in st.session_state.matches if m['stage'] == stage_name]
            
            if not stage_matches:
                st.info("No schedule mapped for this block.")
            
            for m in stage_matches:
                match_id = m['match_id']
                team_a, team_b = m['team_a'], m['team_b']
                odds_a, odds_draw, odds_b = calculate_odds(team_a, team_b)
                odds_map = {team_a: odds_a, "Draw": odds_draw, team_b: odds_b}
                
                st.write(f"### {m['info']} — {team_a} vs. {team_b}")
                st.write(f"📅 **Date:** {m['date']} | ⏰ **Time:** {m['time']}")
                
                if match_id in global_results:
                    final_outcome = global_results[match_id]
                    if match_id in st.session_state.bets:
                        user_bet = st.session_state.bets[match_id]
                        if user_bet['choice'] == final_outcome:
                            st.success(f"✅ Result: **{final_outcome}** | **WIN 🎉** (+${user_bet['amount'] * user_bet['odds']:.2f})")
                        else:
                            st.error(f"✅ Result: **{final_outcome}** | **LOSE ❌** (-${user_bet['amount']:.2f})")
                    else:
                        st.info(f"✅ Result: **{final_outcome}** | No bet placed")
                else:
                    st.write(f"**Live Odds:** {team_a}: **{odds_a}** | Draw: **{odds_draw}** | {team_b}: **{odds_b}**")
                    choice = st.radio("Pick outcome:", [team_a, "Draw", team_b], key=f"pick_{match_id}_c{cycle}", horizontal=True)
                    
                    if st.session_state.balance < 100.0:
                        st.error("📉 Insufficient Balance! Minimum required wager is $100.00. Go to 'Balance' panel to reload funds.")
                    else:
                        bet_amount = st.number_input("Wager Amount ($)", min_value=100.0, max_value=float(st.session_state.balance), value=100.0, step=50.0, key=f"amt_{match_id}_c{cycle}")
                        
                        if match_id in st.session_state.bets:
                            current_bet = st.session_state.bets[match_id]
                            st.info(f"🔒 Active Stake locked: ${current_bet['amount']} on **{current_bet['choice']}**")
                        else:
                            if st.button("Submit Bet Slip", key=f"btn_{match_id}_c{cycle}"):
                                st.session_state.bets[match_id] = {"choice": choice, "amount": bet_amount, "odds": odds_map[choice]}
                                st.session_state.balance -= bet_amount
                                save_user_data(username_input, user_password, st.session_state.balance, st.session_state.bets, st.session_state.processed_payouts)
                                st.success("Bet securely logged into history registry!")
                                st.rerun()
                st.divider()

elif menu_selection == "💰 Balance":
    st.title("💰 Balance & Financial Logs")
    st.write("Review active assets, execute structural wallet reloads, or observe overall historic yields.")
    st.divider()

    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(label="Current Available Liquid Balance", value=f"${st.session_state.balance:.2f}")
    with m_col2:
        total_payout_earnings = 0.0
        for mid, bet in st.session_state.bets.items():
            if mid in global_results and global_results[mid] == bet['choice']:
                total_payout_earnings += (bet['amount'] * bet['odds'])
        st.metric(label="Total Generated Winning Revenue", value=f"${total_payout_earnings:.2f}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💳 Request Deposit Authorization")
    deposit_amount = st.number_input("Specify Deposit Volume ($):", min_value=10.0, max_value=25000.0, value=500.0, step=100.0)
    if st.button("Submit Balance Request to Admin Queue", use_container_width=True):
        current_requests = load_balance_requests()
        current_requests.append({"user": username_input, "amount": deposit_amount})
        save_balance_requests(current_requests)
        st.success(f"✅ Request for ${deposit_amount:.2f} dispatched successfully. Waiting for admin approval.")

    st.divider()
    st.subheader("📊 Performance Ledger History")
    
    if not st.session_state.bets:
        st.info("No logs present on this profile context yet.")
    else:
        for mid, bet in st.session_state.bets.items():
            m = next((match for match in st.session_state.matches if match['match_id'] == mid), None)
            if m:
                if mid in global_results:
                    is_winner = bet['choice'] == global_results[mid]
                    status_banner = "🟢 WON PAYOUT" if is_winner else "🔴 LOST SLIP"
                else:
                    status_banner = "🟡 OPEN PROPOSITION"
                
                with st.expander(f"{status_banner} — {m['team_a']} vs {m['team_b']}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**Predicted Outcome:** {bet['choice']}")
                        st.write(f"**Initial Locked Amount:** ${bet['amount']:.2f}")
                    with col_b:
                        st.write(f"**Odds Multiple:** x{bet['odds']}")
                        if mid in global_results:
                            st.write(f"**Official Field Result:** {global_results[mid]}")
                            if is_winner:
                                st.markdown(f"**Net Received Return:** <span style='color:green'>+${bet['amount'] * bet['odds']:.2f}</span>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"**Net Loss Value:** <span style='color:red'>-${bet['amount']:.2f}</span>", unsafe_allow_html=True)
                        else:
                            st.caption("Waiting for tournament resolution data updates...")
