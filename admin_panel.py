# admin_panel.py
import streamlit as st
import glob
import os
import datetime
import db_manager
from real_results import REAL_WORLD_CUP_DATA, get_match_uid

def render_admin(ADMIN_PASSWORD, INITIAL_MATCHES):
    admin_password = st.text_input("Access Token Key", type="password")
    if admin_password != ADMIN_PASSWORD:
        return
        
    st.caption("🟢 Admin Control Authenticated")
    global_results = db_manager.load_global_results()
    global_fun_bets = db_manager.load_fun_bets()
    
    # 1. Accounts Data Overview
    st.divider()
    st.markdown("#### 🔑 Global Accounts Overview")
    user_files = glob.glob("user_*.json")
    user_credentials = []
    user_list_clean = []
    for file_path in user_files:
        raw_name = os.path.basename(file_path).replace("user_", "").replace(".json", "")
        u_data = db_manager.load_user_data(raw_name)
        user_list_clean.append(raw_name)
        user_credentials.append({"Username": raw_name.upper(), "Balance": f"${u_data.get('balance', 0.0):.2f}"})
    if user_credentials: st.dataframe(user_credentials, use_container_width=True)

    # 2. Deposit Requests
    st.divider()
    st.markdown("#### 📥 Balance Request Queue")
    pending_requests = db_manager.load_balance_requests()
    for idx, req in enumerate(list(pending_requests)):
        st.write(f"**Player:** {req['user'].upper()} | **Amount:** ${req['amount']:.2f}")
        col_app, col_rej = st.columns(2)
        if col_app.button("Approve", key=f"app_{idx}"):
            t_data = db_manager.load_user_data(req['user'])
            t_data["balance"] += req['amount']
            db_manager.save_user_data(req['user'], t_data)
            pending_requests.pop(idx)
            db_manager.save_balance_requests(pending_requests)
            st.rerun()
        if col_rej.button("Reject", key=f"rej_{idx}"):
            pending_requests.pop(idx)
            db_manager.save_balance_requests(pending_requests)
            st.rerun()

    # 3. Update Real Scores Display
    st.divider()
    st.markdown("#### 🌐 Update Scoreboard View")
    rw_phase = st.selectbox("Select Display Phase:", list(REAL_WORLD_CUP_DATA.keys()))
    rw_cat = st.selectbox("Select Display Category:", list(REAL_WORLD_CUP_DATA[rw_phase].keys()))
    rw_matches = REAL_WORLD_CUP_DATA[rw_phase][rw_cat]
    rw_idx = st.selectbox("Choose Display Fixture:", range(len(rw_matches)), format_func=lambda x: f"{rw_matches[x]['team_a']} vs {rw_matches[x]['team_b']}")
    
    target_rw_match = rw_matches[rw_idx]
    real_uid = str(get_match_uid(rw_phase, rw_cat, target_rw_match['team_a'], target_rw_match['team_b']))
    
    new_real_score = st.text_input("Scoreline:", value=target_rw_match['score'], key=f"scr_{real_uid}")
    new_real_status = st.selectbox("Display Status:", ["Scheduled", "Live", "Finished"], key=f"st_{real_uid}")
    if st.button("Publish Scoreboard Update", key=f"pub_{real_uid}", use_container_width=True):
        global_results[real_uid] = {"outcome": "Settled", "score_text": new_real_score.strip(), "status": new_real_status}
        db_manager.save_global_results(global_results)
        st.rerun()

    # 4. Force Settle User Bets
    st.divider()
    st.markdown("#### 💰 Force Settle Active User Bets")
    open_fixtures = [m for m in INITIAL_MATCHES if int(m['match_id']) not in global_results]
    if open_fixtures:
        bet_match_options = {f"Match #{m['match_id']}: {m['team_a']} vs {m['team_b']}": m for m in open_fixtures}
        sel_str = st.selectbox("Select Bet Target to Settle:", list(bet_match_options.keys()))
        bm = bet_match_options[sel_str]
        outcome_choice = st.radio("Winning Outcome:", [bm['team_a'], "Draw", bm['team_b']], horizontal=True)
        f_a = st.number_input(f"{bm['team_a']} Goals", min_value=0, value=0)
        f_b = st.number_input(f"{bm['team_b']} Goals", min_value=0, value=0)
        if st.button("Finalize Payouts & Close Wagers", use_container_width=True, type="primary"):
            global_results[int(bm['match_id'])] = {"outcome": outcome_choice, "score_text": f"{f_a} - {f_b}", "status": "Finished"}
            db_manager.save_global_results(global_results)
            st.rerun()

    # 🔒 4.1. FIXED: Manual Match Lock Control Panel
    st.divider()
    st.markdown("#### 🎛️ Manual Match Lock Dashboard")
    st.caption("Manually close or reopen betting windows for individual fixtures.")

    # Filter by stage to avoid a massive wall of text
    match_stages = list(set([m['stage'] for m in INITIAL_MATCHES]))
    lock_stage_filter = st.selectbox("Filter Lock Panel by Stage:", match_stages, key="lock_stage_filter")
    filtered_lock_matches = [m for m in INITIAL_MATCHES if m['stage'] == lock_stage_filter]

    for m in filtered_lock_matches:
        m_id = m['match_id']
        uid_str = str(m_id)
        
        # Look up the match's lock status directly inside global_results database
        is_currently_locked = global_results.get(uid_str, {}).get("status") == "Locked"
            
        with st.container():
            col_info, col_toggle = st.columns([2, 1])
            with col_info:
                st.write(f"**Match #{m_id}:** {m['team_a']} vs {m['team_b']}")
                status_emoji = "🔴 LOCKED" if is_currently_locked else "🟢 OPEN"
                st.write(f"Status: **{status_emoji}**")
            with col_toggle:
                lock_state = st.toggle("Close Bets", value=is_currently_locked, key=f"global_lock_{m_id}")
                
                if lock_state != is_currently_locked:
                    if lock_state:
                        # Write a "Locked" status signature into your global results file
                        global_results[uid_str] = {"status": "Locked", "outcome": None, "score_text": "Betting Closed"}
                    else:
                        # Reopen it by removing the lock signature block
                        if uid_str in global_results and global_results[uid_str].get("status") == "Locked":
                            del global_results[uid_str]
                            
                    db_manager.save_global_results(global_results)
                    st.success(f"Updated Match #{m_id} lock status globally!")
                    st.rerun()

    # 5. Custom Novelty Side Bets
    st.divider()
    st.markdown("#### 🎉 Manage Custom Fun Prop Bets")
    with st.form("create_prop_form", clear_on_submit=True):
        prop_desc = st.text_input("Bet Prompt Description:")
        p_odds = st.number_input("Odds Multiple (x):", min_value=1.1, value=2.5)
        if st.form_submit_button("Publish Prop Bet Line"):
            if prop_desc.strip():
                global_fun_bets[f"prop_{int(datetime.datetime.now().timestamp())}"] = {"description": prop_desc.strip(), "odds": round(p_odds, 2), "status": "OPEN"}
                db_manager.save_fun_bets(global_fun_bets)
                st.rerun()
