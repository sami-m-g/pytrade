import os

from dotenv import load_dotenv


class ClientSecret:
    load_dotenv()

    CLIENT_SECRET_TYPE: str = "service_account"
    CLIENT_SECRET_PROJECT_ID: str = os.getenv("CLIENT_SECRET_PROJECT_ID")
    CLIENT_SECRET_PRIIVATE_KEY_ID: str = os.getenv("CLIENT_SECRET_PRIIVATE_KEY_ID")
    CLIENT_SECRET_PRIVATE_KEY: str = os.getenv("CLIENT_SECRET_PRIVATE_KEY")
    CLIENT_SECRET_CLIENT_EMAIL: str = os.getenv("CLIENT_SECRET_CLIENT_EMAIL")
    CLIENT_SECRET_CLIENT_ID: str = os.getenv("CLIENT_SECRET_CLIENT_ID")
    CLIENT_SECRET_AUTH_URI: str = "https://accounts.google.com/o/oauth2/auth"
    CLIENT_SECRET_TOKEN_URI: str = "https://oauth2.googleapis.com/token"
    CLIENT_SECRET_AUTH_PROVIDER_x509_CERT_URL: str = "https://www.googleapis.com/oauth2/v1/certs"
    CLIENT_SECRET_CLIENT_x509_CERT_URL: str = os.getenv("CLIENT_SECRET_CLIENT_x509_CERT_URL")

    @staticmethod
    def to_json() -> dict[str, str]:
        return {
            "secret_type": ClientSecret.CLIENT_SECRET_TYPE,
            "project_id": ClientSecret.CLIENT_SECRET_PROJECT_ID,
            "private_key_id": ClientSecret.CLIENT_SECRET_PRIIVATE_KEY_ID,
            "private_key": ClientSecret.CLIENT_SECRET_PRIVATE_KEY.replace("\\n", "\n"),
            "client_email": ClientSecret.CLIENT_SECRET_CLIENT_EMAIL,
            "client_id": ClientSecret.CLIENT_SECRET_CLIENT_ID,
            "auth_uri": ClientSecret.CLIENT_SECRET_AUTH_URI,
            "token_uri": ClientSecret.CLIENT_SECRET_TOKEN_URI,
            "auth_provider_x509_cert_url": ClientSecret.CLIENT_SECRET_AUTH_PROVIDER_x509_CERT_URL,
            "client_x509_cert_url": ClientSecret.CLIENT_SECRET_CLIENT_x509_CERT_URL
        }