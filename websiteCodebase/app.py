from flask import Flask, render_template, request, jsonify
import sqlite3


app = Flask(__name__)

# Function to connect to SQLite and fetch data
def fetch_data(query, params=()):
    conn = sqlite3.connect("data/recommendation.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

# Function to update similarity score
@app.route("/update_similarity", methods=["POST"])
def update_similarity():
    data = request.json
    source_product = data["source_product"]
    target_product = data["target_product"]
    change = data["change"]  # +1 for thumbs up, -1 for thumbs down

    conn = sqlite3.connect("data/recommendation.db")
    cursor = conn.cursor()

    # Update the similarity score
    cursor.execute("""
        UPDATE cosine_similarity 
        SET cosine_sim_score = cosine_sim_score + ?
        WHERE source_product = ? AND target_product = ?;
    """, (change, source_product, target_product))

    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Similarity score updated."})



# Home Page - List Categories
@app.route("/")
def home():
    # Get page number from request
    page = request.args.get("page", 1, type=int)
    categories_per_page = 12

    # Fetch all categories
    all_categories = fetch_data("SELECT * FROM categories ORDER BY cat_name ASC;")
    total_categories = len(all_categories)
    
    # Pagination logic
    start_idx = (page - 1) * categories_per_page
    end_idx = start_idx + categories_per_page
    paginated_categories = all_categories[start_idx:end_idx]

    total_pages = (total_categories // categories_per_page) + (1 if total_categories % categories_per_page > 0 else 0)

    return render_template("home.html", 
                           categories=paginated_categories, 
                           page=page, 
                           total_pages=total_pages)


# Category Page - Show Products in Selected Category
@app.route("/category/<category_id>")
def category(category_id):
    products = fetch_data("SELECT * FROM products WHERE cat_id = ?;", (category_id,))
    return render_template("category.html", products=products)

# Product Page - Show Product Details & Recommendations
@app.route("/product/<product_id>")
def product(product_id):
    # Fetch Product Details
    product = fetch_data("SELECT * FROM products WHERE product_id = ?;", (product_id,))
    
    if not product:
        return "Product not found!", 404

    product = product[0]  # Convert to a tuple
    # Fetch Category-Based Recommendations (From Rules Table)
    query = """SELECT consequents FROM rules WHERE antecedents_id LIKE ? ORDER BY confidence DESC LIMIT 5;"""
    # Different ways to match: 
    params = (f"[{product[1]}]",)

    category_recommendations = fetch_data(
        query,
        params  # product[1] is category_id
    )

    # ✅ Fetch Product-Based Recommendations with Titles (Top 5)
    product_recommendations = fetch_data(
        """
        SELECT p.product_id, p.product_name 
        FROM products p
        JOIN cosine_similarity c ON p.product_id = c.target_product
        WHERE c.source_product = ?
        ORDER BY c.cosine_sim_score DESC
        LIMIT 5;
        """,
        (product_id,)
    )

    return render_template(
        "product.html",
        product=product,
        category_recommendations=category_recommendations,
        product_recommendations=product_recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)
