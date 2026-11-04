# HTTP Clients, TLS Fingerprinting & Networking

> **From Luis's Email Cheat Sheet:** *"http clients and tls ... some low level networking and difrerent protocols (http, ws, etc.) and their peculiarities"*

---

## 1. HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC)

- **HTTP/1.1 (Over TCP):**
  - Sends text headers and handles **only 1 request at a time** per TCP connection (`keep-alive` reuses the connection one after another).
  - **Quirk:** If Request 1 is slow, Requests 2 and 3 must wait behind it (or the browser must open 6 separate TCP connections).
- **HTTP/2 (Over TCP):**
  - Uses binary frames, compresses headers (`HPACK`), and sends **many requests at the same time (multiplexing)** over **1 single TCP connection**.
  - **Quirk (TCP Head-of-Line Blocking):** Even though 50 requests share 1 TCP connection, the operating system treats TCP as one single ordered line of bytes. If **1 single TCP packet is lost on the network**, the OS pauses **all 50 requests** until that 1 packet is resent!
- **HTTP/3 (Over QUIC / UDP):**
  - Runs over **UDP** instead of TCP, with TLS 1.3 built directly into the connection handshake (faster startup).
  - **Main Benefit:** Each stream is independent—if 1 UDP packet is lost, **only that 1 request waits**, while the other 49 requests keep moving without delay!

---

## 2. Real-Time Protocols & Their Peculiarities (WebSockets vs SSE vs Long Polling vs Webhooks)

- **HTTP Long Polling:**
  - Client makes an HTTP request; server holds it open until new data arrives, responds, closes the socket, and client immediately reconnects.
  - *Peculiarity:* High header and connection overhead, but works through strict corporate proxies that block WebSockets.
- **Server-Sent Events (SSE / `text/event-stream`):**
  - A single long-lived standard HTTP connection where the server pushes text events one-way to the client.
  - *Peculiarities:* Runs over normal HTTP/1.1 or HTTP/2, gets automatic reconnection in browsers for free, and is ideal for one-way streaming (like LLM token streaming or live inventory sync updates). It cannot push from client to server on the same stream.
- **WebSockets (`ws://` / `wss://`):**
  - Upgrades an HTTP connection (`101 Switching Protocols`) into a persistent, bidirectional, full-duplex TCP socket.
  - *3 Important WebSocket Quirks (From Your 60K+ Socket.IO Experience):*
    - **1. Half-Open Sockets:** Always send **Ping / Pong heartbeats** every 25 seconds to drop dead Wi-Fi connections.
    - **2. Multi-Server Scaling:** WebSockets are stateful; scale across Django nodes using **Redis Pub/Sub** to route messages to the node holding the user's socket.
    - **3. Memory Buffers:** If a slow client cannot consume messages as fast as they arrive, the server must drop old updates or apply backpressure.
- **Webhooks (Server-to-Server Push):**
  - The marketplace server calls Ruit's API via `POST` when an event occurs (e.g. item sold).
  - *Peculiarities:* Must verify HMAC signatures (`X-Hub-Signature`) to prevent attackers from sending fake sales, and return `200 OK` within 2 seconds while offloading processing to Celery.

---

## 3. HTTP Clients & Connection Pooling in Python

- **Always Reuse a Session (`httpx.AsyncClient` or `requests.Session`):**
  - Calling `requests.get()` or `httpx.get()` directly opens a brand-new TCP connection and runs a full TLS handshake every single time (wasting 100–300ms per call).
  - Reusing a client session keeps warm connections open in a **connection pool**.
- **Always Set Explicit Timeouts:**
  - In Python's `requests` library, the default timeout is `None`—meaning if a marketplace hangs, your worker freezes forever! Always set clear `connect` and `read` timeouts (e.g., 3s to connect, 10s to read).

---

## 4. TLS Fingerprinting (JA3 / JA4) & Anti-Bot Protection

- **Why Python HTTP Clients Get Blocked (`403 Forbidden`) Even with Chrome Headers:**
  - Marketplaces like Vinted, Wallapop, and Depop use **Cloudflare** or **DataDome**.
  - When a client connects over HTTPS, the very first packet (`TLS ClientHello`) lists supported encryption ciphers and extensions in a specific order.
  - Anti-bot systems hash this list into a **JA3 / JA4 TLS Fingerprint** (and also check the **HTTP/2 SETTINGS frame**).
  - Real Chrome uses Google's **BoringSSL** library, while standard Python (`requests`/`httpx`) uses **OpenSSL**. Cloudflare sees `User-Agent: Chrome` in the header, sees `OpenSSL` in the TLS handshake, and blocks the request as a bot!
- **How to Fix It in Python (`curl_cffi`):**
  - Use the **`curl_cffi`** library (built on `curl-impersonate`), which uses Chrome's exact BoringSSL handshake and HTTP/2 settings so the request looks identical to a real Chrome browser on the wire.
