from flask import Flask, jsonify
import yaml

app = Flask(__name__)

def load_spec():
    with open("tasks-api.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@app.route("/openapi.json")
def spec_json():
    return jsonify(load_spec())

@app.route("/docs")
def docs():
    swagger_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Tasks API - Swagger UI</title>
      <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css" />
    </head>
    <body>
      <div id="swagger-ui"></div>
      <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js" crossorigin></script>
      <script>
        window.onload = () => {
          window.ui = SwaggerUIBundle({
            url: '/openapi.json', 
            dom_id: '#swagger-ui',
          });
        };
      </script>
    </body>
    </html>
    """
    return swagger_html

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)