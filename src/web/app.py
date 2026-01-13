from flask import Flask, request, render_template_string
from src.query.sourcewise_summary import summarize_by_source
from src.query.trending_topics import get_trending_topics

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Global News AI</title>
</head>
<body style="font-family: Arial; margin: 40px;">
    <h2>🌍 Global News AI (Test)</h2>

    <h4>🔥 Trending Topics</h4>
    <form method="post">
        {% for topic in trending %}
            <button name="query" value="{{ topic }}" type="submit">
                {{ topic.capitalize() }}
            </button>
        {% endfor %}
    </form>

    <hr>

    <form method="post">
        <input type="text" name="query" placeholder="Search news..." size="40" required>
        <button type="submit">Search</button>
    </form>

    {% if results %}
        <hr>
        {% for source, summary in results.items() %}
            <h3>{{ source.upper() }}</h3>
            <p>{{ summary }}</p>
        {% endfor %}
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    query = None

    trending = get_trending_topics()

    if request.method == "POST":
        query = request.form["query"]
        results = summarize_by_source(query)

    return render_template_string(
        HTML,
        results=results,
        trending=trending
    )

if __name__ == "__main__":
    app.run(debug=True)
