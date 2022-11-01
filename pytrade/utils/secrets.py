from loadenv import EnvEnum


class ClientSecret(EnvEnum):
    CLIENT_SECRET_TYPE: str = "service_account"
    CLIENT_SECRET_PROJECT_ID: str = ()
    CLIENT_SECRET_PRIIVATE_KEY_ID: str = ()
    CLIENT_SECRET_PRIVATE_KEY: str = ()
    CLIENT_SECRET_CLIENT_EMAIL: str = ()
    CLIENT_SECRET_CLIENT_ID: str = ()
    CLIENT_SECRET_AUTH_URI: str = "https://accounts.google.com/o/oauth2/auth"
    CLIENT_SECRET_TOKEN_URI: str = "https://oauth2.googleapis.com/token"
    CLIENT_SECRET_AUTH_PROVIDER_x509_CERT_URL: str = "https://www.googleapis.com/oauth2/v1/certs"
    CLIENT_SECRET_CLIENT_x509_CERT_URL: str = ()

    @staticmethod
    def to_json() -> dict[str, str]:
        return {
            "secret_type": ClientSecret.CLIENT_SECRET_TYPE.value,
            "project_id": ClientSecret.CLIENT_SECRET_PROJECT_ID.value,
            "private_key_id": ClientSecret.CLIENT_SECRET_PRIIVATE_KEY_ID.value,
            "private_key": ClientSecret.CLIENT_SECRET_PRIVATE_KEY.value.replace("\\n", "\n"),
            "client_email": ClientSecret.CLIENT_SECRET_CLIENT_EMAIL.value,
            "client_id": ClientSecret.CLIENT_SECRET_CLIENT_ID.value,
            "auth_uri": ClientSecret.CLIENT_SECRET_AUTH_URI.value,
            "token_uri": ClientSecret.CLIENT_SECRET_TOKEN_URI.value,
            "auth_provider_x509_cert_url": ClientSecret.CLIENT_SECRET_AUTH_PROVIDER_x509_CERT_URL.value,
            "client_x509_cert_url": ClientSecret.CLIENT_SECRET_CLIENT_x509_CERT_URL.value
        }