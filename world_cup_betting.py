# world_cup_betting.py
import streamlit as st
import json
import os
import glob
import datetime
from filelock import FileLock

# --- IMPORT EXTERNAL PAGES & DATA ---
from matches import FIFA_SCORES, INITIAL_MATCHES
from real_results import render_real_results_page
import betting_hub
import db_manager 

APP_TITLE = "PAYGONE - FIFA WORLD CUP 2026 BETTING SIMULATOR"
RESULTS_FILE = "global_settled_results.json"
REQUESTS_FILE = "global_balance_requests.json"
FUN_BETS_FILE = "global_fun_bets.json"
ADMIN_PASSWORD = "master"

# -------------------------------------------------------------------------
# DATABASE UTILITIES
# -------------------------------------------------------------------------
def load_global_results():
    lock = FileLock(f"{RESULTS_FILE}.lock")
    with lock:
        if os.path.exists(RESULTS_FILE):
            try:
                with open(RESULTS_FILE, "r") as f:
                    data = json.load(f)
                    parsed = {}
                    for k, v in data.items():
                        try: key_converted = int(k)
                        except ValueError: key_converted = str(k)
                        if isinstance(v, dict): parsed[key_converted] = v
                        else: parsed[key_converted] = {"outcome": v, "score_text": "Settled"}
                    return parsed
            except: return {}
        return {}

def save_global_results(results_dict):
    lock = FileLock(f"{RESULTS_FILE}.lock")
    with lock:
        stringified_data = {str(k): v for k, v in results_dict.items()}
        try:
            with open(RESULTS_FILE, "w") as f: json.dump(stringified_data, f, indent=4)
        except: pass

def load_balance_requests():
    lock = FileLock(f"{REQUESTS_FILE}.lock")
    with lock:
        if os.path.exists(REQUESTS_FILE):
            try:
                with open(REQUESTS_FILE, "r") as f: return json.load(f)
            except: return []
        return []

def save_balance_requests(requests_list):
    lock = FileLock(f"{REQUESTS_FILE}.lock")
    with lock:
        with open(REQUESTS_FILE, "w") as f: json.dump(requests_list, f)

def load_fun_bets():
    lock = FileLock(f"{FUN_BETS_FILE}.lock")
    with lock:
        if os.path.exists(FUN_BETS_FILE):
            try:
                with open(FUN_BETS_FILE, "r") as f: return json.load(f)
            except: return {}
        return {}

def save_fun_bets(bets_dict):
    lock = FileLock(f"{FUN_BETS_FILE}.lock")
    with lock:
        with open(FUN_BETS_FILE, "w") as f: json.dump(bets_dict, f, indent=4)

def load_user_data(username: str):
    filename = f"user_{username.lower()}.json"
    lock = FileLock(f"{filename}.lock")
    with lock:
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                    data["bets"] = {int(k): v for k, v in data.get("bets", {}).items()}
                    data["processed_payouts"] = [int(x) for x in data.get("processed_payouts", [])]
                    if "parlays" not in data: data["parlays"] = []
                    if "favorite_country" not in data: data["favorite_country"] = ""
                    if "fun_bets" not in data: data["fun_bets"] = {}
                    return data
            except: pass
        return {"password": "", "balance": 1000.0, "bets": {}, "processed_payouts": [], "parlays": [], "favorite_country": "", "fun_bets": {}}

def save_user_data(username: str, data: dict):
    filename = f"user_{username.lower()}.json"
    lock = FileLock(f"{filename}.lock")
    with lock:
        with open(filename, "w") as f: json.dump(data, f)

def calculate_odds(team_a, team_b):
    rating_a = FIFA_SCORES.get(team_a, 1500.0)
    rating_b = FIFA_SCORES.get(team_b, 1500.0)
    total_rating = rating_a + rating_b
    prob_a = rating_a / total_rating
    prob_b = rating_b / total_rating
    return round(1 / (prob_a * 0.8), 2), round(1 / 0.20, 2), round(1 / (prob_b * 0.8), 2)
            
