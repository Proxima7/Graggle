import os
SECRETS_PATH_PROD = os.getenv("SECRETS_PATH_PROD", "/mnt/secrets-store")
SECRETS_PATH_DEV = os.getenv("SECRETS_PATH_DEV", "/mnt/secrets-store")

def set_env():
    os.environ["APP_PORT"] = "8101"

