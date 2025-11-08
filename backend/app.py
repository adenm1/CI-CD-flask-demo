"""Application entry point."""
import os
from api import create_app

# Get environment from ENV variable
environment = os.getenv("FLASK_ENV", "production")

# Create application instance
app = create_app(environment)

if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "0.0.0.0"),
        port=app.config.get("PORT", 8000),
        debug=app.config.get("DEBUG", False)
    )
