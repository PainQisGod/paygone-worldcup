import streamlit as st
import json
import os
import hashlib
from filelock import FileLock

RESULTS_FILE = "global_settled_results.json"

def get_match_uid(phase, category, team_a, team_b):
    """
    Looks up the matching simulation ID from the data structure 
    to synchronize betting payouts seamlessly.
    """
    try:
        match_list = REAL_WORLD_CUP_DATA[phase][category]
        for m in match_list:
            if m["team_a"].strip().lower() == team_a.strip().lower() and m["team_b"].strip().lower() == team_b.strip().lower():
                return str(m["match_id"])
    except:
        pass
    # Fallback to legacy hash if match_id isn't found
    import hashlib
    raw_str = f"{phase}_{category}_{team_a.strip().lower()}_{team_b.strip().lower()}"
    return hashlib.md5(raw_str.encode('utf-8')).hexdigest()

# Add the 'match_id' to your real data dictionary matching matches.py perfectly:
REAL_WORLD_CUP_DATA = {
    "Group Stage": {
        "Group A": [
            {"team_a": "Mexico", "flag_a": "🇲🇽", "team_b": "South Africa", "flag_b": "🇿🇦", "score": "2:00AM", "status": "Scheduled", "date": "12 June"},
            {"team_a": "Korea Republic", "flag_a": "🇰🇷", "team_b": "Czechia", "flag_b": "🇨🇿", "score": "9:00AM", "status": "Scheduled", "date": "12 June"},
            {"team_a": "Czechia", "flag_a": "🇨🇿", "team_b": "South Africa", "flag_b": "🇿🇦", "score": "11:00PM", "status": "Scheduled", "date": "18 June"},
            {"team_a": "Mexico", "flag_a": "🇲🇽", "team_b": "Korea Republic", "flag_b": "🇰🇷", "score": "8:00AM", "status": "Scheduled", "date": "19 June"},
            {"team_a": "Czechia", "flag_a": "🇨🇿", "team_b": "Mexico", "flag_b": "🇲🇽", "score": "8:00AM", "status": "Scheduled", "date": "25 June"},
            {"team_a": "South Africa", "flag_a": "🇿🇦", "team_b": "Korea Republic", "flag_b": "🇰🇷", "score": "8:00AM", "status": "Scheduled", "date": "25 June"}
        ],
        "Group B": [
            {"team_a": "Canada", "flag_a": "🇨🇦", "team_b": "Bosnia and Herzegovina", "flag_b": "🇧🇦", "score": "2:00AM", "status": "Scheduled", "date": "13 June"},
            {"team_a": "Qatar", "flag_a": "🇶🇦", "team_b": "Switzerland", "flag_b": "🇨🇭", "score": "2:00AM", "status": "Scheduled", "date": "14 June"},
            {"team_a": "Switzerland", "flag_a": "🇨🇭", "team_b": "Bosnia and Herzegovina", "flag_b": "🇧🇦", "score": "2:00AM", "status": "Scheduled", "date": "19 June"},
            {"team_a": "Canada", "flag_a": "🇨🇦", "team_b": "Qatar", "flag_b": "🇶🇦", "score": "5:00AM", "status": "Scheduled", "date": "19 June"},
            {"team_a": "Bosnia and Herzegovina", "flag_a": "🇧🇦", "team_b": "Qatar", "flag_b": "🇶🇦", "score": "2:00AM", "status": "Scheduled", "date": "25 June"},
            {"team_a": "Switzerland", "flag_a": "🇨🇭", "team_b": "Canada", "flag_b": "🇨🇦", "score": "2:00AM", "status": "Scheduled", "date": "25 June"}
        ],
        "Group C": [
            {"team_a": "Brazil", "flag_a": "🇧🇷", "team_b": "Morocco", "flag_b": "🇲🇦", "score": "5:00AM", "status": "Scheduled", "date": "14 June"},
            {"team_a": "Haiti", "flag_a": "🇭🇹", "team_b": "Scotland", "flag_b": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "score": "8:00AM", "status": "Scheduled", "date": "14 June"},
            {"team_a": "Scotland", "flag_a": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "team_b": "Morocco", "flag_b": "🇲🇦", "score": "5:00AM", "status": "Scheduled", "date": "20 June"},
            {"team_a": "Brazil", "flag_a": "🇧🇷", "team_b": "Haiti", "flag_b": "🇭🇹", "score": "7:30AM", "status": "Scheduled", "date": "20 June"},
            {"team_a": "Morocco", "flag_a": "🇲🇦", "team_b": "Haiti", "flag_b": "🇭🇹", "score": "5:00AM", "status": "Scheduled", "date": "25 June"},
            {"team_a": "Scotland", "flag_a": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "team_b": "Brazil", "flag_b": "🇧🇷", "score": "5:00AM", "status": "Scheduled", "date": "25 June"}
        ],
        "Group D": [
            {"team_a": "USA", "flag_a": "🇺🇸", "team_b": "Paraguay", "flag_b": "🇵🇾", "score": "9:00AM", "status": "Scheduled", "date": "13 June"},
            {"team_a": "Australia", "flag_a": "🇦🇺", "team_b": "Turkiye", "flag_b": "🇹🇷", "score": "11:00AM", "status": "Scheduled", "date": "14 June"},
            {"team_a": "USA", "flag_a": "🇺🇸", "team_b": "Australia", "flag_b": "🇦🇺", "score": "2:00AM", "status": "Scheduled", "date": "20 June"},
            {"team_a": "Turkiye", "flag_a": "🇹🇷", "team_b": "Paraguay", "flag_b": "🇵🇾", "score": "10:00AM", "status": "Scheduled", "date": "20 June"},
            {"team_a": "Paraguay", "flag_a": "🇵🇾", "team_b": "Australia", "flag_b": "🇦🇺", "score": "9:00AM", "status": "Scheduled", "date": "26 June"},
            {"team_a": "Turkiye", "flag_a": "🇹🇷", "team_b": "USA", "flag_b": "🇺🇸", "score": "9:00AM", "status": "Scheduled", "date": "26 June"}
        ],
        "Group E": [
            {"team_a": "Germany", "flag_a": "🇩🇪", "team_b": "Curacao", "flag_b": "🇨🇼", "score": "12:00AM", "status": "Scheduled", "date": "15 June"},
            {"team_a": "Ivory Coast", "flag_a": "🇨🇮", "team_b": "Ecuador", "flag_b": "🇪🇨", "score": "6:00AM", "status": "Scheduled", "date": "15 June"},
            {"team_a": "Germany", "flag_a": "🇩🇪", "team_b": "Ivory Coast", "flag_b": "🇨🇮", "score": "3:00AM", "status": "Scheduled", "date": "21 June"},
            {"team_a": "Ecuador", "flag_a": "🇪🇨", "team_b": "Curacao", "flag_b": "🇨🇼", "score": "7:00AM", "status": "Scheduled", "date": "21 June"},
            {"team_a": "Curacao", "flag_a": "🇨🇼", "team_b": "Ivory Coast", "flag_b": "🇨🇮", "score": "3:00AM", "status": "Scheduled", "date": "26 June"},
            {"team_a": "Ecuador", "flag_a": "🇪🇨", "team_b": "Germany", "flag_b": "🇩🇪", "score": "3:00AM", "status": "Scheduled", "date": "26 June"}
        ],
        "Group F": [
            {"team_a": "Netherlands", "flag_a": "🇳🇱", "team_b": "Japan", "flag_b": "🇯🇵", "score": "3:00AM", "status": "Scheduled", "date": "15 June"},
            {"team_a": "Sweden", "flag_a": "🇸🇪", "team_b": "Tunisia", "flag_b": "🇹🇳", "score": "9:00AM", "status": "Scheduled", "date": "15 June"},
            {"team_a": "Netherlands", "flag_a": "🇳🇱", "team_b": "Sweden", "flag_b": "🇸🇪", "score": "12:00AM", "status": "Scheduled", "date": "21 June"},
            {"team_a": "Tunisia", "flag_a": "🇹🇳", "team_b": "Japan", "flag_b": "🇯🇵", "score": "11:00AM", "status": "Scheduled", "date": "21 June"},
            {"team_a": "Japan", "flag_a": "🇯🇵", "team_b": "Sweden", "flag_b": "🇸🇪", "score": "6:00AM", "status": "Scheduled", "date": "26 June"},
            {"team_a": "Tunisia", "flag_a": "🇹🇳", "team_b": "Netherlands", "flag_b": "🇳🇱", "score": "6:00AM", "status": "Scheduled", "date": "26 June"}
        ],
        "Group G": [
            {"team_a": "Belgium", "flag_a": "🇧🇪", "team_b": "Egypt", "flag_b": "🇪🇬", "score": "2:00AM", "status": "Scheduled", "date": "16 June"},
            {"team_a": "Iran", "flag_a": "🇮🇷", "team_b": "New Zealand", "flag_b": "🇳🇿", "score": "8:00AM", "status": "Scheduled", "date": "16 June"},
            {"team_a": "Belgium", "flag_a": "🇧🇪", "team_b": "Iran", "flag_b": "🇮🇷", "score": "2:00AM", "status": "Scheduled", "date": "22 June"},
            {"team_a": "New Zealand", "flag_a": "🇳🇿", "team_b": "Egypt", "flag_b": "🇪🇬", "score": "8:00AM", "status": "Scheduled", "date": "22 June"},
            {"team_a": "Egypt", "flag_a": "🇪🇬", "team_b": "Iran", "flag_b": "🇮🇷", "score": "10:00AM", "status": "Scheduled", "date": "27 June"},
            {"team_a": "New Zealand", "flag_a": "🇳🇿", "team_b": "Belgium", "flag_b": "🇧🇪", "score": "10:00AM", "status": "Scheduled", "date": "27 June"}
        ],
        "Group H": [
            {"team_a": "Spain", "flag_a": "🇪🇸", "team_b": "Cabo Verde", "flag_b": "🇨🇻", "score": "11:00PM", "status": "Scheduled", "date": "15 June"},
            {"team_a": "Saudi Arabia", "flag_a": "🇸🇦", "team_b": "Uruguay", "flag_b": "🇺🇾", "score": "5:00AM", "status": "Scheduled", "date": "16 June"},
            {"team_a": "Spain", "flag_a": "🇪🇸", "team_b": "Saudi Arabia", "flag_b": "🇸🇦", "score": "11:00PM", "status": "Scheduled", "date": "21 June"},
            {"team_a": "Uruguay", "flag_a": "🇺🇾", "team_b": "Cabo Verde", "flag_b": "🇨🇻", "score": "5:00AM", "status": "Scheduled", "date": "22 June"},
            {"team_a": "Cabo Verde", "flag_a": "🇨🇻", "team_b": "Saudi Arabia", "flag_b": "🇸🇦", "score": "7:00AM", "status": "Scheduled", "date": "27 June"},
            {"team_a": "Uruguay", "flag_a": "🇺🇾", "team_b": "Spain", "flag_b": "🇪🇸", "score": "7:00AM", "status": "Scheduled", "date": "27 June"}
        ],
        "Group I": [
            {"team_a": "France", "flag_a": "🇫🇷", "team_b": "Senegal", "flag_b": "🇸🇳", "score": "2:00AM", "status": "Scheduled", "date": "17 June"},
            {"team_a": "Iraq", "flag_a": "🇮🇶", "team_b": "Norway", "flag_b": "🇳🇴", "score": "5:00AM", "status": "Scheduled", "date": "17 June"},
            {"team_a": "France", "flag_a": "🇫🇷", "team_b": "Iraq", "flag_b": "🇮🇶", "score": "4:00AM", "status": "Scheduled", "date": "23 June"},
            {"team_a": "Norway", "flag_a": "🇳🇴", "team_b": "Senegal", "flag_b": "🇸🇳", "score": "7:00AM", "status": "Scheduled", "date": "23 June"},
            {"team_a": "Norway", "flag_a": "🇳🇴", "team_b": "France", "flag_b": "🇫🇷", "score": "2:00AM", "status": "Scheduled", "date": "27 June"},
            {"team_a": "Senegal", "flag_a": "🇸🇳", "team_b": "Iraq", "flag_b": "🇮🇶", "score": "2:00AM", "status": "Scheduled", "date": "27 June"}
        ],
        "Group J": [
            {"team_a": "Argentina", "flag_a": "🇦🇷", "team_b": "Algeria", "flag_b": "🇩🇿", "score": "8:00AM", "status": "Scheduled", "date": "17 June"},
            {"team_a": "Austria", "flag_a": "🇦🇹", "team_b": "Jordan", "flag_b": "🇯🇴", "score": "11:00AM", "status": "Scheduled", "date": "17 June"},
            {"team_a": "Argentina", "flag_a": "🇦🇷", "team_b": "Austria", "flag_b": "🇦🇹", "score": "12:00AM", "status": "Scheduled", "date": "23 June"},
            {"team_a": "Jordan", "flag_a": "🇯🇴", "team_b": "Algeria", "flag_b": "🇩🇿", "score": "10:00AM", "status": "Scheduled", "date": "23 June"},
            {"team_a": "Algeria", "flag_a": "🇩🇿", "team_b": "Austria", "flag_b": "🇦🇹", "score": "9:00AM", "status": "Scheduled", "date": "27 June"},
            {"team_a": "Jordan", "flag_a": "🇯🇴", "team_b": "Argentina", "flag_b": "🇦🇷", "score": "9:00AM", "status": "Scheduled", "date": "27 June"}
        ],
        "Group K": [
            {"team_a": "Portugal", "flag_a": "🇵🇹", "team_b": "Congo DR", "flag_b": "🇨🇩", "score": "12:00AM", "status": "Scheduled", "date": "18 June"},
            {"team_a": "Uzbekistan", "flag_a": "🇺🇿", "team_b": "Colombia", "flag_b": "🇨🇴", "score": "9:00AM", "status": "Scheduled", "date": "18 June"},
            {"team_a": "Portugal", "flag_a": "🇵🇹", "team_b": "Uzbekistan", "flag_b": "🇺🇿", "score": "12:00AM", "status": "Scheduled", "date": "24 June"},
            {"team_a": "Colombia", "flag_a": "🇨🇴", "team_b": "Congo DR", "flag_b": "🇨🇩", "score": "9:00AM", "status": "Scheduled", "date": "24 June"},
            {"team_a": "Colombia", "flag_a": "🇨🇴", "team_b": "Portugal", "flag_b": "🇵🇹", "score": "6:30AM", "status": "Scheduled", "date": "28 June"},
            {"team_a": "Congo DR", "flag_a": "🇨🇩", "team_b": "Uzbekistan", "flag_b": "🇺🇿", "score": "6:30AM", "status": "Scheduled", "date": "28 June"}
        ],
        "Group L": [
            {"team_a": "England", "flag_a": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "team_b": "Croatia", "flag_b": "🇭🇷", "score": "3:00AM", "status": "Scheduled", "date": "18 June"},
            {"team_a": "Ghana", "flag_a": "🇬🇭", "team_b": "Panama", "flag_b": "🇵🇦", "score": "6:00AM", "status": "Scheduled", "date": "18 June"},
            {"team_a": "England", "flag_a": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "team_b": "Ghana", "flag_b": "🇬🇭", "score": "3:00AM", "status": "Scheduled", "date": "24 June"},
            {"team_a": "Panama", "flag_a": "🇵🇦", "team_b": "Croatia", "flag_b": "🇭🇷", "score": "6:00AM", "status": "Scheduled", "date": "24 June"},
            {"team_a": "Croatia", "flag_a": "🇭🇷", "team_b": "Ghana", "flag_b": "🇬🇭", "score": "4:00AM", "status": "Scheduled", "date": "28 June"},
            {"team_a": "Panama", "flag_a": "🇵🇦", "team_b": "England", "flag_b": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "score": "4:00AM", "status": "Scheduled", "date": "28 June"}
        ]
    },
    "Knockout Stage": {
        "Round of 32": [
            {"team_a": "Runner-up Group A", "flag_a": "🏳️", "team_b": "Runner-up Group B", "flag_b": "🏳️", "score": "2:00AM", "status": "Scheduled", "date": "29 June"},
            {"team_a": "Winner Group C", "flag_a": "🏳️", "team_b": "Runner-up Group F", "flag_b": "🏳️", "score": "12:00AM", "status": "Scheduled", "date": "30 June"},
            {"team_a": "Winner Group E", "flag_a": "🏳️", "team_b": "3rd Group A/B/C/D/F", "flag_b": "🏳️", "score": "3:30AM", "status": "Scheduled", "date": "30 June"},
            {"team_a": "Winner Group F", "flag_a": "🏳️", "team_b": "Runner-up Group C", "flag_b": "🏳️", "score": "8:00AM", "status": "Scheduled", "date": "30 June"},
            {"team_a": "Runner-up Group E", "flag_a": "🏳️", "team_b": "Runner-up Group I", "flag_b": "🏳️", "score": "12:00AM", "status": "Scheduled", "date": "1 July"},
            {"team_a": "Winner Group I", "flag_a": "🏳️", "team_b": "3rd Group C/D/F/G/H", "flag_b": "🏳️", "score": "4:00AM", "status": "Scheduled", "date": "1 July"},
            {"team_a": "Winner Group A", "flag_a": "🏳️", "team_b": "3rd Group C/E/F/H/I", "flag_b": "🏳️", "score": "8:00AM", "status": "Scheduled", "date": "1 July"},
            {"team_a": "Winner Group L", "flag_a": "🏳️", "team_b": "3rd Group E/H/I/J/K", "flag_b": "🏳️", "score": "11:00PM", "status": "Scheduled", "date": "1 July"},
            {"team_a": "Winner Group G", "flag_a": "🏳️", "team_b": "3rd Group A/E/H/I/J", "flag_b": "🏳️", "score": "3:00AM", "status": "Scheduled", "date": "2 July"},
            {"team_a": "Winner Group D", "flag_a": "🏳️", "team_b": "3rd Group B/E/F/I/J", "flag_b": "🏳️", "score": "7:00AM", "status": "Scheduled", "date": "2 July"},
            {"team_a": "Winner Group H", "flag_a": "🏳️", "team_b": "Runner-up Group J", "flag_b": "🏳️", "score": "2:00AM", "status": "Scheduled", "date": "3 July"},
            {"team_a": "Runner-up Group K", "flag_a": "🏳️", "team_b": "Runner-up Group L", "flag_b": "🏳️", "score": "6:00AM", "status": "Scheduled", "date": "3 July"},
            {"team_a": "Winner Group B", "flag_a": "🏳️", "team_b": "3rd Group E/F/G/I/J", "flag_b": "🏳️", "score": "10:00AM", "status": "Scheduled", "date": "3 July"},
            {"team_a": "Runner-up Group D", "flag_a": "🏳️", "team_b": "Runner-up Group G", "flag_b": "🏳️", "score": "1:00AM", "status": "Scheduled", "date": "4 July"},
            {"team_a": "Winner Group J", "flag_a": "🏳️", "team_b": "Runner-up Group H", "flag_b": "🏳️", "score": "5:00AM", "status": "Scheduled", "date": "4 July"},
            {"team_a": "Winner Group K", "flag_a": "🏳️", "team_b": "3rd Group D/E/I/J/L", "flag_b": "🏳️", "score": "8:30AM", "status": "Scheduled", "date": "4 July"}
        ],
        "Round of 16": [
            {"team_a": "Winner R32 Match 1", "flag_a": "🏳️", "team_b": "Winner R32 Match 4", "flag_b": "🏳️", "score": "12:00AM", "status": "Scheduled", "date": "5 July"},
            {"team_a": "Winner R32 Match 3", "flag_a": "🏳️", "team_b": "Winner R32 Match 6", "flag_b": "🏳️", "score": "4:00AM", "status": "Scheduled", "date": "5 July"},
            {"team_a": "Winner R32 Match 2", "flag_a": "🏳️", "team_b": "Winner R32 Match 5", "flag_b": "🏳️", "score": "3:00AM", "status": "Scheduled", "date": "6 July"},
            {"team_a": "Winner R32 Match 7", "flag_a": "🏳️", "team_b": "Winner R32 Match 8", "flag_b": "🏳️", "score": "7:00AM", "status": "Scheduled", "date": "6 July"},
            {"team_a": "Winner R32 Match 12", "flag_a": "🏳️", "team_b": "Winner R32 Match 11", "flag_b": "🏳️", "score": "2:00AM", "status": "Scheduled", "date": "7 July"},
            {"team_a": "Winner R32 Match 10", "flag_a": "🏳️", "team_b": "Winner R32 Match 9", "flag_b": "🏳️", "score": "7:00AM", "status": "Scheduled", "date": "7 July"},
            {"team_a": "Winner R32 Match 15", "flag_a": "🏳️", "team_b": "Winner R32 Match 14", "flag_b": "🏳️", "score": "11:00PM", "status": "Scheduled", "date": "7 July"},
            {"team_a": "Winner R32 Match 13", "flag_a": "🏳️", "team_b": "Winner R32 Match 16", "flag_b": "🏳️", "score": "3:00AM", "status": "Scheduled", "date": "8 July"}
        ],
        "Quarterfinals": [
            {"team_a": "Winner R16 Match 1", "flag_a": "🏳️", "team_b": "Winner R16 Match 2", "flag_b": "🏳️", "score": "3:00AM", "status": "Scheduled", "date": "10 July"},
            {"team_a": "Winner R16 Match 5", "flag_a": "🏳️", "team_b": "Winner R16 Match 6", "flag_b": "🏳️", "score": "2:00AM", "status": "Scheduled", "date": "11 July"},
            {"team_a": "Winner R16 Match 3", "flag_a": "🏳️", "team_b": "Winner R16 Match 4", "flag_b": "🏳️", "score": "4:00AM", "status": "Scheduled", "date": "12 July"},
            {"team_a": "Winner R16 Match 7", "flag_a": "🏳️", "team_b": "Winner R16 Match 8", "flag_b": "🏳️", "score": "8:00AM", "status": "Scheduled", "date": "12 July"}
        ],
        "Semifinals": [
            {"team_a": "Winner QF Match 1", "flag_a": "🏳️", "team_b": "Winner QF Match 2", "flag_b": "🏳️", "score": "2:00AM", "status": "Scheduled", "date": "15 July"},
            {"team_a": "Winner QF Match 3", "flag_a": "🏳️", "team_b": "Winner QF Match 4", "flag_b": "🏳️", "score": "2:00AM", "status": "Scheduled", "date": "16 July"}
        ],
        "3rd Place Match": [
            {"team_a": "Loser SF Match 1", "flag_a": "🏳️", "team_b": "Loser SF Match 2", "flag_b": "🏳️", "score": "4:00AM", "status": "Scheduled", "date": "19 July"}
        ],
        "Final": [
            {"team_a": "Winner SF Match 1", "flag_a": "🏳️", "team_b": "Winner SF Match 2", "flag_b": "🏳️", "score": "2:00AM", "status": "Scheduled", "date": "20 July"}
        ]
    }
}

