clients = {}


def store_client(request_id: str):
    clients[request_id] = {"id": request_id, "abort_flag": False}


def get_client(request_id: str):
    return clients.get(request_id)


def set_flag(request_id: str):
    clients[request_id].abort_flag = True


def remove_client(request_id: str):
    if request_id in clients:
        del clients[request_id]