# -------------------------------------------------------------------------
# SECURED LOGIN SYSTEM
# -------------------------------------------------------------------------
if "current_user" not in st.session_state:
    st.title(f"🏆 {APP_TITLE}")
    st.subheader("Please sign in to access your dashboard")
    username_input = st.text_input("Enter Username:", value="").strip()
    password_input = st.text_input("Enter Password:", type="password", value="").strip()
    
    if st.button("Enter", use_container_width=True):
        if username_input == "": st.error("⚠️ Username field cannot be empty!")
        elif password_input == "": st.error("⚠️ Password field cannot be empty!")
        elif username_input.lower() == "admin":
            if password_input == ADMIN_PASSWORD:
                st.session_state.current_user = "Admin"
                st.session_state.balance = 0.0
                st.session_state.bets = {}
                st.session_state.processed_payouts = []
                st.session_state.matches = INITIAL_MATCHES.copy()
                st.session_state.reset_cycle = 0
                st.rerun()
            else: st.error("❌ Incorrect profile password!")
        else:
            filename = f"user_{username_input.lower()}.json"
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
                else: st.error("❌ Incorrect profile password!")
            else:
                new_profile = {"password": password_input, "balance": 1000.0, "bets": {}, "processed_payouts": [], "parlays": [], "favorite_country": "", "fun_bets": {}}
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

username_input = st.session_state.current_user
user_profile = load_user_data(username_input)
global_results = load_global_results()
global_fun_bets = load_fun_bets()

if "parlay_cart" not in st.session_state: st.session_state.parlay_cart = {}

# Payout Calculation Automation Loops
payout_happened = False
for match_id, user_bet in list(st.session_state.bets.items()):
    target_key = int(match_id) if int(match_id) in global_results else (str(match_id) if str(match_id) in global_results else None)
    if target_key is not None and int(match_id) not in st.session_state.processed_payouts:
        if isinstance(user_bet, dict) and user_bet.get('choice') == global_results[target_key].get("outcome"):
            st.session_state.balance += (user_bet.get('amount', 0.0) * user_bet.get('odds', 1.0))
        st.session_state.processed_payouts.append(int(match_id))
        payout_happened = True

if "parlays" in user_profile:
    for parlay in user_profile["parlays"]:
        if parlay.get("status") == "OPEN":
            all_settled, parlay_won = True, True
            for m_id, leg in parlay["legs"].items():
                t_leg_key = int(m_id) if int(m_id) in global_results else (str(m_id) if str(m_id) in global_results else None)
                if t_leg_key is not None:
                    if leg["choice"] != global_results[t_leg_key].get("outcome"): parlay_won = False
                else: all_settled = False
            if all_settled:
                parlay["status"] = "SETTLED"
                if parlay_won:
                    st.session_state.balance += parlay["potential_payout"]
                    st.toast(f"🎉 PARLAY WINNER! Received ${parlay['potential_payout']:.2f}!")
                else: st.toast("❌ Parlay Busted!")
                payout_happened = True

for prop_id, user_wager in list(user_profile.get("fun_bets", {}).items()):
    if prop_id in global_fun_bets and global_fun_bets[prop_id]["status"] != "OPEN" and not user_wager.get("paid", False):
        if user_wager["choice"] == global_fun_bets[prop_id]["status"]:
            st.session_state.balance += (user_wager["amount"] * user_wager["odds"])
        user_wager["paid"] = True
        payout_happened = True

if payout_happened:
    user_profile.update({"balance": st.session_state.balance, "processed_payouts": st.session_state.processed_payouts})
    save_user_data(username_input, user_profile)

cycle = st.session_state.reset_cycle

# -------------------------------------------------------------------------
# SIDEBAR NAVIGATION & ADMIN CONTROLS
# -------------------------------------------------------------------------
with st.sidebar:
    st.write(f"Active Profile: **{username_input.upper()}**")
    menu_selection = st.radio("Navigate System:", ["🕹️ Hub", "💰 Balance", "🏆 Leaderboard", "⚽ Real Results"], index=0)
    
    if st.button("🚪 Logout / Switch Account", use_container_width=True):
        if "parlay_cart" in st.session_state: st.session_state.parlay_cart = {}
        del st.session_state.current_user
        st.rerun()
        
    with st.expander("🛠️ Admin Panel"):
        admin_password = st.text_input("Access Token Key", type="password")
        if admin_password == ADMIN_PASSWORD:
            st.caption("🟢 Admin Control Authenticated")
            
            # 1. Accounts Data View
            user_files = glob.glob("user_*.json")
            user_credentials = [({"Username": os.path.basename(f).replace("user_", "").replace(".json", "").upper(), "Balance": f"${load_user_data(os.path.basename(f).replace('user_', '').replace('.json', '')).get('balance', 0.0):.2f}"}) for f in user_files]
            if user_credentials: st.dataframe(user_credentials, use_container_width=True)
            
            # 2. Deposit Requests Processing Queue
            pending_requests = load_balance_requests()
            for idx, req in enumerate(list(pending_requests)):
                st.write(f"**Player:** {req['user'].upper()} | **Amount:** ${req['amount']:.2f}")
                st.caption(f"Reason: {req.get('reason')}")
                c_app, c_rej = st.columns(2)
                if c_app.button("Approve", key=f"app_{idx}"):
                    t_data = load_user_data(req['user'])
                    t_data["balance"] += req['amount']
                    save_user_data(req['user'], t_data)
                    if req['user'].lower() == username_input.lower(): st.session_state.balance = t_data["balance"]
                    pending_requests.pop(idx); save_balance_requests(pending_requests); st.rerun()
                if c_rej.button("Reject", key=f"rej_{idx}"):
                    pending_requests.pop(idx); save_balance_requests(pending_requests); st.rerun()
            
            # 3. Fast Global Resets
            if st.button("🔴 Reset Loaded Wallet Data", type="primary"):
                st.session_state.update({"balance": 1000.0, "bets": {}, "processed_payouts": [], "parlay_cart": {}})
                user_profile.update({"balance": 1000.0, "bets": {}, "processed_payouts": [], "parlays": [], "fun_bets": {}})
                save_user_data(username_input, user_profile); st.session_state.reset_cycle += 1; st.rerun()
            if st.button("🚨 Wipe All Match Results GLOBALLY"):
                save_global_results({}); save_fun_bets({}); st.rerun()
            
            # 4. Admin Scoreboard View Updates
            st.divider()
            from real_results import REAL_WORLD_CUP_DATA, get_match_uid
            rw_phase = st.selectbox("Select Display Phase:", list(REAL_WORLD_CUP_DATA.keys()))
            rw_cat = st.selectbox("Select Display Category:", list(REAL_WORLD_CUP_DATA[rw_phase].keys()))
            rw_matches = REAL_WORLD_CUP_DATA[rw_phase][rw_cat]
            rw_idx = st.selectbox("Choose Display Fixture:", range(len(rw_matches)), format_func=lambda x: f"{rw_matches[x]['team_a']} vs {rw_matches[x]['team_b']}")
            target_rw_match = rw_matches[rw_idx]
            real_uid = str(get_match_uid(rw_phase, rw_cat, target_rw_match['team_a'], target_rw_match['team_b']))
            
            new_real_score = st.text_input("Scoreline:", value=target_rw_match['score'], key=f"rw_scr_{real_uid}")
            new_real_status = st.selectbox("Display Status:", ["Scheduled", "Live", "Finished"], key=f"rw_st_{real_uid}")
            if st.button("Publish Scoreboard Update", key=f"rw_btn_{real_uid}", use_container_width=True):
                db = load_global_results()
                db[real_uid] = {"outcome": "Settled", "score_text": new_real_score.strip(), "status": new_real_status}
                save_global_results(db); st.rerun()

            # 5. Settle Real Match Bets
            st.divider()
            open_fixtures = [m for m in st.session_state.matches if int(m['match_id']) not in load_global_results()]
            if open_fixtures:
                b_options = {f"Match #{m['match_id']}: {m['team_a']} vs {m['team_b']}": m for m in open_fixtures}
                sel_str = st.selectbox("Select Bet Target to Settle:", list(b_options.keys()))
                bm = b_options[sel_str]
                outcome_choice = st.radio("Winning Outcome:", [bm['team_a'], "Draw", bm['team_b']], horizontal=True)
                f_a = st.number_input(f"{bm['team_a']} Goals", min_value=0, value=0)
                f_b = st.number_input(f"{bm['team_b']} Goals", min_value=0, value=0)
                if st.button("Finalize Payouts & Close Wagers", key=f"pay_b_{bm['match_id']}", use_container_width=True, type="primary"):
                    db = load_global_results()
                    db[int(bm['match_id'])] = {"outcome": outcome_choice, "score_text": f"{f_a} - {f_b}", "status": "Finished"}
                    save_global_results(db); st.rerun()

            # 6. Admin Special Props Builder
            st.divider()
            with st.form("create_prop_form", clear_on_submit=True):
                prop_desc = st.text_input("Bet Prompt Description:")
                p_odds = st.number_input("Odds Multiple (x):", min_value=1.1, value=2.5)
                # Fixed the typo method name here:
                if st.form_submit_button("Publish Prop Bet Line"):
                    if prop_desc.strip():
                        props = load_fun_bets()
                        props[f"prop_{int(datetime.datetime.now().timestamp())}"] = {"description": prop_desc.strip(), "odds": round(p_odds, 2), "status": "OPEN"}
                        save_fun_bets(props); st.rerun()

            open_props_admin = {k: v for k, v in global_fun_bets.items() if v["status"] == "OPEN"}
            if open_props_admin:
                target_prop_id = st.selectbox("Select prop to resolve:", list(open_props_admin.keys()), format_func=lambda x: open_props_admin[x]["description"])
                settle_outcome = st.radio("Official Outcome:", ["HIT", "MISSED"], horizontal=True)
                if st.button("Finalize Prop Bet Payouts", use_container_width=True):
                    global_fun_bets[target_prop_id]["status"] = settle_outcome
                    save_fun_bets(global_fun_bets); st.rerun()

