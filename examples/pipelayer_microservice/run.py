def start_service(specification_dir: str,
                  open_api_file: str = "openapi.yaml",
                  port: int = 8080):
    import connexion

    app = connexion.FlaskApp(__name__, specification_dir=specification_dir)
    app.add_api(open_api_file)
    app.run(port=port, debug=True)


if __name__ == "__main__":
    start_service(specification_dir="./")
