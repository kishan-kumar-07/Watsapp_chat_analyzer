import re
import pandas as pd

def preprocessor(data):
    pattern = "\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s?[ap]m\s-\s"

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    df = pd.DataFrame({"user_message": messages, "message_date": dates})
    # Clean invisible unicode spaces like \u202f and normal whitespace
    df["message_date"] = df["message_date"].str.replace('\u202f', ' ', regex=False).str.strip()

    # Now safely parse the datetime
    df["message_date"] = pd.to_datetime(df["message_date"], format='%d/%m/%y, %I:%M %p -')

    # Rename column
    df.rename(columns={"message_date": "date"}, inplace=True)

    users = []
    messages = []
    for message in df["user_message"]:
        entry = re.split("([\w\W]+?):\s", message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])

    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user_message"], inplace=True)

    df["year"] = df["date"].dt.year

    df["month_num"] = df["date"].dt.month

    df["only_date"] = df["date"].dt.date

    df["month"] = df["date"].dt.month_name()

    df["day_name"]=df["date"].dt.day_name()

    df["day"] = df["date"].dt.day

    df["hour"] = df["date"].dt.hour

    df["minute"] = df["date"].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df