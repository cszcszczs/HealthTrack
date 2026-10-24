import uvicorn

def start():
    print("Starting HealthTrack server...")
    uvicorn.run(
        "presentation.webapipatient:app",
        host="localhost",
        port=7000,
        reload=True
    )

    print("HealthTrack server is running.")

def main():
    return "__main__"

if __name__ == "__main__":
    start()