def render_real_results_page():
    st.title("⚽ Real-World World Cup 2026 Results")
    st.caption("Official real-time scores and tournament stage tracking.")
    st.divider()

    live_overrides = load_live_admin_results()

    main_phases = list(REAL_WORLD_CUP_DATA.keys())
    main_tabs = st.tabs(main_phases)

    for m_idx, phase_name in enumerate(main_phases):
        with main_tabs[m_idx]:
            sub_categories = list(REAL_WORLD_CUP_DATA[phase_name].keys())
            if not sub_categories:
                st.info("No data available.")
                continue
                
            sub_tabs = st.tabs(sub_categories)
            for s_idx, sub_name in enumerate(sub_categories):
                with sub_tabs[s_idx]:
                    st.subheader(f"📊 {sub_name} Scores")
                    st.write("") 
                    
                    match_list = REAL_WORLD_CUP_DATA[phase_name][sub_name]
                    for match in match_list:
                        # Hash lookup key generated here
                        match_uid = get_match_uid(phase_name, sub_name, match['team_a'], match['team_b'])
                        
                        display_score = match['score']
                        display_status = match['status']
                        
                        if match_uid in live_overrides:
                            display_score = live_overrides[match_uid]["score"]
                            display_status = live_overrides[match_uid]["status"]

                        with st.container():
                            col1, col2, col3 = st.columns([3, 2, 3])
                            
                            with col1:
                                st.markdown(f"<div style='text-align: right; font-size: 18px; font-weight: bold; padding-top: 5px;'>{match['flag_a']} {match['team_a']}</div>", unsafe_allow_html=True)
                                
                            with col2:
                                if display_status == "Finished":
                                    st.markdown(f"<div style='text-align: center; background-color: #1e3d2f; color: #4ade80; font-size: 18px; font-weight: bold; border-radius: 8px; padding: 5px 0px;'>{display_score}</div>", unsafe_allow_html=True)
                                elif display_status == "Live":
                                    st.markdown(f"<div style='text-align: center; background-color: #3d1e1e; color: #f87171; font-size: 18px; font-weight: bold; border-radius: 8px; padding: 5px 0px;'>{display_score}</div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<div style='text-align: center; background-color: #262730; color: #e0e0e0; font-size: 15px; font-weight: bold; border-radius: 8px; padding: 5px 0px; border: 1px solid #444;'>{display_score}</div>", unsafe_allow_html=True)
                                    
                                st.markdown(f"<div style='text-align: center; color: #aaa; font-size: 13px; margin-top: 5px; font-style: italic;'>{match['date']}</div>", unsafe_allow_html=True)
                                
                            with col3:
                                status_suffix = ""
                                if display_status == "Finished":
                                    status_suffix = " <span style='color: #888888; font-size: 12px; font-weight: normal; margin-left: 8px;'>🏁 FT</span>"
                                elif display_status == "Live":
                                    status_suffix = " <span style='color: #ff4b4b; font-size: 12px; font-weight: bold; margin-left: 8px;'>🔴 LIVE</span>"
                                    
                                st.markdown(f"<div style='text-align: left; font-size: 18px; font-weight: bold; padding-top: 5px;'>{match['flag_b']} {match['team_b']}{status_suffix}</div>", unsafe_allow_html=True)
                                
                        st.write("") 
                        st.markdown("<hr style='margin: 10px 0px; border-color: #333;' />", unsafe_allow_html=True)
