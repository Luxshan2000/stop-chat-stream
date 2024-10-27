# Chat API: Openai Example

## Overview
This FastAPI application provides a chat interface using OpenAI's models, allowing users to send and receive messages in a streaming manner. Users have the option to stop the generation of responses using three different approaches: In-Memory, Database (PostgreSQL), and Redis.

## Streaming Endpoint
To initiate a chat stream, make a POST request to the `/chat/` endpoint with the required payload. You can abort the streaming by sending a POST request to the `/abort/` endpoint with the `request_id`.

### Example
- **Start Chat**:
  ```http
  POST /chat/
  Content-Type: application/json

  {
      "model": "gpt-3.5-turbo",
      "messages": [{"role": "user", "content": "Hello!"}],
      "request_id": "12345"
  }
  ```

- **Abort Chat**:
  ```http
  POST /abort/
  Content-Type: application/json

  {
      "request_id": "12345"
  }
  ```

## Approaches to Stop Generation

| Feature                     | In-Memory Approach                              | Database Approach (PostgreSQL)         | Redis Approach                         |
|-----------------------------|------------------------------------------------|----------------------------------------|---------------------------------------|
| **Storage Type**            | In-memory (dictionary)                         | Persistent (PostgreSQL database)      | In-memory (Redis)                     |
| **Speed**                   | Fast, as it operates in memory                 | Moderate, depending on database access | Fast, optimized for quick reads/writes |
| **Persistence**             | No, data is lost on restart                    | Yes, retains data across restarts     | Yes, data can persist if configured   |
| **Scalability**             | Limited by memory capacity                      | Scales with database infrastructure    | High, can handle large volumes of data |
| **Abort Signal Check**      | Direct access to client dictionary              | Requires querying the database         | Fast access via key-value pairs       |
| **Implementation Complexity** | Simple to implement                           | Moderate, requires database setup      | Moderate, requires Redis setup        |
| **Use Case Suitability**    | Suitable for lightweight applications           | Suitable for applications needing persistence | Suitable for high-performance applications |

### 1. In-Memory Approach

#### Overview
The In-Memory Approach allows you to manage chat streaming directly within the application memory. This method tracks active clients using a dictionary.

#### Implementation Steps
1. **Store Client**: 
   Uncomment the line in the `/chat/` endpoint:
   ```python
   store_client(request_id=request_id)
   ```

2. **Check Client and Abort**: 
   Uncomment the check in the `generate_response` function:
   ```python
   if clients[request_id]:
       await client.close()
       remove_client(request_id=request_id)
       return
   ```

3. **Abort Request**:
   Uncomment the code in the `/abort/` endpoint:
   ```python
   if request_id in clients:
       set_flag(request_id=request_id)
       return {"message": f"Streaming for request {request_id} will be aborted."}
   ```

### 2. Database Approach (PostgreSQL)

#### Overview
The Database Approach uses a PostgreSQL database to track chat requests and their statuses, providing persistent storage.

#### Implementation Steps
1. **Insert Request in DB**: 
   Uncomment the line in the `/chat/` endpoint:
   ```python
   await insert(session=db, id=request_id, flag=False)
   ```

2. **Check Abort Flag**: 
   Uncomment the code in the `generate_response` function:
   ```python
   abort = await get_by_id(session=db, id=request_id)
   await db.refresh(abort)
   if abort.flag:
       await client.close()
       await delete_by_id(session=db, id=request_id)
       return
   ```

3. **Update Flag on Abort**:
   Uncomment the code in the `/abort/` endpoint:
   ```python
   if await update_flag_by_id(session=db, id=request_id, new_flag=True):
       return {"message": f"Streaming for request {request_id} will be aborted."}
   ```

### 3. Redis Approach

#### Overview
The Redis Approach leverages Redis as an in-memory data store to manage the state of chat requests, providing fast access and scalability.

#### Implementation Steps
1. **Save Abort Signal**: 
   Uncomment the line in the `/chat/` endpoint:
   ```python
   save_abort_signal_to_redis(id=request_id, flag=False, redis_client=rd)
   ```

2. **Check Abort Signal**: 
   Uncomment the code in the `generate_response` function:
   ```python
   abort = get_abort_signal_from_redis(id=request_id, redis_client=rd)
   if abort and abort.flag:
       await client.close()
       delete_abort_signal_from_redis(id=request_id, redis_client=rd)
       return
   ```

3. **Update Abort Signal**: 
   Uncomment the code in the `/abort/` endpoint:
   ```python
   if update_abort_signal_in_redis(id=request_id, flag=True, redis_client=rd):
       return {"message": f"Streaming for request {request_id} will be aborted."}
   ```

## Conclusion
This application provides multiple strategies for managing chat sessions effectively. Choose the approach that best fits your use case based on your application's needs regarding memory, persistence, and speed. Each method allows users to control their chat interactions, enhancing user experience and application responsiveness.