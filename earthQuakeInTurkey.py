#read data file
from importlib.resources import path
import pandas as pd
#data path
DATA_PATH = r""
#clearing data from unnecessary datas
data = pd.read_csv(DATA_PATH, delimiter=';')
print(data.head())
data = data.drop(['No','Deprem Kodu','Tip'],axis=1)
print(data.head())

data['Olus zamani'] = data['Olus zamani'].str.split('.').str[0]
#clearing data from wrong index
for i in range(0,len(data)):
    if float(data['Olus zamani'][i][6:])>=60:
        data = data.drop(i)
data = data.reset_index(drop=True)#reset index

#creating single column with olus zamani and olus tarihi
# Creating single column for date and time
time = pd.to_datetime(data['Olus tarihi']+' '+data['Olus zamani'])
data['Olus zamani'] = time
data.drop(['Olus tarihi'],axis=1,inplace=True)
print(data.head())

# Creating a list with empty string values
place = []
for y in range(len(data)):
    place.append("")

# Placing Yer values to the empty list
for i in range(0, len(data)):
    place[i] = data['Yer'][i]

    # If the Yer values have '(', it will divided by left and right side of the '(', ')' in order
    if place[i].find("(") != -1:
        place[i] = place[i].split('(')[1]
        place[i] = place[i].split(')')[0]
place = pd.DataFrame(place)
print(place.head())

# Getting rid of the string values start with '['
place = place[0].str.split('[').str[0].to_frame()
place.columns = ['Yer']

# Placing the created Yer column to the original dataset
data['Yer'] = place

# Some data points have missing letters due to Turkish Alphabet unique letters
place_update = {"?ORUM": "CORUM", "K?TAHYA": "KUTAHYA", "EGE DENiZi": "EGE DENIZI",
              "DiYARBAKIR": "DIYARBAKIR", "T?RKiYE-iRAN SINIR B?LGESi": "TURKIYE-IRAN SINIR BOLGESI",
              "BALIKESiR ": "BALIKESIR", "SiVAS": "SIVAS", "iZMiR": "IZMIR", "TUNCELi": "TUNCELI",
              "SURiYE": "SURIYE", "ESKiSEHiR": "ESKISEHIR", "DENiZLi": "DENIZLI", "BiTLiS": "BITLIS",
              "KiLiS": "KILIS", "VAN G?L?": "VAN GOLU", "?ANKIRI": "CANKIRI",
              "T?RKIYE-IRAN SINIR B?LGESI": "TURKIYE-IRAN SINIR BOLGESI", "MANiSA": "MANISA",
              "AKDENiZ": "AKDENIZ", "G?RCiSTAN": "GURCISTAN", "BiNGOL": "BINGOL", "OSMANiYE": "OSMANIYE",
              "KIRSEHiR": "KIRSEHIR", "MARMARA DENiZi": "MARMARA DENIZI", "ERZiNCAN": "ERZINCAN",
              "BALIKESiR": "BALIKESIR", "GAZiANTEP": "GAZIANTEP", "G?RCISTAN": "GURCISTAN",
              "?ANAKKALE'": "CANAKKALE", "HAKKARi": "HAKKARI", "AFYONKARAHiSAR": "AFYONKARAHISAR",
              "BiLECiK": "BILECIK", "KAYSERi": "KAYSERI", "T?RKiYE-IRAK SINIR B?LGESi": "TURKIYE-IRAK SINIR BOLGESI",
              "KARADENiZ": "KARADENIZ", "T?RKIYE-IRAK SINIR B?LGESI": "TURKIYE-IRAK SINIR BOLGESI",
              "KARAB?K": "KARABUK", "KIBRIS-SADRAZAMK?Y?K": "KIBRIS-SADRAZAMKOY",
              "T?RKIYE-SURIYE SINIR B?LGESI?K": "TURKIYE-SURIYE SINIR BOLGESI", "?ANAKKALE": "CANAKKALE",
              "KIBRIS-SADRAZAMK?Y": "KIBRIS-SADRAZAMKOY", "ERZURUM ": "ERZURUM",
              "T?RKIYE-SURIYE SINIR B?LGESI": "TURKIYE-SURIYE SINIR BOLGESI", "ADANA ": "ADANA", "KUS G?L?": "KUS GOLU",
              "BURDUR ": "BURDUR", "KIBRIS-G?ZELYURT": "KIBRIS-GUZELYURT", "KONYA ": "KONYA",
              "KOCAELI ": "KOCAELI", "AMASYA ": "AMASYA", "KIRSEHIR ": "KIRSEHIR",
              "KIBRIS-KILI?ASLAN": "KIBRIS-KILICASLAN", "KIBRIS-Z?MR?TK?Y": "KIBRIS-ZUMRUTKOY",
              "DENIZLI ": "DENIZLI", "MANISA ": "MANISA", "ULUBAT G?L?": "ULUBAT GOLU",
              "T?RKIYE-ERMENISTAN SINIR B?LGESI": "TURKIYE-ERMENISTAN SINIR BOLGESI",
              "ERZINCAN ": "ERZINCAN", "TOKAT ": "TOKAT", "ARDAHAN ": "ARDAHAN"}
