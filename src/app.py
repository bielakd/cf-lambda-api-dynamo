def handler(context, event):
    print("Starting Execution")
    print(event)
    return {
        "Hello": "World",
        "isBase64Encoded": False
    }