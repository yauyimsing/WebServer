
def application(env, start_response):
    status = "404 Not Found"
    headers = []
    start_response(status, headers)
    return "hello kugou from sayhello.py"
