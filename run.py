import os
from application import create_app
from dotenv import load_dotenv
load_dotenv()

config_name = os.getenv('APP_SETTINGS')

app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
