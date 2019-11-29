import flaskblog

app = flaskblog.create_app()

if __name__ == "__main__":
    app.run(host="localhost", debug=True)