# -------------------------------------------------------------------------
# INTERFACE CONTENT ROUTER
# -------------------------------------------------------------------------
st.markdown(f"## 🏆 {APP_TITLE}")

if menu_selection == "🕹️ Hub":
    st.title("🕹️ Betting Hub")
    st.metric(label="Your Current Balance", value=f"${st.session_state.balance:.2f}")
    st.divider()

    parent_tab_matches, parent_tab_others = st.tabs(["⚽ Matches", "🎉 Others"])

    # ⚽ TAB 1: MATCHES 
    with parent_tab_matches:
        betting_hub.render_matches_tab(
            user_profile=user_profile,
            username_input=username_input,
            global_results=global_results,
            cycle=cycle,
            calculate_odds=calculate_odds
        )

    # 🎉 TAB 2: OTHERS (STAYS IN MAIN FILE SINCE IT IS VERY SHORT)
    with parent_tab_others:
        st.subheader("🎉 Special Custom Friends Bets")
        if not global_fun_bets: st.info("No custom prop bets have been created by the admin yet.")
        else:
            for p_id, prop in global_fun_bets.items():
                st.markdown(f"### ✨ Bet: *\"{prop['description']}\"*")
                st.write(f"📈 Odds: **{prop['odds']}x**")
                if prop["status"] != "OPEN":
                    st.write(f"🏁 **Result:** `{prop['status']}`")
                    if p_id in user_profile.get("fun_bets", {}):
                        st.success("✅ WIN!") if user_profile["fun_bets"][p_id]["choice"] == prop["status"] else st.error("❌ LOST!")
                else:
                    if p_id in user_profile.get("fun_bets", {}):
                        st.info(f"🔒 Ticket Logged: Staked **${user_profile['fun_bets'][p_id]['amount']}** on `{user_profile['fun_bets'][p_id]['choice']}`")
                    else:
                        prop_choice = st.radio("Will this happen?", ["HIT", "MISSED"], key=f"choice_{p_id}", horizontal=True)
                        prop_amount = st.number_input("Wager Amount ($)", min_value=100.0, max_value=float(st.session_state.balance), value=100.0, key=f"amt_{p_id}")
                        if st.button("Submit Fun Bet", key=f"submit_{p_id}"):
                            user_profile.setdefault("fun_bets", {})[p_id] = {"choice": prop_choice, "amount": prop_amount, "odds": prop["odds"], "paid": False}
                            st.session_state.balance -= prop_amount; user_profile["balance"] = st.session_state.balance
                            save_user_data(username_input, user_profile); st.rerun()
                st.divider()

