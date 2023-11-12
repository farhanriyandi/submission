import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

#load data
day_df = pd.read_csv('https://raw.githubusercontent.com/farhanriyandi/submission/main/data/day.csv')
hour_df = pd.read_csv('https://raw.githubusercontent.com/farhanriyandi/submission/main/data/hour.csv')

day_df.drop(columns='instant', inplace=True)
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

day_df['season'] = day_df['season'].map({1:"Spring", 2:"Summer", 3:"Fall", 4:"Winter"})

day_df['mnth'] = day_df['mnth'].map({1:"January", 2:"February", 3:"March", 4:"April", 5:"may", 6:"June", 7:"July", 8:"August", 9:"September",
                                     10:"October", 11:"November", 12: "December"})

day_df['holiday'] = day_df['holiday'].map({0:"No", 1:"Yes"})

day_df['weekday'] = day_df['weekday'].map({0:"Sunday", 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thrusday", 5:"Friday", 6:"Saturday"})

day_df['workingday'] = day_df['workingday'].map({0:"No", 1:"Yes"})

day_df['weathersit'] = day_df['weathersit'].map({1 :"Clear with few clouds", 2:"Misty or Cloudy", 3: "Light rain or Light snow",
                                                4: "Heavy rain or thick snowfall"})

day_df['yr'] = day_df['yr'].map({0:"2011", 1:"2012"})

columns = ['season', 'mnth', 'holiday','weekday', 'workingday','weathersit', 'yr']

for column in columns:
    day_df[column] = day_df[column].astype('category')

hour_df.drop(columns='instant', inplace=True)
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df['season'] = hour_df['season'].map({1:"Spring", 2:"Summer", 3:"Fall", 4:"Winter"})

hour_df['mnth'] = hour_df['mnth'].map({1:"January", 2:"February", 3:"March", 4:"April", 5:"may", 6:"Juny", 7:"July", 8:"August", 9:"September",
                                     10:"October", 11:"November", 12: "December"})

hour_df['holiday'] = hour_df['holiday'].map({0:"No", 1:"Yes"})

hour_df['weekday'] = hour_df['weekday'].map({0:"Sunday", 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thrusday", 5:"Friday", 6:"Saturday"})

hour_df['workingday'] = hour_df['workingday'].map({0:"No", 1:"Yes"})

hour_df['weathersit'] = hour_df['weathersit'].map({1 :"Clear with few clouds", 2:"Misty or Cloudy", 3: "Light rain or Light snow",
                                                4: "Heavy rain or thick snowfall"})

hour_df['yr'] = hour_df['yr'].map({0:"2011", 1:"2012"})

columns = ['season', 'mnth', 'holiday','weekday', 'workingday','weathersit', 'yr']

for column in columns:
    hour_df[column] = hour_df[column].astype('category')

# divided 2011 and 2012
duaribusebelas = day_df[day_df['yr'] == '2011']
duaribu2belas = day_df[day_df['yr'] == '2012']


# min date and max date
min_date = pd.to_datetime(day_df['dteday'].min())
max_date = pd.to_datetime(day_df['dteday'].max())

def create_monthly_df(df):
    df['dteday'] = pd.to_datetime(df['dteday'])

    monthly = df.resample(rule='M', on='dteday').agg({
        'cnt':'sum'
    })
    monthly.index = monthly.index.strftime('%Y-%m')
    monthly = monthly.reset_index()
    return monthly

def create_season(df):
    season_count = df.groupby('season')['cnt'].sum().reset_index()
    return season_count

def create_weather(df):
    weather_count = df.groupby('weathersit')['cnt'].sum().reset_index()
    return weather_count

def create_workingday(df):
    workingday_count = df.groupby('workingday')['cnt'].sum().reset_index()
    return workingday_count

def create_holiday(df):
    holiday_count = df.groupby('holiday')['cnt'].sum().reset_index()
    return holiday_count

def create_weekday_hour(df):
    weekday_hour = df.groupby(['hr', 'weekday'])['cnt'].sum().unstack()
    return weekday_hour

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://4rentbythebeach.com/wp-content/uploads/2020/11/Bike-Rental-Pompano-Beach-300x225.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

## Menyiapkan dataframe
monthly = create_monthly_df(day_df)
season_duaribusebelas = create_season(duaribusebelas)
season_duaribu2belas = create_season(duaribu2belas)
weather_duaribusebelas = create_weather(duaribusebelas) 
weather_duaribu2belas = create_weather(duaribu2belas)
workingday = create_workingday(day_df)
holiday = create_holiday(day_df)
weekday_hour = create_weekday_hour(hour_df)

# plot number of daily orders (2021)
st.header('Bike Sharing Dashboard 🚲')
st.subheader('Bike rentals per month from 2011 to 2012')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly["dteday"],
    monthly["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
plt.xticks(rotation=45)

st.pyplot(fig)

# peminjaman pada setiap season
st.subheader("The number of bike rentals for each season in 2011 and 2012")


fig = plt.figure(figsize=(15, 5), constrained_layout=True)
gs = fig.add_gridspec(nrows=1, ncols=2)

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

sns.barplot(data=season_duaribusebelas, x='season', y='cnt', palette=colors,ax=ax1)
ax1.bar_label(ax1.containers[0],fontsize=10)
# ax1.bar_label(ax1.containers[1],fontsize=10)
# ax1.bar_label(ax1.containers[2],fontsize=10)
# ax1.bar_label(ax1.containers[3],fontsize=10)
ax1.set_title("2011", loc="center", fontsize=15)

sns.barplot(data=season_duaribu2belas, x='season', y='cnt', palette=colors,ax=ax2)
ax2.bar_label(ax2.containers[0],fontsize=10)
# ax2.bar_label(ax2.containers[1],fontsize=10)
# ax2.bar_label(ax2.containers[2],fontsize=10)
# ax2.bar_label(ax2.containers[3],fontsize=10)
ax2.ticklabel_format(style='plain', axis='y')  # Menghilangkan notasi ilmiah pada sumbu y
ax2.set_title("2012", loc="center", fontsize=15)

st.pyplot(fig)

st.subheader('The number of bike rentals for each weather condition in 2011 and 2012')
#Peminjaman sepeda pada kondisi cuaca
fig = plt.figure(figsize=(15, 5), constrained_layout=True)
gs = fig.add_gridspec(nrows=1, ncols=2)

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

sns.barplot(data=weather_duaribusebelas, x='weathersit', y='cnt', palette=colors,ax=ax1)
ax1.bar_label(ax1.containers[0],fontsize=10)
# ax1.bar_label(ax1.containers[1],fontsize=10)
# ax1.bar_label(ax1.containers[2],fontsize=10)
ax1.set_title("2011", loc="center", fontsize=15)

sns.barplot(data=weather_duaribu2belas, x='weathersit', y='cnt', palette=colors,ax=ax2)
ax2.bar_label(ax2.containers[0],fontsize=10)
# ax2.bar_label(ax2.containers[1],fontsize=10)
# ax2.bar_label(ax2.containers[2],fontsize=10)
ax2.ticklabel_format(style='plain', axis='y')  # Menghilangkan notasi ilmiah pada sumbu y
ax2.set_title("2012", loc="center", fontsize=15)

st.pyplot(fig)

st.subheader('The number of bike renters based on working days and holidays')
fig = plt.figure(figsize=(15, 5), constrained_layout=True)
gs = fig.add_gridspec(nrows=1, ncols=2)

colors_ = ["#D3D3D3", "#72BCD4"]
colors = ["#72BCD4", "#D3D3D3"]

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

sns.barplot(data=workingday, x='workingday', y='cnt', palette=colors_,ax=ax1)
ax1.bar_label(ax1.containers[0],fontsize=10)
ax1.ticklabel_format(style='plain', axis='y')
ax1.set_title("workingday", loc="center", fontsize=15)

sns.barplot(data=holiday, x='holiday', y='cnt', palette=colors,ax=ax2)
ax2.bar_label(ax2.containers[0],fontsize=10)
ax2.ticklabel_format(style='plain', axis='y')  # Menghilangkan notasi ilmiah pada sumbu y
ax2.set_title("holiday", loc="center", fontsize=15)

st.pyplot(fig)


st.subheader('bicycle users based on 0-23 hours Monday-Sunday')
fig = plt.figure(figsize=(15, 5), constrained_layout=True)
gs = fig.add_gridspec(nrows=1, ncols=1)
ax = fig.add_subplot(gs[0])

markers = ['.', 'o', 's', 'D', '^', 'v', '>']  # Menentukan marker untuk setiap hari dalam seminggu
for i, day in enumerate(weekday_hour.columns):
    ax.plot(weekday_hour.index, weekday_hour[day], marker=markers[i], label=day)

ax.set_xlabel('Jam (hr)')
ax.set_ylabel('Jumlah (cnt)')
ax.set_title('Grafik Jumlah peminjam berdasarkan Jam dan Hari dalam Seminggu')
ax.legend()

st.pyplot(fig)


st.subheader("The correlation between the increase in bike rentals and temperature (temp), perceived temperature (atemp), humidity (humidity), and windspeed (windspeed)")
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20, 15))

sns.scatterplot(data=day_df, x="temp", y="cnt", ax=ax[0, 0])
ax[0, 0].set_ylabel(None)
ax[0, 0].set_xlabel(None)
ax[0, 0].set_title("temp vs cnt", loc="center", fontsize=18)
ax[0, 0].tick_params(axis ='x', labelsize=15)

sns.scatterplot(data=day_df, x="atemp", y="cnt", ax=ax[0, 1])
ax[0, 1].set_ylabel(None)
ax[0, 1].set_xlabel(None)
ax[0, 1].set_title("atemp vs cnt", loc="center", fontsize=18)
ax[0, 1].tick_params(axis ='x', labelsize=15)

sns.scatterplot(data=day_df, x="hum", y="cnt", ax=ax[1, 0])
ax[1, 0].set_ylabel(None)
ax[1, 0].set_xlabel(None)
ax[1, 0].set_title("hum vs cnt", loc="center", fontsize=18)
ax[1, 0].tick_params(axis ='x', labelsize=15)

sns.scatterplot(data=day_df, x="windspeed", y="cnt", ax=ax[1, 1])
ax[1, 1].set_ylabel(None)
ax[1, 1].set_xlabel(None)
ax[1, 1].set_title("windspeed vs cnt", loc="center", fontsize=18)
ax[1, 1].tick_params(axis ='x', labelsize=15)

st.pyplot(fig)