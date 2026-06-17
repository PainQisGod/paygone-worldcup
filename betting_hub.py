# betting_hub.py
import streamlit as st
import datetime

# Clean import from our new independent database manager!
from db_manager import save_user_data

def render_matches_tab(user_profile, username_input, global_results, cycle, calculate_odds):
    # 🚩 1. Favorite Country Tracker
    fav_nation = user_profile.get("favorite_country", "")
    if fav_nation:
        with st.expander(f"⭐ TRACKER: Your Favorite Nation ({fav_nation.upper()})", expanded=True):
            nation_matches = [m for m in st.session_state.matches if m['team_a'] == fav_nation or m['team_b'] == fav_nation]
            
            if not nation_matches:
                st.info(f"No scheduled fixtures logged for {fav_nation} in this segment.")
            else:
                past_matches = [m for m in nation_matches if m['match_id'] in global_results]
                upcoming_matches = [m for m in nation_matches if m['match_id'] not in global_results]
                
                track_col1, track_col2 = st.columns(2)
                with track_col1:
                    st.markdown("#### 📅 Next Fixture")
                    if upcoming_matches:
                        next_m = upcoming_matches[0]
                        opp = next_m['team_b'] if next_m['team_a'] == fav_nation else next_m['team_a']
                        st.write(f"**🆚 vs {opp}** ({next_m['stage']})")
                        st.caption(f"🗓️ {next_m['date']} at {next_m['time']}")
                        
                        o_a, o_d, o_b = calculate_odds(next_m['team_a'], next_m['team_b'])
                        st.write(f"📈 Odds to Win: **{o_a if next_m['team_a'] == fav_nation else o_b}x** | Draw: **{o_d}x**")
                    else:
                        st.write("🏁 No more upcoming matches scheduled for this phase.")
                        
                with track_col2:
                    st.markdown("#### 📊 Team Form & Bets")
                    wins, losses, draws = 0, 0, 0
                    bet_won_count, bet_lost_count = 0, 0
                    
                    for pm in past_matches:
                        res = global_results[pm['match_id']]
                        outcome = res.get("outcome")
                        if outcome == fav_nation: wins += 1
                        elif outcome == "Draw": draws += 1
                        else: losses += 1
                            
                        mid = pm['match_id']
                        if mid in st.session_state.bets:
                            if st.session_state.bets[mid]['choice'] == outcome: bet_won_count += 1
                            else: bet_lost_count += 1
                                
                    st.write(f"**On-Field Record:** `{wins}W - {draws}D - {losses}L`")
                    st.write(f"**Your Bet History:** `{bet_won_count} Won` / `{bet_lost_count} Lost`")
    else:
        st.info("💡 Tip: Go to the **💰 Balance** page to pick your favorite country and track them here!")
    
    st.divider()

    # --- Mode Selection ---
    betting_mode = st.radio(
        "Select Slip Mode Configuration:",
        ["🎫 Single Match Bets", "🔥 Matchday Parlay Slip Tracker"],
        horizontal=True
    )
    st.divider()

    subtab_list = ["Matchday 1", "Matchday 2", "Matchday 3", "Round of 32", "Round of 16", "Quarterfinals", "Semifinals", "3rd Place Match", "Final"]
    subtabs = st.tabs(subtab_list)

    for index, stage_name in enumerate(subtab_list):
        with subtabs[index]:
            stage_matches = [m for m in st.session_state.matches if m['stage'] == stage_name]
            stage_m_ids = [str(sm['match_id']) for sm in stage_matches]
            
            # Collapsible Parlay Viewer
            active_parlays = [p for p in user_profile.get("parlays", []) if p.get("stage") == stage_name]
            if active_parlays:
                st.markdown(f"### 📋 Your Locked Parlays for `{stage_name.upper()}`")
                for p_idx, open_parlay in enumerate(active_parlays):
                    p_status = open_parlay.get("status", "OPEN")
                    status_emoji = "🟡" if p_status == "OPEN" else "🟢"
                    
                    with st.expander(f"{status_emoji} Parlay #{p_idx + 1} — Multiplier: {open_parlay['combined_odds']}x", expanded=False):
                        st.markdown(f"**Wager Stake:** `${open_parlay['stake']:.2f}` | **Potential Return:** `${open_parlay['potential_payout']:.2f}`")
                        st.divider()
                        for m_id, leg in open_parlay["legs"].items():
                            if int(m_id) in global_results:
                                act = global_results[int(m_id)].get("outcome")
                                score_txt = global_results[int(m_id)].get("score_text", "")
                                color = "🟢" if leg['choice'] == act else "🔴"
                                st.markdown(f"• {color} **{leg['teams']}** — Picked `{leg['choice']}` ({score_txt})")
                            else:
                                st.markdown(f"• ⏳ **{leg['teams']}** — Picked `{leg['choice']}` ({leg['odds']}x)")
                st.divider()

            # Parlay Builder Panel
            if betting_mode == "🔥 Matchday Parlay Slip Tracker":
                active_stage_cart = {k: v for k, v in st.session_state.parlay_cart.items() if k in stage_m_ids}
                if active_stage_cart:
                    st.markdown(f"### 📝 Active `{stage_name.upper()}` Parlay Builder")
                    accumulated_odds = 1.0
                    for m_key, leg_info in list(active_stage_cart.items()):
                        st.write(f"🔸 **{leg_info['teams']}** | Picked: `{leg_info['choice']}` @ **{leg_info['odds']}x**")
                        accumulated_odds *= leg_info['odds']
                    
                    accumulated_odds = round(accumulated_odds, 2)
                    st.markdown(f"**Combined Multiplier Score:** `{accumulated_odds}x`")
                    
                    if st.session_state.balance < 100.0:
                        st.error("📉 Insufficient Balance to back a parlay!")
                    else:
                        parlay_wager = st.number_input(f"Stake Amount ($):", min_value=100.0, max_value=float(st.session_state.balance), value=100.0, step=50.0, key=f"parlay_val_{stage_name}_c{cycle}")
                        pot_return = round(parlay_wager * accumulated_odds, 2)
                        st.info(f"💰 **Estimated Winning Revenue Return:** `${pot_return:.2f}`")
                        
                        p_col1, p_col2 = st.columns(2)
                        if p_col1.button("🔒 Authorize & Finalize Parlay", key=f"lock_parlay_{stage_name}", use_container_width=True, type="primary"):
                            new_parlay_obj = {
                                "stage": stage_name,
                                "timestamp": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
                                "stake": parlay_wager,
                                "combined_odds": accumulated_odds,
                                "potential_payout": pot_return,
                                "status": "OPEN",
                                "legs": active_stage_cart
                            }
                            user_profile["parlays"] = user_profile.get("parlays", [])
                            user_profile["parlays"].append(new_parlay_obj)
                            st.session_state.balance -= parlay_wager
                            user_profile["balance"] = st.session_state.balance
                            db_manager.save_user_data(username_input, user_profile)
                            
                            for purged_key in active_stage_cart.keys():
                                del st.session_state.parlay_cart[purged_key]
                            st.success("Successfully locked combo slip sequence!")
                            st.rerun()
                            
                        if p_col2.button("🗑️ Reset Selection Layout", key=f"clear_parlay_{stage_name}", use_container_width=True):
                            for purged_key in active_stage_cart.keys():
                                del st.session_state.parlay_cart[purged_key]
                            st.rerun()
                else:
                    st.info(f"ℹ️ Select match entry combinations below to start crafting your `{stage_name}` Parlay accumulator.")
                st.divider()

            # Render Individual Fixtures
            if not stage_matches:
                st.info("No schedule mapped for this block.")
            
            for m in stage_matches:
                match_id = m['match_id']
                str_mid = str(match_id)
                team_a, team_b = m['team_a'], m['team_b']
                odds_a, odds_draw, odds_b = calculate_odds(team_a, team_b)
                odds_map = {team_a: odds_a, "Draw": odds_draw, team_b: odds_b}
                
                st.write(f"### {m['info']} — {team_a} vs. {team_b}")
                st.write(f"📅 **Date:** {m['date']} | ⏰ **Time:** {m['time']}")
                
                try:
                    kickoff_str = f"{m['date']} 2026 {m['time']}"
                    is_locked = datetime.datetime.now() >= datetime.datetime.strptime(kickoff_str, "%d %B %Y %I:%M%p")
                except:
                    is_locked = False
                
                # Settle checks
                if int(match_id) in global_results:
                    res_data = global_results[int(match_id)]
                    final_outcome = res_data.get("outcome")
                    st.write(f"🔢 **Final Score:** {res_data.get('score_text', 'Settled')}")
                    if match_id in st.session_state.bets:
                        if st.session_state.bets[match_id].get('choice') == final_outcome:
                            st.success(f"✅ Result: **{final_outcome}** | **WIN 🎉**")
                        else:
                            st.error(f"✅ Result: **{final_outcome}** | **LOSE ❌**")
                elif is_locked:
                    st.warning("🔒 Wagers Locked! This match has already kicked off.")
                    if match_id in st.session_state.bets:
                        st.info(f"📋 Locked Slip: Placed ${st.session_state.bets[match_id]['amount']:.2f} on **{st.session_state.bets[match_id]['choice']}**")
                else:
                    st.write(f"**Live Odds:** {team_a}: **{odds_a}** | Draw: **{odds_draw}** | {team_b}: **{odds_b}**")
                    
                    already_in_parlay = any(str_mid in p.get("legs", {}) and p.get("status") == "OPEN" for p in user_profile.get("parlays", []))
                    if already_in_parlay:
                        st.warning("🔒 Staked in an active open Parlay bundle.")
                    else:
                        choice = st.radio("Pick outcome:", [team_a, "Draw", team_b], key=f"pick_{match_id}_c{cycle}", horizontal=True)
                        if betting_mode == "🎫 Single Match Bets":
                            if st.session_state.balance >= 100.0:
                                bet_amount = st.number_input("Wager Amount ($)", min_value=100.0, max_value=float(st.session_state.balance), value=100.0, step=50.0, key=f"amt_{match_id}_c{cycle}")
                                if match_id in st.session_state.bets:
                                    st.info(f"🔒 Active Stake locked: ${st.session_state.bets[match_id]['amount']} on **{st.session_state.bets[match_id]['choice']}**")
                                else:
                                    if st.button("Submit Bet Slip", key=f"btn_{match_id}_c{cycle}"):
                                        st.session_state.bets[match_id] = {"choice": choice, "amount": bet_amount, "odds": odds_map[choice]}
                                        st.session_state.balance -= bet_amount
                                        user_profile["balance"] = st.session_state.balance
                                        user_profile["bets"] = st.session_state.bets
                                        db_manager.save_user_data(username_input, user_profile)
                                        st.success("Bet securely logged!")
                                        st.rerun()
                        else:
                            if str_mid in st.session_state.parlay_cart:
                                st.success(f"➕ Staged: **{st.session_state.parlay_cart[str_mid]['choice']}**")
                                if st.button("❌ Remove From Cart", key=f"rem_parlay_{match_id}_c{cycle}"):
                                    del st.session_state.parlay_cart[str_mid]
                                    st.rerun()
                            else:
                                if st.button("➕ Stage to Matchday Parlay Combo", key=f"add_parlay_{match_id}_c{cycle}", use_container_width=True):
                                    st.session_state.parlay_cart[str_mid] = {"teams": f"{team_a} vs {team_b}", "choice": choice, "odds": odds_map[choice]}
                                    st.rerun()
                st.divider()