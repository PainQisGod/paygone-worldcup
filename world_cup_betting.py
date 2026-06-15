import streamlit as st
import json
import os

# -------------------------------------------------------------------------
# DATABASE PATHS & UTILITIES
# -------------------------------------------------------------------------
RESULTS_FILE = "global_settled_results.json"

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
                data["processed_payouts"] = set(data.get("processed_payouts", []))
                return data
        except:
            pass
    return {"balance": 670.0, "bets": {}, "processed_payouts": set()}

def save_user_data(username, balance, bets, processed_payouts):
    filename = get_user_file(username)
    data = {
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
    "🇦🇷 Argentina": 1877.27, "🇪🇸 Spain": 1874.71, "🇫🇷 France": 1870.70, "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England": 1828.02,
    "🇵🇹 Portugal": 1767.85, "🇧🇷 Brazil": 1765.86, "🇲🇦 Morocco": 1755.10, "🇳🇱 Netherlands": 1753.57,
    "🇧🇪 Belgium": 1742.24, "🇩🇪 Germany": 1735.77, "🇭🇷 Croatia": 1714.87, "🇨🇴 Colombia": 1698.35,
    "🇲🇽 Mexico": 1687.48, "🇸🇳 Senegal": 1684.07, "🇺🇾 Uruguay": 1673.07, "🇺🇸 USA": 1671.23,
    "🇯🇵 Japan": 1661.58, "🇨🇭 Switzerland": 1650.06, "🇮🇷 Iran": 1619.58, "🇹🇷 Turkiye": 1605.73,
    "🇪🇨 Ecuador": 1598.52, "🇦🇹 Austria": 1597.40, "🇰🇷 Korea Republic": 1591.63, "🇦🇺 Australia": 1579.34,
    "🇩🇿 Algeria": 1571.03, "🇪🇬 Egypt": 1562.37, "🇨🇦 Canada": 1559.48, "🇳🇴 Norway": 1557.44,
    "🇨🇮 Ivory Coast": 1540.87, "🇵🇦 Panama": 1539.16, "🇸🇪 Sweden": 1509.79, "🇨🇿 Czechia": 1505.74,
    "🇵🇾 Paraguay": 1505.35, "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland": 1503.34, "🇹🇳 Tunisia": 1476.41, "🇨🇩 Congo DR": 1747.43,
    "🇺🇿 Uzbekistan": 1458.20, "🇶🇦 Qatar": 1450.31, "🇮🇶 Iraq": 1446.28, "🇿🇦 South Africa": 1428.38,
    "🇸🇦 Saudi Arabia": 1423.88, "🇯🇴 Jordan": 1387.74, "🇧🇦 Bosnia and Herzegovina": 1387.22,
    "🇨🇻 Cabo Verde": 1371.11, "🇬🇭 Ghana": 1346.88, "🇨🇼 Curacao": 1294.77, "🇭🇹 Haiti": 1293.10,
    "🇳🇿 New Zealand": 1275.58
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
    {"match_id": 24, "stage": "Matchday 1", "info": "Group K", "team_a": "🇺🇿 Uzbekistan", "team_b": "🇨🇴 Colombia", "date": "June 18, 2026", "time": "9:00AM (UTC+7)"}
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
st.sidebar.title("👤 Player Profile ID")
username_input = st.sidebar.text_input("Enter Profile Name to Load Wallet:", value="").strip()

if not username_input:
    st.title("💸 PayGone Simulator")
    st.info("👈 Please enter a nickname in the sidebar on the left to sign in!")
    st.stop()

# -------------------------------------------------------------------------
# LOAD USER DATA & DETECT ROUTE
# -------------------------------------------------------------------------
user_profile = load_user_data(username_input)
st.session_state.balance = user_profile["balance"]
st.session_state.bets = user_profile["bets"]
st.session_state.processed_payouts = user_profile["processed_payouts"]
st.session_state.matches = INITIAL_MATCHES.copy()

global_results = load_global_results()
payout_happened = False

for match_id in list(st.session_state.bets.keys()):
    if match_id in global_results and match_id not in st.session_state.processed_payouts:
        actual_winner = global_results[match_id]
        user_bet = st.session_state.bets[match_id]
        if user_bet['choice'] == actual_winner:
            st.session_state.balance += (user_bet['amount'] * user_bet['odds'])
        st.session_state.processed_payouts.add(match_id)
        payout_happened = True

if payout_happened:
    save_user_data(username_input, st.session_state.balance, st.session_state.bets, st.session_state.processed_payouts)

if 'reset_cycle' not in st.session_state:
    st.session_state.reset_cycle = 0

cycle = st.session_state.reset_cycle

# Check if admin parameter is passed in URL
is_admin_route = st.query_params.get("view") == "admin"

# -------------------------------------------------------------------------
# 3. ROUTING SWITCH
# -------------------------------------------------------------------------
if is_admin_route:
    st.title("⚙️ Secret PayGone Engine")
    st.caption(f"Authenticated Context: Administering user **{username_input.upper()}**")
    
    password = st.text_input("Enter Master Admin Password", type="password")
    if password == "master":
        st.success("Authorized administrator access verified.")
        
        st.subheader("🧹 System Reset Controls")
        if st.button("🔴 Reset Loaded Wallet Data", type="primary"):
            st.session_state.balance = 670.0
            st.session_state.bets = {}
            st.session_state.processed_payouts = set()
            save_user_data(username_input, 670.0, {}, set())
            st.session_state.reset_cycle += 1 
            st.toast("Profile wallet wiped back to $670!", icon="🔄")
            st.rerun()
            
        if st.button("🚨 Wipe All Match Results GLOBALLY"):
            save_global_results({})
            st.toast("All matches unlocked globally!", icon="🔓")
            st.rerun()
            
        st.divider()
        st.subheader("🏁 Resolve Live Matches Globally")
        open_fixtures = [m for m in st.session_state.matches if m['match_id'] not in global_results]
        
        if not open_fixtures:
            st.info("All matches successfully closed.")
            
        for m in open_fixtures:
            match_id = m['match_id']
            team_a, team_b = m['team_a'], m['team_b']
            st.write(f"**Resolve [{m['stage']}]:** {team_a} vs {team_b}")
            actual_result = st.selectbox("Select Official Winner:", [team_a, "Draw", team_b], key=f"admin_res_{match_id}_c{cycle}")
            
            if st.button("Publish Official Result", key=f"admin_btn_{match_id}_c{cycle}"):
                current_live_results = load_global_results()
                current_live_results[match_id] = actual_result
                save_global_results(current_live_results)
                
                if match_id in st.session_state.bets and match_id not in st.session_state.processed_payouts:
                    user_bet = st.session_state.bets[match_id]
                    if user_bet['choice'] == actual_result:
                        st.session_state.balance += (user_bet['amount'] * user_bet['odds'])
                    st.session_state.processed_payouts.add(match_id)
                    save_user_data(username_input, st.session_state.balance, st.session_state.bets, st.session_state.processed_payouts)
                
                st.toast(f"Result pushed globally!", icon="📣")
                st.rerun()
    elif password:
        st.error("Access denied.")

else:
    # --- REGULAR PLAYER VIEW ---
    header_left, header_right = st.columns([2, 1])
    with header_left:
        st.title("💸 PayGone")
        st.caption(f"Active Account: **{username_input.upper()}** — Progress is automatically saved!")
    with header_right:
        st.metric(label="Wallet Balance", value=f"${st.session_state.balance:.2f}")

    st.divider()
    
    subtab_list = ["Matchday 1"]
    subtabs = st.tabs(subtab_list)
    
    for index, stage_name in enumerate(subtab_list):
        with subtabs[index]:
            st.header(f"Tournament Stage: {stage_name}")
            stage_matches = [m for m in st.session_state.matches if m['stage'] == stage_name]
            
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
                        st.info(f"✅ Result: **{final_outcome}** | No bet placed.")
                else:
                    st.write(f"**Live Odds:** {team_a}: **{odds_a}** | Draw: **{odds_draw}** | {team_b}: **{odds_b}**")
                    choice = st.radio("Pick an outcome:", [team_a, "Draw", team_b], key=f"pick_{match_id}_c{cycle}", horizontal=True)
                    
                    if st.session_state.balance < 1.0:
                        st.error("📉 Balance depleted!")
                    else:
                        default_bet = min(10.0, float(st.session_state.balance))
                        bet_amount = st.number_input("Betting Amount ($)", min_value=1.0, max_value=float(st.session_state.balance), value=default_bet, key=f"amt_{match_id}_c{cycle}")
                        
                        if match_id in st.session_state.bets:
                            current_bet = st.session_state.bets[match_id]
                            st.info(f"🔒 Locked: ${current_bet['amount']} on **{current_bet['choice']}**")
                        else:
                            if st.button("Submit PayGone Bet", key=f"btn_{match_id}_c{cycle}"):
                                st.session_state.bets[match_id] = {"choice": choice, "amount": bet_amount, "odds": odds_map[choice]}
                                st.session_state.balance -= bet_amount
                                save_user_data(username_input, st.session_state.balance, st.session_state.bets, st.session_state.processed_payouts)
                                st.success(f"Bet secured!")
                                st.rerun()
                st.divider()
