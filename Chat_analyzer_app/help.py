from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user !="Overall" :
       df=df[df['user']==selected_user]
# to fetch the number of messages
    num_messages = df.shape[0]
# to fetch the number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
# to fetch the dataframe according to the user
    df1=df

    #to fetch the no of links shared
    link=[]
    for message in df['message']:
        link.extend(extract.find_urls(message))


    #to fetch the number of media files:
    media=df[df["message"]=="<Media omitted>\n"].shape[0]


    return num_messages,len(words),df1,len(link),media


#busiest person
def busy(df):
    x = df["user"].value_counts()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df



#wordcloud
def wordcloud(selected_user,df):
    f = open("stop_hinglish.txt", "r")
    stop_word = f.read()

    if selected_user !="Overall" :
        df=df[df['user']==selected_user]

    temp = df[df["user"] != "group_notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]
    temp = temp[temp["message"] != ""]



    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_word:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=600, height=400,min_font_size=10,background_color="black")
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp["message"].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp["message"] != ""]


    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


# emoji analysis
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        all_emojis = emoji.EMOJI_DATA
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))

    timeline["time"] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby("only_date").count()["message"]

    daily_timeline = daily_timeline.reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df["day_name"]=df["date"].dt.day_name()

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap