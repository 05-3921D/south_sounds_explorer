import uvicorn
import sys
import os

# Add the backend directory to sys.path so 'app' can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
