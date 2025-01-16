# NextBuys

# Recommendation Engine Website

## Overview
This project is a recommendation engine website designed to provide personalized product suggestions based on user interactions. It leverages advanced algorithms such as FP-Growth and Cosine Similarity to deliver two types of recommendations:

- **Frequently Bought Together Recommendations**
- **Similar Item Recommendations**

## Features
1. **Dynamic Recommendations**: 
   - Recommendations based on user behavior and interactions.
2. **Advanced Algorithms**:
   - FP-Growth for discovering frequent itemsets and generating association rules.
   - Cosine Similarity for identifying closely related items within categories.
3. **Interactive User Experience**:
   - Feedback system to fine-tune recommendations.
   - Real-time updates for product and cart page recommendations based on these feedbacks.

## Data Source
The data for this project is sourced from the [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/YGLYDY). The dataset, curated by the Stanford Network Analysis Project (SNAP), includes metadata on Amazon products, such as product titles, categories, and co-purchased items. It provides insights into consumer behavior and product relationships, forming the foundation for the recommendation engine.

### Preprocessing
- The focus was on the `amazon-purchases.csv` file containing 1,850,717 rows of transaction data.
- Extracted transactions with multiple purchased products to build a dataset for co-purchasing analysis.
- Categories with excessive products were optimized by selecting 20 representative products per category.
- Assigned unique category IDs for efficient processing.

## Methodology
### 1. **FP-Growth Algorithm**
#### Definition
The FP-Growth (Frequent Pattern Growth) algorithm is used to discover frequent itemsets efficiently by building a compact FP-tree.

#### Steps:
1. **Transaction-Product Matrix Creation**:
   - Constructed a matrix with binary entries to represent transactions.
2. **Frequent Items Calculation**:
   - Used a minimum support threshold of 0.008 to retain 70% of items for rule generation.
3. **FP-Tree Construction**:
   - Built a tree where branches represent transactions and nodes represent items.
4. **Mining the FP-Tree**:
   - Derived frequent itemsets using conditional pattern bases and conditional FP-trees.
5. **Evaluation Metrics**:
   - **Support**: Frequency of an itemset.
   - **Confidence**: Likelihood of co-purchasing.
   - **Lift**: Strength of the association.
6. **Rule Selection**:
   - Confidence used for single antecedents; lift for multiple antecedents.

### 2. **Cosine Similarity**
#### Definition
Cosine Similarity measures the cosine of the angle between two non-zero vectors, determining their similarity independent of magnitude.

#### Steps:
1. **Dataset Creation**:
   - Product titles were vectorized using TF-IDF.
2. **Category Segmentation**:
   - Grouped products by category to ensure relevant comparisons.
3. **Vectorization**:
   - Converted titles to TF-IDF vectors to capture textual features.
4. **Similarity Calculation**:
   - Pairwise cosine similarity computed for products within each category.
5. **Result Storage**:
   - Stored similarity scores for real-time recommendation retrieval.

## Website Functionality
### **Datasets Utilized**
1. **Product Directory**: Comprehensive product details.
2. **Category Directory**: Information about product categories.
3. **Association Rules Directory**: Stores FP-Growth-generated rules.
4. **Cosine Similarity Directory**: Stores similarity scores for products.

### **Workflow**
1. **Home Page**:
   - Displays categories fetched from the Category Directory.
2. **Product Selection**:
   - Retrieves products and generates recommendations based on FP-Growth and Cosine Similarity.
3. **Cart Page Recommendations**:
   - Refines recommendations using lift for association rules.
4. **No Recommendations**:
   - Indicates unavailability if rules or scores are missing.

### **Recommendation Processes**
#### **Association Rules-Based Recommendations**:
- Retrieves top 2-3 relatable categories using sorted association rules.

#### **Cosine Similarity-Based Recommendations**:
- Displays the top 5 similar products based on user selection.

### **Feedback System**
- **Like**: Increases recommendation priority.
- **Dislike**: Reduces recommendation likelihood.
- Feedback dynamically updates future suggestions.

## Technical Details
- **Languages and Tools**: Python, SQL, HTML, CSS, JavaScript.
- **Data Processing Libraries**: Pandas, NumPy, Scikit-learn.
- **Algorithms**: MLXTEND [FPGRWOTH & Association rules], TF-IDF, .

## Prerequisites
- Python 3.8+
- Libraries present in requirements.txt

## Contributors
- **Gaurav Shetty** - [gss119@scarletmail.rutgers.edu](mailto:gss119@scarletmail.rutgers.edu)
- **Naimish Sharma** - [ns1568@scarletmail.rutgers.edu](mailto:ns1568@scarletmail.rutgers.edu)
- **Nihil Kotal** - [nihil.kottal@rutgers.edu](mailto:nihil.kottal@rutgers.edu)

---

Feel free to raise issues or contribute to this project through pull requests!
