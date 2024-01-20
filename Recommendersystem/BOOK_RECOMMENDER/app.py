from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

popular_df = pickle.load(open("MODEL/popular.pkl", 'rb'))
books = pickle.load(open("MODEL/books.pkl", 'rb'))
pt = pickle.load(open("MODEL/pt.pkl", 'rb'))
similarity_scores = pickle.load(open("MODEL/similarity_scores.pkl", 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=[title for title in popular_df['Book-Title'].values],
                           author=[author for author in popular_df['Book-Author'].values],
                           image=[url for url in popular_df['Image-URL-M'].values],
                           votes=[votes for votes in popular_df['num-ratings'].values],
                           ratings=[rating for rating in popular_df['avg-rating'].values],
                           )


@app.route('/book_recommend')
def book_recommend():
    return render_template('book_recommend.html')


@app.route('/recommended_books', methods=['post'])
def recommended_books():
    user_input = request.form.get('user_input')

    if user_input in pt.index:
        book_index = np.where(pt.index == user_input)[0][0]

        similar_items = sorted(list(enumerate(similarity_scores[book_index])), key=lambda x: x[1], reverse=True)[1:7]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]

            # Extract unique values from 'Book-Title', 'Book-Author', and 'Image-URL-M'
            unique_titles = temp_df.drop_duplicates('Book-Title')['Book-Title'].unique().tolist()
            unique_authors = temp_df.drop_duplicates('Book-Title')['Book-Author'].unique().tolist()
            unique_images = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].unique().tolist()

            # Extend the 'item' list with the unique values
            item.extend(unique_titles)
            item.extend(unique_authors)
            item.extend(unique_images)

            data.append(item)
    else:
        data = []

    return render_template('book_recommend.html', data=data, user_input=user_input)


@app.route('/no_recommendations')
def no_recommendations():
    return render_template('no_recommendations.html')


if __name__ == "__main__":
    app.run(debug=True)
