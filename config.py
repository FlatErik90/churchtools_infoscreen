import os


class Config:
    USERNAME = os.environ.get('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    CT_BASE_URL = "https://nak.church.tools"
