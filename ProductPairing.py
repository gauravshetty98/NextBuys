import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProductDirectoryBuilder:
    @staticmethod
    def preprocess_text(series):
        """
        Preprocesses text data by converting to lowercase and removing special characters.
        
        Args:
            series (pd.Series): A pandas Series containing text data.
        
        Returns:
            pd.Series: Preprocessed text data.
        """
        return series.str.lower().str.replace(r'[^\w\s]', '', regex=True)


    def calculate_similarity_scores(self, titles, vectorizer):
        """
        Calculates mean cosine similarity scores for each title against all other titles.
        
        Args:
            titles (pd.Series): A pandas Series containing product titles.
            vectorizer (TfidfVectorizer): The TF-IDF vectorizer instance.
        
        Returns:
            list: List of mean similarity scores.
        """
        tfidf_matrix = vectorizer.fit_transform(titles)
        similarity_scores = []
        
        for title in titles:
            target_tfidf = vectorizer.transform([title])
            cosine_similarities = cosine_similarity(target_tfidf, tfidf_matrix).flatten()
            similarity_scores.append(cosine_similarities.mean())
        
        return similarity_scores

    def process_category(self, cat, sub_cat_data, filtered_data, vectorizer, top_n=20):
        """
        Processes a single category, calculates similarity scores, and selects top products.
        
        Args:
            cat (str): Category name.
            sub_cat_data (pd.DataFrame): DataFrame containing category metadata.
            filtered_data (pd.DataFrame): DataFrame containing product data.
            vectorizer (TfidfVectorizer): The TF-IDF vectorizer instance.
            top_n (int): Number of top products to retain.
        
        Returns:
            pd.DataFrame: DataFrame containing top products for the category.
        """
    
        # Filter products for the given category
        cat_data = filtered_data[filtered_data['Category_x'] == cat].reset_index(drop=True)

        # Preprocess product titles
        cat_data['Title'] = self.preprocess_text(cat_data['Title'])
        
        # Calculate similarity scores
        cat_data['sim_index'] = self.calculate_similarity_scores(cat_data['Title'], vectorizer)
        
        # Add category ID
        cat_id = sub_cat_data[sub_cat_data['cat_title'] == cat].iloc[0, 1]
        cat_data['cat_id'] = cat_id
        
        # Sort by similarity scores and drop duplicates
        cat_data = cat_data.sort_values(by='sim_index', ascending=False).drop_duplicates(subset=['Title'], keep='first')
        
        # Retain top N most similar products
        return cat_data.head(top_n)

    def build_product_directory(self, sub_cat_data, filtered_data):
        """
        Builds a product directory by processing each category and selecting top similar products.
        
        Args:
            sub_cat_data (pd.DataFrame): DataFrame containing category metadata.
            filtered_data (pd.DataFrame): DataFrame containing product data.
        
        Returns:
            pd.DataFrame: Product directory with most relevant products.
        """
        vectorizer = TfidfVectorizer()
        new_df = pd.DataFrame()
        
        unique_categories = sub_cat_data['cat_title'].unique()
        
        for loop, cat in enumerate(unique_categories, start=1):
            cat_data = self.process_category(cat, sub_cat_data, filtered_data, vectorizer)
            new_df = pd.concat([new_df, cat_data], ignore_index=True)
        
        return new_df
    
    def get_recommendations_id(self, product_key, cosine_sim, prod_data):
        # Get the index of the product that matches the title
        idx = prod_data[prod_data['ASIN/ISBN (Product Code)'] == product_key].index[0]

        # Get the pairwise similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the products based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the product indices
        prod_indices = [i[0] for i in sim_scores]

        # Get the similarity scores
        sim_values = [i[1] for i in sim_scores]

        # Return the top 10 most similar movies
        return list(zip(prod_data['ASIN/ISBN (Product Code)'].iloc[prod_indices], sim_values))
    
    
    def build_pairing_directory(self, category_dir, new_df):
        vectorizer = TfidfVectorizer()
        pairing_dir = pd.DataFrame()

        print("Total = ", len(category_dir['cat_title'].unique()))
        loop = 0

        for cat in category_dir['cat_title'].unique():
            cat_data = new_df[new_df['Category_x'] == cat]
            cat_data = cat_data.reset_index(drop=True)
            temp_df = pd.DataFrame()
            tfidf_matrix = vectorizer.fit_transform(cat_data['Title'].str.lower().str.replace('[^\w\s]', ''))
            cosine_sim_tf = cosine_similarity(tfidf_matrix)
            for i in range(len(cat_data)):
                cosine_calcs = self.get_recommendations_id(cat_data.iloc[i,5], cosine_sim_tf, cat_data)
                temp_df['target_prod'] = [cat_data.iloc[i,5]]*len(cat_data)
                temp_df['compare_prod'] = [x[0] for x in cosine_calcs]
                temp_df['sim_values'] = [x[1] for x in cosine_calcs]
                # store the product keys in a new dataframe 
                pairing_dir = pd.concat([pairing_dir, temp_df], ignore_index= True)
            loop = loop+1

        return pairing_dir

