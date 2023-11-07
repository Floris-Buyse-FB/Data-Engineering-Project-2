import pandas as pd
from flask import Flask, request, jsonify
from utils.api_utils_functions import recommend, preproces_df

app = Flask(__name__)

@app.route('/post_data', methods=['POST'])
def post_data():
    try:
        # Get the JSON data from the request
        data = request.json

        # Get the new campaign data
        new_campaign_data = pd.DataFrame(data)

        # Get the recommended contact persons
        df = preproces_df()
        results = recommend(df, str(new_campaign_data))

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
