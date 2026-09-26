import uvicorn

def start():
    print("Srating server...")
    uvicorn.run(
        "presentation.webapilibreria:app",
        host="localhost",
        port=7000,
        reload=True
    )

    print("Server is running.")

def main():
    return "__main__"

if __name__ == "__main__":
    start()
