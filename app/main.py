from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# After creating the app, add static file serving
# Create a 'static' folder in your app directory and put the HTML file there

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def serve_dashboard():
    """Serve the beautiful dashboard"""
    return FileResponse("app/static/index.html")