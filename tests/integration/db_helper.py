def db_params(container) -> dict:
    return {
        "host": container.get_container_host_ip(),
        "port": int(container.get_exposed_port(5432)),
        "database": container.dbname,
        "user": container.username,
        "password": container.password,
    }