elif menu_selection == "💰 Balance":
    st.title("💰 Balance & Financial Logs")
    st.divider()
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("Available Balance", f"${st.session_state.balance:.2f}")
    
    # Calculate Total Earnings
    total_payout_earnings = sum((b['amount'] * b['odds']) for mid, b in st.session_state.bets.items() if (int(mid) in global_results and b['choice'] == global_results[int(mid)]['outcome']))
    m_col2.metric("Total Generated Revenue", f"${total_payout_earnings:.2f}")

    # History Line Chart Display Logic
    st.subheader("📊 Balance History Timeline")
    balance_history, chart_labels = [1000.0], ["Registration"]
    curr_bal = 1000.0
    if st.session_state.bets:
        for mid, bet in sorted(st.session_state.bets.items(), key=lambda x: str(x[0])):
            if int(mid) in global_results:
                curr_bal -= bet['amount']
                if global_results[int(mid)]['outcome'] == bet['choice']: curr_bal += (bet['amount'] * bet['odds'])
                balance_history.append(curr_bal); chart_labels.append(f"Match #{mid}")
    if len(balance_history) <= 1: st.info("📉 Timeline will populate once first prediction is settled.")
    else: st.line_chart(data={"Match Milestone": chart_labels, "Account Balance ($)": balance_history}, x="Match Milestone", y="Account Balance ($)")

    # Favorite Country Setup Tracker Dropdown
    st.divider()
    country_options = sorted(list(FIFA_SCORES.keys()))
    current_fav = user_profile.get("favorite_country", "")
    selected_fav = st.selectbox("Choose your favorite nation to track:", options=["None"] + country_options, index=0 if current_fav == "" else country_options.index(current_fav) + 1)
    updated_fav_val = "" if selected_fav == "None" else selected_fav
    if updated_fav_val != current_fav:
        user_profile["favorite_country"] = updated_fav_val; save_user_data(username_input, user_profile); st.rerun()

    # Balance Deposit Request Forms Queue
    st.subheader("💳 Request Deposit Authorization")
    deposit_amount = st.number_input("Specify Volume ($):", min_value=10.0, max_value=500.0, value=500.0)
    deposit_reason = st.text_area("Reason for request:")
    if st.button("Submit Balance Request", use_container_width=True):
        if not deposit_reason.strip(): st.error("⚠️ Reason required!")
        else:
            reqs = load_balance_requests(); reqs.append({"user": username_input, "amount": deposit_amount, "reason": deposit_reason.strip()})
            save_balance_requests(reqs); st.success("Dispatched to admin queue!")

elif menu_selection == "🏆 Leaderboard":
    st.title("🏆 Standing Leaderboard")
    user_files = glob.glob("user_*.json")
    leaderboard_records = []
    for file_path in user_files:
        r_name = os.path.basename(file_path).replace("user_", "").replace(".json", "")
        u_d = load_user_data(r_name)
        leaderboard_records.append({"Player": r_name.upper(), "Current Balance": f"${u_d.get('balance', 0.0):.2f}"})
    st.dataframe(leaderboard_records, use_container_width=True)

elif menu_selection == "⚽ Real Results":
    render_real_results_page()

st.markdown("---")
st.caption("🤖 PAYGONE Simulator Engine")
