import streamlit as st
import json
import os
import glob

# -------------------------------------------------------------------------
# CONSTANTS & MODULAR DATA IMPORT
# -------------------------------------------------------------------------
from matches import FIFA_SCORES, INITIAL_MATCHES
from real_results import render_real_results_page

APP_TITLE = "PAYGONE - FIFA WORLD CUP 2026 BETTING SIMULATOR"
RESULTS_FILE = "global_settled_results.json"
REQUESTS_FILE = "global_balance_requests.json"
ADMIN_PASSWORD = "master"

# -------------------------------------------------------------------------
# PERSISTENT SYSTEM READ/WRITE UTILITIES
# -------------------------------------------------------------------------
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

def load_user_data(username: str):
    filename = f"user_{username.lower()}.json"
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                data["bets"] = {int(k): v for k, v in data.get("bets", {}).items()}
                data["processed_payouts"] = [int(x) for x in data.get("processed_payouts", [])]
                return data
        except:
            pass
    return {"password": "", "balance": 1000.0, "bets": {}, "processed_payouts": []}

def save_user_data(username: str, data: dict):
    filename = f"user_{username.lower()}.json"
    with open(filename, "w") as f:
        json.dump(data, f)

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
# SECURED LOGIN SYSTEM (WITH PASSWORD VALIDATION)
# -------------------------------------------------------------------------
if "current_user" not in st.session_state:
    st.title(f"🏆 {APP_TITLE}")
    st.subheader("Please sign in to access your dashboard")
    
    username_input = st.text_input("Enter Username:", value="").strip()
    password_input = st.text_input("Enter Password:", type="password", value="").strip()
    
    if st.button("Enter", use_container_width=True):
        if username_input == "":
            st.error("⚠️ Username field cannot be empty!")
        elif password_input == "":
            st.error("⚠️ Password field cannot be empty!")
        
        # --- Handle Admin Login ---
        elif username_input.lower() == "admin":
            if password_input == ADMIN_PASSWORD:
                st.session_state.current_user = "Admin"
                st.session_state.balance = 0.0
                st.session_state.bets = {}
                st.session_state.processed_payouts = []
                st.session_state.matches = INITIAL_MATCHES.copy()
                st.session_state.reset_cycle = 0
                st.rerun()
            else:
                st.error("❌ Incorrect profile password!")
                
        # --- Handle Standard Player Login ---
        else:
            filename = f"user_{username_input.lower()}.json"
            
            # Scenario A: Existing User -> Verify Password
            if os.path.exists(filename):
                user_profile = load_user_data(username_input)
                if user_profile.get("password") == password_input:
                    st.session_state.current_user = username_input
                    st.session_state.balance = user_profile["balance"]
                    st.session_state.bets = user_profile["bets"]
                    st.session_state.processed_payouts = list(user_profile["processed_payouts"])
                    st.session_state.matches = INITIAL_MATCHES.copy()
                    st.session_state.reset_cycle = 0
                    st.rerun()
                else:
                    st.error("❌ Incorrect profile password!")
            
            # Scenario B: Brand New User -> Account Registration
            else:
                new_profile = {
                    "password": password_input,
                    "balance": 1000.0,
                    "bets": {},
                    "processed_payouts": []
                }
                save_user_data(username_input, new_profile)
                
                st.session_state.current_user = username_input
                st.session_state.balance = new_profile["balance"]
                st.session_state.bets = new_profile["bets"]
                st.session_state.processed_payouts = []
                st.session_state.matches = INITIAL_MATCHES.copy()
                st.session_state.reset_cycle = 0
                st.success("🎉 New account registered securely!")
                st.rerun()
    st.stop()

# --- RE-LOAD LOGGED-IN SESSION CONTEXT ---
username_input = st.session_state.current_user
user_profile = load_user_data(username_input)
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
    user_profile["balance"] = st.session_state.balance
    user_profile["processed_payouts"] = st.session_state.processed_payouts
    save_user_data(username_input, user_profile)

cycle = st.session_state.reset_cycle