data['Yer'] = data['Yer'].replace(place_update)
print(data['Yer'].head())
#creating plot diagrams
#imports
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
#Distribution of the Earthquakes (Annually)
fig1 = px.histogram(data_frame=data, x='Olus zamani')
fig1.update_layout(title_text='Distribution of the Earthquakes (Annually)',
                       title_x=0.5, title_font=dict(size=32))
fig1.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig1.show()
#Distribution of the Magnitudes
fig2 = px.histogram(data_frame=data,x='xM',marginal='rug', hover_data=data.columns)
fig2.update_layout(title_text='Distribution of the Magnitudes',
                  title_x=0.5, title_font=dict(size=32))
fig2.show()
#Distribution of the Depth(km)
fig3 = px.histogram(data_frame=data,x='Derinlik', marginal='rug', hover_data=data.columns)
fig3.update_layout(title_text='Distribution of the Depth(km)',
                       title_x=0.5, title_font=dict(size=32))
fig3.show()
#Relationship between the Depth and the Magnitude
fig4 = px.scatter(data,x='Derinlik',y='xM')
fig4.update_layout(title_text='Relationship between the Depth and the Magnitude',
                       title_x=0.5, title_font=dict(size=32))
fig4.show()
#Number of Earthquakes due to Location
Yer_count = data.groupby(pd.Grouper(key='Yer')).size().reset_index(name='count')
fig = px.treemap(Yer_count, path=['Yer'], values='count')
fig.update_layout(title_text='Number of Earthquakes due to Location',
                  title_x=0.5, title_font=dict(size=30)
                  )
fig.update_traces(textinfo="label+value")
fig.show()
#Top 10 Frequent Earthquake Locations
Yer_count = data.groupby(pd.Grouper(key='Yer')).size().reset_index(name='count')
Yer_count_top = Yer_count.nlargest(10, 'count')[['Yer', 'count']]
fig = px.bar(Yer_count_top, x='Yer', y='count', color='Yer', text='count')
fig.update_layout(title_text='Top 10 Frequent Earthquake Locations',
                  title_x=0.5, title_font=dict(size=30))
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.show()
#Heatmap of the Earthquakes (animated)

fig = px.density_mapbox(data, lat=data['Enlem'], lon=data['Boylam'], z=data['xM'],
                        center=dict(lat=39.42, lon=35), zoom=4.5,
                        mapbox_style="stamen-terrain",
                        radius=15,
                        opacity=0.5,
                        animation_frame=pd.DatetimeIndex(data['Olus zamani']).date)
fig.update_layout(title_text='Heatmap of the Earthquakes (animated)',
                  title_x=0.5, title_font=dict(size=32))
fig.show()
#Heatmap of the Earthquakes (stable)
fig = px.density_mapbox(data, lat=data['Enlem'], lon=data['Boylam'], z=data['xM'],
                        center=dict(lat=39.42, lon=35), zoom=4.5,
                        mapbox_style="stamen-terrain",
                        radius=10,
                        opacity=0.5)
fig.update_layout(title_text='Heatmap of the Earthquakes',
                  title_x=0.5, title_font=dict(size=32))
fig.show()
#Top 30 Largest Earthquakes in the Turkey
top_mag = data.nlargest(30, 'xM')[['Yer', 'xM', 'Enlem', 'Boylam']]
fig = px.density_mapbox(top_mag, lat=top_mag['Enlem'], lon=top_mag['Boylam'], z=top_mag['xM'],
                        center=dict(lat=39.42, lon=35), zoom=4.5,
                        mapbox_style="open-street-map",
                        radius=30,
                        opacity=0.8)
fig.update_layout(title_text='Top 30 Largest Earthquakes in the Turkey',
                  title_x=0.5, title_font=dict(size=32))
fig.show()
#Top 30 Earthquakes due to Magnitude vs Year
fig = px.scatter(data.nlargest(30, 'xM')[['xM', 'Yer', 'Olus zamani']],
                 x='Olus zamani', y='xM', color='Yer', text='xM', hover_name='Olus zamani',
                 size='xM')
fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
fig.update_layout(title_text='Top 30 Earthquakes due to Magnitude vs Year',  # Main title for the project
                  title_x=0.5, title_font=dict(size=30))  # Location and the font size of the main title

fig.show()
#Distribution of the Earthquakes due to Lat and Long (M>5)
fig = go.Figure(data=[go.Scatter3d(
    x=data['Enlem'],
    y=data['Boylam'],
    z=data[data['xM'] >= 5]['xM'],
    mode='markers+text',
    hovertext=data['Yer'],
    marker=dict(
        size=5,
        color=data['xM'],
        colorscale='Viridis',
        opacity=0.8
    ),
    text=data[data['xM'] >= 5]['xM'],
)])
fig.update_layout(scene=dict(
    xaxis_title='Latitude',
    yaxis_title='Longitude',
    zaxis_title='xM')
)
fig.update_layout(title_text='Distribution of the Earthquakes due to Lat and Long (M>5)',
                  title_x=0.5, title_font=dict(size=22))
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
fig.show()
#Correlation Graph

plt.figure(figsize=(15, 8))
correlation = sns.heatmap(data.corr(), vmin=-1, vmax=1, annot=True, linewidths=1, linecolor='black')
correlation.set_title('Correlation Graph of the Dataset', fontdict={'fontsize': 24})