from flask import Flask,render_template,jsonify
import pandas as pd
import pickle

from flask import Flask
app = Flask(__name__)

@app.route('/')
def api_help():
    return render_template('index.html')

@app.route('/api/recommendation/<string:movie>')
def get_recommendation(movie):
    df=pd.read_csv('find_index.csv')
    index=df[df['movie_title'] == movie]["index"].values[0]

    with open('recommendation.pkl', 'rb') as file:  
        LOAD_MODEL = pickle.load(file)

    similar_movies = list(enumerate(LOAD_MODEL[index]))

    sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse=True)

    def get_title_from_index(index):
        return df[df.index == index]["movie_title"].values[0]
    
    l=[]

    i=0
    for movie in sorted_similar_movies:
        m=get_title_from_index(movie[0])
        if type(m) is float:
            continue
        l.append(m)
        i=i+1
        if i>15:
            break
        
    return jsonify({'similar_movies':l})


@app.route('/api/review/<string:review>')
def get_review(review):
    count_vectorizer=pickle.load(open("count_vectorizer",'rb'))
    model_clf=pickle.load(open("model_clf" ,'rb'))
    test=pd.Series(review)
    vector=count_vectorizer.transform(test)
    result=int(model_clf.predict(vector)[0])
    return jsonify({'result':result})

if __name__ == "__main__":
    app.run(debug=True)