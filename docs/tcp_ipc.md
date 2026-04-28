TCP IPC (TCP Queue) guide

This project includes a lightweight TCP-based IPC mechanism for pushing payloads into in-process queues.

Server: `src/voice/infrastructure/tcp_queue.py`
CLI: `python -m voice.cli.send_tcp`

Protocol
- Connect to the TCP server
- Send a single line with the queue name (utf-8) terminated by LF
- Send raw payload bytes until connection close

Example (send a short text payload):

```bash
echo -n "hello ipc" | python -m voice.cli.send_tcp --port 8800 --queue my-queue
```

Example (send a file):

```bash
python -m voice.cli.send_tcp --port 8800 --queue audio --file /path/to/file.raw
```

The server will create the queue in `QueueManager` if it does not exist and place the payload there.
