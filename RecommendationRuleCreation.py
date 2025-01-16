import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules

class RuleCreation:
    @staticmethod
    def load_data(file_path):
        """Load and return the dataset."""
        data = pd.read_csv(file_path)
        data['Order Date'] = pd.to_datetime(data['Order Date'])
        data = data.sort_values(by=['Survey ResponseID', 'Order Date'])
        return data

    @staticmethod
    def filter_orders(data):
        """Filter orders with more than one product per order."""
        data['order_id'] = data.groupby(['Survey ResponseID', 'Order Date']).ngroup() + 1
        order_counts = data.groupby('order_id').size().reset_index(name='count')
        data = pd.merge(data, order_counts, on='order_id', how='inner')
        data = data[data['count'] > 1]

        product_counts = data.groupby('order_id')['ASIN/ISBN (Product Code)'].nunique().reset_index(name='unique_products_count')
        data = pd.merge(data, product_counts, on='order_id', how='inner')
        data = data[data['unique_products_count'] > 1]

        title_category_count = data.groupby('Title')['Category'].nunique().sort_values(ascending=False)
        temp_df = pd.DataFrame(data=title_category_count)
        df = pd.merge(data, temp_df['Category'], on='Title', how='left')
        amazon_prod_details_wo_mul_cat = df[df['Category_y'] == 1]
        return amazon_prod_details_wo_mul_cat

    @staticmethod
    def generate_frequent_itemsets(data, min_support=0.01):
        """Generate frequent itemsets using FP-Growth."""
        basket = pd.pivot_table(data, 
                                 values='count', 
                                 index='order_id', 
                                 columns='Category_x', 
                                 aggfunc='count', 
                                 fill_value=0)

        basket = basket.applymap(lambda x: True if x > 0 else False)
        frequent_itemsets = fpgrowth(basket, min_support=min_support, use_colnames=True)
        return frequent_itemsets

    @staticmethod
    def generate_association_rules(frequent_itemsets, min_threshold=0.5):
        """Generate association rules from frequent itemsets."""
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_threshold)
        return rules

    @staticmethod
    def create_category_directory(rules):
        """Create a category directory from association rules."""
        rules["antecedents"] = rules["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
        rules["consequents"] = rules["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")

        cats = set()
        for _, row in rules.iterrows():
            for col in ["antecedents", "consequents"]:
                items = row[col].replace('(', '').replace(')', '').replace(' ', '').split(',')
                cats.update(items)

        cat_title = sorted(cats)
        cat_id = list(range(1, len(cat_title) + 1))

        category_dir = pd.DataFrame({
            'cat_title': cat_title,
            'cat_id': cat_id
        })
        return category_dir
