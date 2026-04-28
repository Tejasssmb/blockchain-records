# Configure the app for deployment
import os
from app import app

# Remove debug mode for production
app.config['DEBUG'] = False

# Allow deployment on different port
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
