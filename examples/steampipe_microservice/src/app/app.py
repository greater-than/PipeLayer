import connexion

app = connexion.FlaskApp(__name__, specification_dir="../")
app.add_api("app.yaml")
app.run(port=8080)
