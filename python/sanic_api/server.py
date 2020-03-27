from apps import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6070, debug=True, workers=4)