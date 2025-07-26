import streamlit as st
import preprocessor,help
import matplotlib.pyplot as plt
import seaborn as sns



# Inject CSS with the image as background
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.pexels.com/photos/2387793/pexels-photo-2387793.jpeg?cs=srgb&dl=pexels-adrien-olichon-1257089-2387793.jpg&fm=jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)



from help import daily_timeline

st.title("CHAT ANALYZER")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")

sidebar_bg = """
   <style>
   [data-testid="stSidebar"] {
       background-image: url("https://i.pinimg.com/736x/47/4f/b1/474fb17a4d3acea401e0ea9c10a3476e.jpg");
       background-size: cover;
       background-position: center;
   }
   </style>
   """
st.markdown(sidebar_bg, unsafe_allow_html=True)
st.sidebar.subheader("upload your file")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #to convert byte data type into utf-8 string
    data=bytes_data.decode("utf-8")
    # st.text(data)
    df=preprocessor.preprocessor(data)

    #fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    #analysis button
    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_messages, words,df1,link,media= help.fetch_stats(selected_user, df)
        st.header("Top Statistics:-")
        st.write(" ")
        st.write(" ")


        st.subheader(f"1) Total no of messages :-  {num_messages}")
        # st.subheader(num_messages)
        st.write(" ")

        st.subheader(f"2) Total no of words :-  {words}")
        # st.subheader(words)
        st.write(" ")

        st.subheader(f"3) Total no of media files shared :-  {media}")
        # st.subheader(media)
        st.write(" ")

        st.subheader(f"4) Total no of links shared :-  {link}")
        # st.subheader(link)
        st.write(" ")


        st.subheader(f"5) Messages sent by {selected_user} :-")

        st.write(" ")
        st.dataframe(df1)

#statistic graph
        # monthly timeline
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.title("Statistical Graph-Analysis")
        st.write(" ")
        st.write(" ")
        st.write(" ")


        st.header("Monthly Statistics :-")
        st.write(" ")
        timeline =help.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline["time"],timeline["message"],color="purple")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        st.write(" ")
        st.write(" ")



        # daily timeline
        st.write(" ")
        st.header("Daily Statistics :-")
        st.write(" ")
        daily_timeline= help.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(daily_timeline["only_date"], daily_timeline["message"], color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # activity map
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.title('Activity Map :-')
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Daily activity map :-")
            st.write(" ")
            busy_day = help.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.title("Most busiest day")
            ax.bar(busy_day.index, busy_day.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader("Monthly activity map :-")
            st.write(" ")
            busy_month = help.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.title("Most busiest month")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # heatmap
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.title("Weekly Activity Heat_Map :-")
        user_heatmap = help.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest user in the group

        if selected_user == 'Overall':
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.title('Most Busiest Users :-')
            st.write(" ")
            x, new_df = help.busy(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.write(" ")
                ax.bar(x.index, x.values, color='red')
                plt.xlabel("User_name")
                plt.ylabel("No of messages")
                plt.title("Graph of Busiest Users in the group :-")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.write(" ")
                st.dataframe(new_df)

        #wordcloud
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.title('Word cloud of one most common words used in the chat :-')
        st.write(" ")
        df_wc= help.wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

# most common words
        most_common_df = help.most_common_words(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()

            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')

            st.header('Most commmon words used in the chat:-')
            st.write(" ")
            st.pyplot(fig)
        with col2:
            st.header("Most common words DataFrame:-         ")
            st.write(" ")
            st.dataframe(most_common_df)


# emojis analysis
        st.write(" ")
        st.write(" ")
        st.write(" ")
        emoji_df = help.emoji_helper(selected_user, df)
        st.title("Emoji Analysis :-")
        st.write(" ")
        st.write(" ")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)