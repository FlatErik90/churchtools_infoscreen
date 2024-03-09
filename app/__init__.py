from flask import Flask
from config import Config
import churchtools as ct


app = Flask(__name__)
app.config.from_object(Config)
ct_client = ct.ChurchTools(app.config['CT_BASE_URL'])
ct_client.login(username=app.config['USERNAME'], password=app.config['PASSWORD'], remember_me=True)


from app import routes