import streamlit as st
import pandas as pd
import pickle
st.title('IPL Dashboard')



def load_player_details(player):
    st.subheader(player)


def imp_info_of_batsman(player_name):
                   ####### #FOR 100s#######
    df9 = df[df['striker'] == player_name]
    df9 = df9.groupby('match_id')['runs_off_bat'].sum().reset_index().rename(columns={'runs_off_bat': '100S'})
    match_id_to_venue_map = df[['venue', 'match_id']].drop_duplicates(keep='first')
    df9.insert(0, 'VENUE', df9['match_id'].map(match_id_to_venue_map.set_index('match_id')['venue']))

    # Drop the original 'match_id' column if you don't need it anymore
    df9.drop(columns=['match_id'], inplace=True)
    df9[(df9['100S'] >= 100) & (df9['100S'] < 200)].value_counts('VENUE')

    if df9[(df9['100S'] >= 100) & (df9['100S'] < 200)].value_counts('VENUE').empty:
        st.markdown("- <span style='color:red; font-weight:bold;'>NO 100s</span>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"- <span style='color:blue'>STADIUM WISE CENTURY RECORDS OF {player_name}  ", unsafe_allow_html=True)
        df10 = df9[(df9['100S'] >= 100) & (df9['100S'] < 200)].value_counts('VENUE').reset_index()
        df10.rename(columns={'count': 'NUMBER OF 100s'}, inplace=True)

        def highlight_rows(row):
            background_color = 'green' if row['NUMBER OF 100s'] >= 3 else 'yellow'
            return ['background-color: {}'.format(background_color)] * len(row)

        st.dataframe(df10.style.apply(highlight_rows, axis=1))
########### FOR 50s ###########
    df11 = df[df['striker'] == player_name]
    df11 = df11.groupby('match_id')['runs_off_bat'].sum().reset_index().rename(columns={'runs_off_bat': '50S'})
    match_id_to_venue_map = df[['venue', 'match_id']].drop_duplicates(keep='first')
    df11.insert(0, 'VENUE', df11['match_id'].map(match_id_to_venue_map.set_index('match_id')['venue']))

    # Drop the original 'match_id' column if you don't need it anymore
    df11.drop(columns=['match_id'], inplace=True)
    df11[(df11['50S'] >= 50) & (df11['50S'] < 100)].value_counts('VENUE')

    if df11[(df11['50S'] >= 50) & (df11['50S'] < 100)].value_counts('VENUE').empty:
        st.markdown("- <span style='color:red; font-weight:bold;'>NO 50s</span>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"- <span style='color:blue'>STADIUM WISE HALF CENTURY RECORDS OF {player_name}  ", unsafe_allow_html=True)
        df12 = df11[(df11['50S'] >= 50) & (df11['50S'] < 100)].value_counts('VENUE').reset_index()
        df12.rename(columns={'count': 'NUMBER OF 50s'}, inplace=True)

        def highlight_rows(row):
            background_color = 'green' if row['NUMBER OF 50s'] >= 10 else 'yellow'
            return ['background-color: {}'.format(background_color)] * len(row)

        st.dataframe(df12.style.apply(highlight_rows, axis=1))
# FOR ORANGE CAP HOLDER
    filtered_df = orange_cap_holders_df[orange_cap_holders_df['striker'] == player_name]

    if not filtered_df.empty:
        st.markdown(
            f"- <span style='color:orange; font-weight:bold;'>Orange cap holder details of {player_name}</span>",
            unsafe_allow_html=True
        )
#

        def highlight_player(row):
            if row['striker'] == player_name:
                return ['background-color: orange'] * len(row)
            else:
                return [''] * len(row)

        styled_df = filtered_df.style.apply(highlight_player, axis=1)
        st.dataframe(styled_df)
# Standard Deviation (SD):
# Standard deviation is a measure of the amount of variation or dispersion in a set of values.
# In the context of cricket, it measures how much the batsman's scores deviate from their average score.
# A lower standard deviation suggests more consistent performance, as the scores are closer to the average
    total_inns = df[df.striker == player_name].groupby('match_id').count().shape[0]
    avg = df[df.striker == player_name].runs_off_bat.sum() / total_inns
    inns_df = df[df.striker == player_name].groupby('match_id').count()
    SD = round((sum((x - avg) ** 2 for x in inns_df['runs_off_bat']) / total_inns) ** 0.5, 2)
    CV = (SD / avg) * 100
    CI = round(inns_df[inns_df.runs_off_bat >= avg].shape[0] / total_inns, 2)

    st.write("")
    st.write("")
    st.markdown(
        f"- <span style='color:green; font-weight:bold;'>{player_name} best 5 records against bowlers </span>",
        unsafe_allow_html=True)
    df20 = df[df.striker == player_name].groupby('bowler')[['runs_off_bat', 'legal_balls', 'wickets']].sum()
    df20['legal_balls'] = df20['legal_balls'].astype(int)
    df21 = df20.sort_values(['runs_off_bat', 'legal_balls', 'wickets'], ascending=[False, True, True])
    df21["SR"] = round(df21.runs_off_bat / df21.legal_balls * 100, 2)
    df22 = df21.rename(
        columns={'runs_off_bat': 'Total Runs', 'legal_balls': ' Balls Played', 'wickets': ' Dismissals'}).head(5)
    background_color = 'yellow'

    # Function to apply background color to the DataFrame cells
    def apply_background_color(row):
        return [f'background-color: {background_color}' for _ in row]

    # Apply styling to the DataFrame
    styled_df = df22.style.apply(apply_background_color, axis=1)

    # Convert Styler object to HTML
    styled_html = styled_df.to_html(classes=['styled-table'], escape=False, index=False)

    # Display the DataFrame with the background color applied
    st.markdown(styled_html, unsafe_allow_html=True)

    st.write("")
    st.write("")

    def set_light_blue(text):
        return f"<span style='color:lightblue'>{text}</span>"

    if (SD <= 18.77 or CV <= 57.73 or CI >= 0.31) and (avg >= 30):
        st.markdown(
            f"- <span style='color:green;'>Based on Standard Deviation, Coefficient of Variation, Consistency Index"
            f" <b>{player_name}</b> is a "
            f" <b>consistent player</b></span>",
            unsafe_allow_html=True
        )

def imp_info_of_bowler(player_name):
    # PURPLE CAP HOLDERS
    light_purple_hex = '#D3B8FF'
    pcap_df = df.groupby(['season', 'bowler'])[['wickets', 'runs_for_eco', 'legal_balls']].sum().sort_values(
        ['season', 'wickets'], ascending=False)
    pcap_df['economy'] = (pcap_df['runs_for_eco'] / pcap_df['legal_balls']) * 6
    pcap_df['avg'] = round(pcap_df['runs_for_eco'] / pcap_df['wickets'], 2)

    new_pcap_df = pcap_df[['wickets', 'economy', 'avg']].sort_values(['wickets', 'economy', 'avg'],
                                                                     ascending=[False, False, False]).reset_index()
    pcap_holder_df = new_pcap_df.drop_duplicates('season', keep='first')
    filtered_pcap_df = pcap_holder_df[pcap_holder_df.bowler == player_name]
    filtered_pcap_df.set_index('season', inplace=True)
    if not filtered_pcap_df.empty:
        st.markdown(
            f"- <span style='color:purple; font-weight:bold;'>Pcap cap holder details of {player_name}</span>",
            unsafe_allow_html=True
        )

        def highlight_player(row):
            if row['bowler'] == player_name:
                return ['background-color:purple'] * len(row)
            else:
                return [''] * len(row)

        styled_df = filtered_pcap_df.style.apply(highlight_player, axis=1)
        st.dataframe(styled_df)
    st.markdown(
        f"- <span style='color:green; font-weight:bold;'>Stadium wise at least 3 wickets taken by {player_name}</span>",
        unsafe_allow_html=True)
    wickets_df = df[df.bowler == player_name].groupby(['start_date', 'venue'])['wickets'].sum().reset_index()
    wickets_df.rename(columns={'venue': 'VENUE', 'wickets': 'No. of times'}, inplace=True)
    df17 = wickets_df[wickets_df['No. of times'] >= 3].groupby('VENUE').size().reset_index(name='No. of times').sort_values('No. of times', ascending=False).set_index('VENUE')
    background_color = 'lightblue'

    # Function to apply background color to the DataFrame cells
    def apply_background_color(row):
        return [f'background-color: {background_color}' for _ in row]

    # Apply styling to the DataFrame
    styled_df = df17.style.apply(apply_background_color, axis=1)

    # Convert Styler object to HTML
    styled_html = styled_df.to_html(classes=['styled-table'], escape=False, index=False)

    # Display the DataFrame with the background color applied
    st.markdown(styled_html, unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.markdown(
        f"- <span style='color:green; font-weight:bold;'>{player_name} best 5 records against batsman </span>",
        unsafe_allow_html=True)
    df15 = df[df.bowler == player_name].groupby('striker')[['runs_off_bat', 'legal_balls', 'wickets']].sum()
    df15['SR'] = round(df15['runs_off_bat'] / df15['legal_balls'] * 100, 2)
    df15['WKT_PER_BALLs'] = round(df15['legal_balls'] / df15['wickets'])
    df15.rename(columns={'legal_balls': 'Balls_Played', 'wickets': 'Wicket_Times'}, inplace=True)
    df16 = df15.sort_values(['Wicket_Times', 'SR', 'WKT_PER_BALLs'], ascending=[False, True, True]).head(5)
    background_color = 'yellow'

    # Function to apply background color to the DataFrame cells
    def apply_background_color(row):
        return [f'background-color: {background_color}' for _ in row]

    # Apply styling to the DataFrame
    styled_df = df16.style.apply(apply_background_color, axis=1)

    # Convert Styler object to HTML
    styled_html = styled_df.to_html(classes=['styled-table'], escape=False, index=False)

    # Display the DataFrame with the background color applied
    st.markdown(styled_html, unsafe_allow_html=True)

# BOWLER CLASS -- bowler_obj


class Bowler(Exception):
    def __init__(self, bowler):
        self.player = bowler
        self.show_information = False

    def bowler_details(self):
        col1, col2, col3 = st.columns(3, gap='large')
        balls_delivered = df[df.bowler == self.player].legal_balls.sum()
        total_wickets = df[df.bowler == self.player].wickets.sum()
        with col1:
            st.markdown(
                f"- <span style='color:blue'>Balls Delivered:</span> <span style='color:green'> "
                f"{balls_delivered}</span>",
                unsafe_allow_html=True)
        df1 = df[df.bowler == self.player].groupby('bowler')[['runs_off_bat', 'wides', 'noballs']].sum()
        try:
            runs_of_bowler = int((df1.runs_off_bat + df1.wides + df1.noballs).loc[self.player])
        except IndexError:
            runs_of_bowler = 0
        with col2:
            st.markdown(
                f"- <span style='color:blue'>Total runs given by {self.player}:</span> <span style='color:green'>"
                f" {runs_of_bowler}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Total wickets taken by {self.player}:</span> <span style='color:green'>"
                f" {total_wickets}</span>",
                unsafe_allow_html=True)
        try:
            total_no_balls = int(df1.noballs.loc[self.player])
            total_wides = int(df1.wides.loc[self.player])
        except IndexError:
            total_no_balls = 0
            total_wides = 0
        total_fair_deliveries = int(balls_delivered)
        with col3:
            st.markdown(
                f"- <span style='color:blue'>Total No balls:</span> <span style='color:green'> {total_no_balls}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Total Wides: </span> <span style='color:green'> {total_wides}</span>",
                unsafe_allow_html=True)
        with col1:
            st.markdown(
                f"- <span style='color:blue'>Overall economy of {self.player} :</span> <span style='color:green'> {round(runs_of_bowler / total_fair_deliveries * 6, 2)}</span>",
                unsafe_allow_html=True)

        st.divider()


class Batsman(Exception):
    def __init__(self, batsman):
        self.player = batsman

    def batsman_details(self):
        col1, col2, col3 = st.columns(3, gap='large')
        balls_played = df[(df.striker == self.player) & ((df['noballs'].isna()) & (df['wides'].isna()))].shape[0]
        runs = df[df.striker == self.player].groupby('striker')['runs_off_bat'].sum().loc[self.player]
        df9 = df[df.striker == self.player].groupby('start_date')[['runs_off_bat']].sum().sort_values('runs_off_bat', ascending = False)
        total_50s = df9[(df9.runs_off_bat >= 50) & (df9.runs_off_bat < 100)].count().loc['runs_off_bat']
        total_100s = df9[(df9.runs_off_bat >= 100) & (df9.runs_off_bat < 200)].count().loc['runs_off_bat']
        df18 = df[df.striker == self.player]
        df19 = df18.groupby(['match_id', 'venue'])['runs_off_bat'].sum().sort_values(
            ascending=False).reset_index().head(1)
        try:
            total_fours = df[(df.striker == self.player) & (df.runs_off_bat == 4)].runs_off_bat.value_counts().iloc[0]
        except IndexError:
            total_fours = 0
        try:
            total_sixes = df[(df.striker == self.player) & (df.runs_off_bat == 6)].runs_off_bat.value_counts().iloc[0]
        except IndexError:
            total_sixes = 0
        with col1:
            st.markdown(
                f"- <span style='color:blue'>Balls Played:</span> <span style='color:green; font-weight:bold'> "
                f"{balls_played}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Total runs made by {self.player} is "
                f":</span> <span style='color:green ; font-weight:bold'> {runs}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Overall strike rate of {self.player} is "
                f":</span> <span style='color:green; font-weight:bold'> {round(runs / balls_played * 100, 2)}</span>",
                unsafe_allow_html=True)

        with col2:
            st.markdown(
                f"- <span style='color:blue'>Total number of 4s :</span> <span style='color:green ; font-weight:bold'> "
                f"{total_fours}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Total number of 6s :</span> <span style='color:green ; font-weight:bold'> "
                f"{total_sixes}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Total number of 50s :</span> <span style='color:green ; font-weight:bold'> "
                f"{total_50s}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Total number of 100s :</span> <span style='color:green ; font-weight:bold'> "
                f"{total_100s}</span>",
                unsafe_allow_html=True)
        st.markdown(
            f"- <span style='color:blue'>Highest Score of {self.player} is "
            f"</span> <span style='color:red; font-weight:bold'> {df19['runs_off_bat'].loc[0]} </span> at"
            f"</span> <span style='color:blue; font-weight:bold'> {df19['venue'].loc[0]}</span>",
            unsafe_allow_html=True)
        st.divider()

# START HERE ###


df = pd.read_csv('IPL_ball_by_ball_updated.csv.zip')
df.replace({'Arun Jaitley Stadium': 'Arun Jaitley Stadium, Delhi',
            'Brabourne Stadium': 'Brabourne Stadium, Mumbai',
            'Dr DY Patil Sports Academy, Mumbai': 'Dr DY Patil Sports Academy, Navi Mumbai',
            'Dr DY Patil Sports Academy': 'Dr DY Patil Sports Academy, Mumbai',
            'Eden Gardens': 'Eden Gardens, Kolkata',
            'Himachal Pradesh Cricket Association Stadium': 'Himachal Pradesh Cricket Association Stadium, Dharamsala',
            'M Chinnaswamy Stadium': 'M.Chinnaswamy Stadium, Bengaluru',
            'M Chinnaswamy Stadium, Bengaluru': 'M.Chinnaswamy Stadium, Bengaluru',
            'M.Chinnaswamy Stadium': 'M.Chinnaswamy Stadium, Bengaluru',
            'MA Chidambaram Stadium': 'MA Chidambaram Stadium, Chepauk, Chennai',
            'MA Chidambaram Stadium, Chepauk': 'MA Chidambaram Stadium, Chepauk, Chennai',
            'Maharashtra Cricket Association Stadium': 'Maharashtra Cricket Association Stadium, Pune',
            'Narendra Modi Stadium, Ahmedabad': 'Narendra Modi Stadium, Motera, Ahmedabad',
            'Sardar Patel Stadium, Motera': 'Narendra Modi Stadium, Motera, Ahmedabad',
            'OUTsurance Oval': 'Mangaung Oval, Bloemfontein',
            'New Wanderers Stadium': 'The Wanderers Stadium, Johannesburg',
            'Punjab Cricket Association IS Bindra Stadium': 'Punjab Cricket Association IS Bindra Stadium, Mohali, '
                                                            'Chandigarh',
            'Punjab Cricket Association IS Bindra Stadium, Mohali': 'Punjab Cricket Association IS Bindra Stadium, '
                                                                    'Mohali, Chandigarh',
            'Punjab Cricket Association Stadium, Mohali': 'Punjab Cricket Association IS Bindra Stadium,'
                                                          ' Mohali, Chandigarh',
            'Rajiv Gandhi International Stadium': 'Rajiv Gandhi International Stadium, Uppal, Hyderabad',
            'Rajiv Gandhi International Stadium, Uppal': 'Rajiv Gandhi International Stadium, Uppal, Hyderabad',
            'Sawai Mansingh Stadium': 'Sawai Mansingh Stadium, Jaipur',
            'Wankhede Stadium': 'Wankhede Stadium, Mumbai',
            'Subrata Roy Sahara Stadium': 'Maharashtra Cricket Association Stadium, Pune',
            'Feroz Shah Kotla': 'Arun Jaitley Stadium, Delhi'}, inplace=True)

orange_cap_holders_df = df.groupby(['season', 'striker'])['runs_off_bat'].sum().reset_index().sort_values(['season', 'runs_off_bat'], ascending = [False, False]).drop_duplicates('season')


# Calculate 'new_extras' using vectorized operations
byes_mask = df['byes'] >= 1
leg_byes_mask = df['legbyes'] >= 1
df['new_extras'] = df['extras'] - df['byes'].where(byes_mask, df['legbyes'].where(leg_byes_mask, 0))

# Calculate 'legal_balls' using vectorized operations
wides_mask = df['wides'] >= 1
no_balls_mask = df['noballs'] >= 1
df['legal_balls'] = 1 - df['wides'].where(wides_mask, df['noballs'].where(no_balls_mask, 0))

# Calculate 'wickets' using the isin() method with a list of wicket types
wicket_types = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
df['wickets'] = df['wicket_type'].isin(wicket_types).astype(int)

# Calculate 'runs_for_eco' using vectorized addition
df['runs_for_eco'] = df['runs_off_bat'] + df['new_extras']

# Sidebar
st.sidebar.title('Select One Option')
select = st.sidebar.selectbox('Statistics & Insights/Win Prediction', ['Win Prediction', 'Statistics & Insights'])
if select == 'Statistics & Insights':
    option = st.sidebar.selectbox('Batsman/Bowler', ['Batsman', 'Bowler'])

    if option == 'Batsman':
        selected_batsman = st.sidebar.selectbox('Select Batsman', sorted(df['striker'].unique().tolist()))
        btn1 = st.sidebar.button('Find Details')
        batsman_obj = Batsman(selected_batsman)
        if "btn1_state" not in st.session_state:
            st.session_state.btn1_state = False

        if btn1 or st.session_state.btn1_state:
            st.session_state.btn1_state = True
            load_player_details(selected_batsman)
            batsman_obj.batsman_details()

            st.write('Wants to know some valuable records!!')
            btn3_placeholder = st.empty()
            btn3 = btn3_placeholder.button("Show Information")

            if btn3:
                imp_info_of_batsman(batsman_obj.player)
            #   Remove the button by replacing it with an empty placeholder
                btn3_placeholder.empty()


    else:
        selected_bowler = st.sidebar.selectbox('Select Bowler', sorted(df['bowler'].unique().tolist()))
        btn2 = st.sidebar.button('Find Details')
        bowler_obj = Bowler(selected_bowler)
        if "btn2_state" not in st.session_state:
            st.session_state.btn2_state = False
        if btn2 or st.session_state.btn2_state:
            st.session_state.btn2_state = True
            load_player_details(selected_bowler)
            bowler_obj.bowler_details()

            st.write('Wants to know some valuable records!!')
            btn4_placeholder = st.empty()
            btn4 = btn4_placeholder.button("Show Information")
            if btn4:
                imp_info_of_bowler(bowler_obj.player)
                btn4_placeholder.empty()

else:
    with open('pipeline (2).pkl', 'rb') as file:
        loaded_pipeline = pickle.load(file)
    col1, col2, col3 = st.columns(3)
    batting_team = ['Kolkata Knight Riders', 'Sunrisers Hyderabad',
       'Chennai Super Kings', 'Delhi Capitals', 'Mumbai Indians',
       'Gujarat Titans', 'Royal Challengers Bangalore',
       'Rajasthan Royals', 'Lucknow Super Giants', 'Punjab Kings']
    bowling_team = ['Kolkata Knight Riders', 'Sunrisers Hyderabad',
       'Chennai Super Kings', 'Delhi Capitals', 'Mumbai Indians',
       'Gujarat Titans', 'Royal Challengers Bangalore',
       'Rajasthan Royals', 'Lucknow Super Giants', 'Punjab Kings']
    venues = ['Eden Gardens, Kolkata', 'Sharjah Cricket Stadium',
       'Wankhede Stadium, Mumbai', 'Kingsmead',
       'MA Chidambaram Stadium, Chepauk, Chennai',
       'Rajiv Gandhi International Stadium, Uppal, Hyderabad',
       'Sawai Mansingh Stadium, Jaipur',
       'Dubai International Cricket Stadium',
       'Arun Jaitley Stadium, Delhi', 'M.Chinnaswamy Stadium, Bengaluru',
       'Sheikh Zayed Stadium',
       'Maharashtra Cricket Association Stadium, Pune',
       'Dr DY Patil Sports Academy, Mumbai', "St George's Park",
       'The Wanderers Stadium, Johannesburg', 'Brabourne Stadium, Mumbai',
       'Dr DY Patil Sports Academy, Navi Mumbai',
       'JSCA International Stadium Complex', 'Newlands',
       'Narendra Modi Stadium, Motera, Ahmedabad',
       'Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh',
       'SuperSport Park', 'Zayed Cricket Stadium, Abu Dhabi',
       'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow',
       'Barsapara Cricket Stadium, Guwahati',
       'Himachal Pradesh Cricket Association Stadium, Dharamsala',
       'Barabati Stadium', 'Buffalo Park',
       'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
       'De Beers Diamond Oval']

    with col1:
        selected_batting_team = st.selectbox('Select Batting Team', batting_team)
        st.write('')
        selected_bowling_team = st.selectbox('Select Bowling Team', bowling_team)
        st.write(' ')
        selected_venue = st.selectbox('Select Venue', venues)
    with col2:
        target = st.number_input('Target', value=110)
        st.write(' ')
        runs_left = st.number_input('Runs Left', min_value=1, max_value=300, value=50, step=1)
    with col3:
        balls_left = st.number_input('Balls Left', min_value=1, max_value=120, value=50, step=1)
        st.write(' ')
        wickets_left = st.number_input('Wickets Left', min_value=0, max_value=10, value=0, step=1)

    crr = round((target-runs_left)/((120-balls_left)//6 + ((120-balls_left) % 6)/10), 2)
    rrr = round((runs_left/((balls_left//6)+((balls_left % 6)/10))), 2)
    input_df = pd.DataFrame({'batting_team': [selected_batting_team], 'bowling_team': [selected_bowling_team], 'venue': [selected_venue],
                            'target': [target], 'runs_left': [runs_left], 'balls_left': [balls_left],
                            'wickets_left': [wickets_left], 'current_run_rate': [crr], 'required_run_rate': [rrr]})
    if st.button('Predict Win Probability'):
        result = loaded_pipeline.predict_proba(input_df)[0]
        formatted_text = f"**{round(result[0] * 100, 2)}%**"
        st.markdown(f'**{selected_bowling_team}**: <span style="color:green">{formatted_text}</span>', unsafe_allow_html=True)
        formatted_text = f"**{round(result[1] * 100, 2)}%**"
        st.markdown(f'**{selected_batting_team}**: <span style="color:green">{formatted_text}</span>', unsafe_allow_html=True)