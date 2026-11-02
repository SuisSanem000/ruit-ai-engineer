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

## 2. WebSockets (`ws://` / `wss://`) & Scaling Real-Time Connections

- **How WebSockets Work:**
  - Starts as a normal HTTP `GET` request with an `Upgrade: websocket` header.
  - The server replies `101 Switching Protocols`, and the TCP connection stays open so both client and server can push messages at any time with almost zero header overhead.
- **3 Important WebSocket Quirks (From Your 60K+ User Socket.IO Experience):**
  - **1. Dead / Half-Open Connections:** If a user loses Wi-Fi, the server might not know the socket died. Always send **Ping / Pong heartbeats** every 25 seconds to close dead sockets.
  - **2. Scaling Across Multiple Servers:** Because WebSockets stay connected to one specific server, if a Celery worker wants to send a message to Seller A, it publishes the message to **Redis Pub/Sub**, and whichever web server holds Seller A's socket forwards it to their browser.
  - **3. Memory Backpressure:** If the server pushes messages faster than a slow phone can read them, the server's memory buffer fills up. Drop or combine old updates if the buffer grows too large.

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