# -------------------------------------------------------------------------
# SIDEBAR NAVIGATION CONTROLS & LOGOUT
# -------------------------------------------------------------------------
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { font-size: 22px !important; font-weight: bold !important; color: #ffffff !important; }
        [data-testid="stSidebar"] label[data-testid="stRadioOption"] p { font-size: 20px !important; font-weight: 500 !important; }
        [data-testid="stSidebar"] gap { gap: 15px !important; }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.write(f"Active Profile: **{username_input.upper()}**")
    menu_selection = st.radio("Navigate System:", ["🕹️ Hub", "💰 Balance", "🏆 Leaderboard", "⚽ Real Results"], index=0)
    
    if st.button("🚪 Logout / Switch Account", use_container_width=True):
        del st.session_state.current_user
        st.rerun()
        
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    with st.expander("🛠️ Admin Panel"):
        admin_password = st.text_input("Access Token Key", type="password")
        if admin_password == ADMIN_PASSWORD:
            st.caption("🟢 Admin Control Authenticated")
            
            # -------------------------------------------------------------
            # USER LIST VIEW
            # -------------------------------------------------------------
            st.divider()
            st.markdown("#### 🔑 Global Accounts Overview")
            
            user_files = glob.glob("user_*.json")
            user_credentials = []
            user_list_clean = []
            
            for file_path in user_files:
                try:
                    with open(file_path, "r") as f:
                        u_data = json.load(f)
                    raw_name = os.path.basename(file_path).replace("user_", "").replace(".json", "")
                    display_name = raw_name.upper()
                    user_list_clean.append(raw_name)
                    
                    user_credentials.append({
                        "Username": display_name,
                        "Balance": f"${u_data.get('balance', 0.0):.2f}"
                    })
                except:
                    pass
            
            if not user_credentials:
                st.info("No user profiles detected.")
            else:
                st.dataframe(user_credentials, use_container_width=True)
            
            # -------------------------------------------------------------
            # ADMINISTRATIVE PASSWORD OVERRIDE
            # -------------------------------------------------------------
            st.divider()
            st.markdown("#### 🔄 Administrative Password Override")
            if not user_list_clean:
                st.info("No player accounts available to reset.")
            else:
                target_reset_user = st.selectbox("Select Profile to Modify:", options=user_list_clean, format_func=lambda x: x.upper())
                new_forced_password = st.text_input("Assign New Password:", type="password", key="force_pw_input").strip()
                
                if st.button("Force Update Password", use_container_width=True):
                    if new_forced_password == "":
                        st.error("⚠️ New password string cannot be empty!")
                    else:
                        account_data = load_user_data(target_reset_user)
                        account_data["password"] = new_forced_password
                        save_user_data(target_reset_user, account_data)
                        st.success(f"🔒 Password for account **{target_reset_user.upper()}** changed successfully!")
            
            # -------------------------------------------------------------
            # BALANCE REQUEST QUEUE
            # -------------------------------------------------------------
            st.divider()
            st.markdown("#### 📥 Balance Request Queue")
            pending_requests = load_balance_requests()
            if not pending_requests:
                st.info("No balance reloads awaiting validation.")
            else:
                for idx, req in enumerate(pending_requests):
                    st.write(f"**Player:** {req['user'].upper()} | **Amount:** ${req['amount']:.2f}")
                    st.info(f"💬 **Reason given:** *\"{req.get('reason', 'No reason specified')}\"*")
                    
                    col_app, col_rej = st.columns(2)
                    if col_app.button("Approve", key=f"app_{idx}"):
                        target_user = req['user']
                        t_data = load_user_data(target_user)
                        t_data["balance"] += req['amount']
                        save_user_data(target_user, t_data)
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
                user_profile["balance"] = 1000.0
                user_profile["bets"] = {}
                user_profile["processed_payouts"] = []
                save_user_data(username_input, user_profile)
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
# MAIN LAYOUT CONTAINER
# -------------------------------------------------------------------------
st.markdown(f"## 🏆 {APP_TITLE}")

if menu_selection == "🕹️ Hub":
    st.title("🕹️ Betting Hub")
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
                        st.error("📉 Insufficient Balance! Minimum required wager is $100.00.")
                    else:
                        bet_amount = st.number_input("Wager Amount ($)", min_value=100.0, max_value=float(st.session_state.balance), value=100.0, step=50.0, key=f"amt_{match_id}_c{cycle}")
                        if match_id in st.session_state.bets:
                            current_bet = st.session_state.bets[match_id]
                            st.info(f"🔒 Active Stake locked: ${current_bet['amount']} on **{current_bet['choice']}**")
                        else:
                            if st.button("Submit Bet Slip", key=f"btn_{match_id}_c{cycle}"):
                                st.session_state.bets[match_id] = {"choice": choice, "amount": bet_amount, "odds": odds_map[choice]}
                                st.session_state.balance -= bet_amount
                                user_profile["balance"] = st.session_state.balance
                                user_profile["bets"] = st.session_state.bets
                                save_user_data(username_input, user_profile)
                                st.success("Bet securely logged into history registry!")
                                st.rerun()
                st.divider()

elif menu_selection == "💰 Balance":
    st.title("💰 Balance & Financial Logs")
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
    deposit_amount = st.number_input("Specify Deposit Volume ($):", min_value=10.0, max_value=500.0, value=500.0, step=50.0)
    deposit_reason = st.text_area("State your reason for this request:", value="", placeholder="e.g., Please approve this request to back up my next series of bids.")
    
    if st.button("Submit Balance Request to Admin Queue", use_container_width=True):
        if deposit_reason.strip() == "":
            st.error("⚠️ You must provide a reason to request funds!")
        else:
            current_requests = load_balance_requests()
            current_requests.append({
                "user": username_input, 
                "amount": deposit_amount,
                "reason": deposit_reason.strip()
            })
            save_balance_requests(current_requests)
            st.success(f"✅ Request for ${deposit_amount:.2f} dispatched successfully.")

    st.divider()
    st.subheader("📊 Performance Ledger History")
    if not st.session_state.bets:
        st.info("No wagers logged on this profile yet.")
    else:
        for mid, bet in st.session_state.bets.items():
            m = next((match for match in st.session_state.matches if match['match_id'] == mid), None)
            if m:
                status_banner = "🟡 OPEN PROPOSITION"
                if mid in global_results:
                    status_banner = "🟢 WON PAYOUT" if bet['choice'] == global_results[mid] else "🔴 LOST SLIP"
                
                with st.expander(f"{status_banner} — {m['team_a']} vs {m['team_b']}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**Predicted Outcome:** {bet['choice']}")
                        st.write(f"**Initial Locked Amount:** ${bet['amount']:.2f}")
                    with col_b:
                        st.write(f"**Odds Multiple:** x{bet['odds']}")
                        if mid in global_results:
                            st.write(f"**Official Field Result:** {global_results[mid]}")
                            if bet['choice'] == global_results[mid]:
                                st.markdown(f"**Net Received Return:** <span style='color:green'>+${bet['amount'] * bet['odds']:.2f}</span>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"**Net Loss Value:** <span style='color:red'>-${bet['amount']:.2f}</span>", unsafe_allow_html=True)
                        else:
                            st.caption("Waiting for tournament resolution data updates...")

elif menu_selection == "🏆 Leaderboard":
    st.title("🏆 Profit Standings Leaderboard")
    st.divider()
    
    leaderboard_records = []
    user_files = glob.glob("user_*.json")
    
    for file_path in user_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                
            display_name = os.path.basename(file_path).replace("user_", "").replace(".json", "").upper()
            bets = {int(k): v for k, v in data.get("bets", {}).items()}
            
            total_winnings = 0.0
            for mid, bet in bets.items():
                if mid in global_results and global_results[mid] == bet['choice']:
                    total_winnings += (bet['amount'] * bet['odds'])
                    
            leaderboard_records.append({
                "Player": display_name,
                "Current Balance": f"${data.get('balance', 0.0):.2f}",
                "Total Winning Revenue": total_winnings
            })
        except:
            pass
            
    leaderboard_records = sorted(leaderboard_records, key=lambda x: x["Total Winning Revenue"], reverse=True)
    for row in leaderboard_records:
        row["Total Winning Revenue"] = f"${row['Total Winning Revenue']:.2f}"
    
    if not leaderboard_records:
        st.info("No profile records detected to establish leaderboard metrics yet.")
    else:
        st.dataframe(
            leaderboard_records,
            use_container_width=True,
            column_config={
                "Player": "👤 Profile Username",
                "Current Balance": "💳 Available Wallet",
                "Total Winning Revenue": "💰 Earned Winning Revenue"
            }
        )
        st.balloons()
        st.success(f"🥇 Current frontrunner dominating the ranks: **{leaderboard_records[0]['Player']}**!")

# --- ROUTER FOR THE MODULAR REAL RESULTS PAGE ---
elif menu_selection == "⚽ Real Results":
    render_real_results_page()

st.markdown("---")
st.caption("🤖 PAYGONE Simulator Engine • Calculated using live FIFA Performance Indices.")
