from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession


def create_credentials(service_account_file_path):
    scopes = ["https://www.googleapis.com/auth/homegraph"]
    return service_account.Credentials.from_service_account_file(
        service_account_file_path, scopes=scopes
    )


def create_authorized_session(credentials):
    return AuthorizedSession(credentials)
