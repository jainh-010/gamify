#importing the required libraries
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask,request
from flask.templating import render_template

#loading the dataset
path = 'vgames.csv'

app=Flask(__name__)

#reading the dataset
ds= pd.read_csv(path)

#Checking the dataset for duplicate enteries 
#ds.head()

#creating  the list of important columns for engine
columns =['Title','Metadata.Publishers','Features.Max Players','Metadata.Genres','Release.Console','Features.Online?','Release.Rating']

#checking for missing values in the columns selected 
null = ds.isnull().sum()

#Filling the missing values in the columns need to be used
ds['Metadata.Publishers'] =ds['Metadata.Publishers'].fillna('not specified')

#Rechecking for the missing values
null = ds[columns].isnull().values.any()
print("Any null values : ",end='')
print(null)

#creating a function to combine important values in single string
def get_important_features(row):
  try:
    return row['Title']+""+row['Metadata.Genres']+""+row['Metadata.Publishers']+""+row['Release.Console']+""+row['Release.Rating']
  except:
    print("Error:",row)
  #return important_features
ds['features']=ds.apply(get_important_features,axis=1)

#Convert to matrix
cm=CountVectorizer().fit_transform(ds['features'])

#get the cosine similarities
cs = cosine_similarity(cm)

#Getting the input from the user
# title = "Hail to the Chimp"


@app.route('/')
def home():
    return render_template("index1.html")
    
@app.route('/output',methods=['GET','POST'])
def output():
    #getting the input from the form
    title = request.args.get('gname')
    #list_of_all_titles = ds['Title'].tolist()
    #find_close_match = difflib.get_close_matches(title, list_of_all_titles)
    #close_match = find_close_match[0]
    #index_of_the_game = ds[ds.Title == close_match]['game_id'].values[0]

    if title.title() in ds.values :
        
        #find the similarties
        game_id = ds[ds.Title == title.title()]["game_id"].values[0]
    
        #Creating a list for the similarities
        scores = list(enumerate(cs[game_id]))
        
        #Sorting the list
        sorted_score = sorted(scores,key = lambda x:x[1], reverse =True)
        sorted_score = sorted_score [1:]

        #Creating a loop to print top 5 games
        j=0
        #print("Top 5 similar games are :\n")
        result = []
        for games in sorted_score:
            game_title = ds[ds.game_id == games[0]]['Title'].values[0]
            result.append(game_title)
            #print(j+1 ,game_title)
            j=j+1
            if j>4:
                break
  
        return render_template("output.html",Games=result)

    else :
        return render_template("output.html", game = "No games to recommend found in database")

if __name__=='__main__':
    app.run(debug=True)
