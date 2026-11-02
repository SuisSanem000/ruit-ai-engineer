# HTTP Clients, TLS Fingerprinting & Low-Level Networking

> **Luis's Cheat Sheet Topic:** *"http clients and tls ... some low level networking and difrerent protocols (http, ws, etc.) and their peculiarities"*

---

## 1. Low-Level Networking & Protocols: Peculiarities & Tradeoffs

### 1.1 TCP vs UDP & The Evolution of HTTP (HTTP/1.1 $\rightarrow$ HTTP/2 $\rightarrow$ HTTP/3)

| Protocol | Transport | Key Mechanism | The "Peculiarity" / Bottleneck to Mention in the Interview |
| :--- | :--- | :--- | :--- |
| **HTTP/1.1** | TCP | Text-based headers, `Connection: keep-alive` (reuses TCP socket sequentially). | **Application-Level Head-of-Line (HoL) Blocking:** Only 1 request/response can be in flight on a single TCP connection at a time. Browsers open up to 6 parallel TCP connections per domain to work around this. |
| **HTTP/2** | TCP (+ TLS via ALPN `h2`) | **Binary framing**, **multiplexed streams** over a single TCP connection, **HPACK** header compression (static + dynamic lookup tables). | **Transport-Level (TCP) Head-of-Line Blocking:** Even though 100 HTTP/2 streams share 1 TCP connection, the OS kernel treats TCP as a single ordered byte stream. If **1 single TCP packet is dropped**, the OS kernel holds up **all 100 HTTP/2 streams** until that 1 lost packet is retransmitted! |
| **HTTP/3 (QUIC)** | **UDP** (+ built-in TLS 1.3) | Multiplexed streams implemented inside **QUIC over UDP** in user space; `0-RTT` / `1-RTT` combined connection + TLS handshake; **QPACK** headers. | **Zero Head-of-Line Blocking & Connection Migration:** Because QUIC manages streams independently over UDP, a lost UDP packet only stalls the *single stream* that owned that packet! Plus, **Connection IDs** allow a mobile phone switching from Wi-Fi to 5G to keep the connection alive without re-handshaking. |

### 1.2 WebSockets (`ws://` / `wss://`) vs SSE vs Webhooks
You scaled **Socket.IO / WebSockets to 60K+ concurrent users** at Parsaiane—use that real experience here!
- **How the WebSocket Handshake Works:**
  1. Starts as a standard HTTP/1.1 `GET` request with headers:
     `Connection: Upgrade`, `Upgrade: websocket`, `Sec-WebSocket-Key: <base64-nonce>`, `Sec-WebSocket-Version: 13`.
  2. Server hashes the key with the magic GUID, responds `HTTP/1.1 101 Switching Protocols`, and the underlying TCP socket converts into a **persistent, full-duplex binary/text frame channel** (minimal 2–14 byte framing overhead, no HTTP headers per message!).
- **Peculiarities of WebSockets in Production:**
  1. **Half-Open / Zombie Connections:** If a client loses Wi-Fi without sending a TCP `FIN`/`RST`, the server doesn't know the socket is dead until it tries to write. You **must** implement application-level **Ping (`0x9`) / Pong (`0xA`) heartbeats** (e.g., every 25s) to reap dead connections.
  2. **Horizontal Scaling across Multiple Servers:** Because WebSockets are **stateful** (Seller A is connected to Worker 1, Seller B to Worker 2), any backend Celery worker pushing a real-time sync notification must publish to **Redis Pub/Sub (or Django Channels Layer)** so whichever ASGI worker holds Seller A's socket can forward the frame.
  3. **Backpressure:** If the server pushes messages faster than a slow client reads them, the send buffer grows in RAM until OOM—monitor socket write buffer size (`transport.get_write_buffer_size()`) and drop/coalesce stale updates.

---

## 2. Python HTTP Clients (`httpx`, `aiohttp`, `requests`, `curl_cffi`)

### 2.1 The Golden Rules of HTTP Clients in Production
1. **Always Reuse Connection Pools (`httpx.AsyncClient` / `requests.Session`):**
   - Calling `httpx.get(url)` or `requests.get(url)` directly performs: DNS lookup $\rightarrow$ TCP 3-way handshake (`SYN`, `SYN-ACK`, `ACK`) $\rightarrow$ TLS handshake $\rightarrow$ HTTP request $\rightarrow$ Socket close (`FIN`). That wastes **100–300ms per call** and exhausts ephemeral ports (`TIME_WAIT` exhaustion)!
   - Reusing a single `httpx.AsyncClient(http2=True, limits=httpx.Limits(max_connections=100, max_keepalive_connections=20))` keeps warm TCP+TLS sockets open in the pool.
2. **Granular Timeouts:**
   - Never use a single vague timeout (or `requests`'s default `timeout=None` which hangs forever!).
   - Configure explicit phases: `httpx.Timeout(timeout=15.0, connect=3.0, read=10.0, write=5.0, pool=2.0)`.

---

## 3. TLS Handshake & Anti-Bot TLS Fingerprinting (JA3 / JA4 & HTTP/2)

**Why This Is a Game-Changer Topic at Ruit:**  
Marketplaces like **Vinted**, **Wallapop**, **Depop**, and **Vestiaire Collective** sit behind **Cloudflare**, **DataDome**, or **PerimeterX**. Even if you copy the exact `User-Agent: Mozilla/5.0 ... Chrome/130.0` header and cookies from Chrome DevTools into Python `requests` or `httpx`, **Cloudflare still blocks you immediately with HTTP `403 Forbidden`!** Why?

### 3.1 How TLS Fingerprinting (JA3 / JA4) Exposes Python Bots
During the very first step of a TLS 1.2 / 1.3 handshake, the client sends an unencrypted **`ClientHello`** packet to the server containing:
1. TLS Version supported.
2. Exact ordered list of **Cipher Suites**.
3. Exact ordered list of **TLS Extensions** (SNI, ALPN, Supported Groups/Curves, Signature Algorithms, Key Share, GREASE values).
4. Elliptic curve formats.

**JA3 / JA4** concatenates and hashes these fields into a fingerprint string:
- **Real Chrome Browser:** Uses Google's **BoringSSL**, sends specific cipher orders, randomizes extension order (in modern Chrome), and injects **GREASE** (Generate Random Extensions And Sustain Extensibility) values.
- **Python (`requests` / `httpx` / `urllib3`):** Uses the OS's **OpenSSL** library with a completely different cipher suite list, different TLS extension order, and **zero GREASE values**.
- **The Mismatch:** Cloudflare sees `User-Agent: Chrome/130` in the HTTP header, but sees `JA3/JA4 = Python OpenSSL` in the TLS handshake $\rightarrow$ **Instant Bot Block!**

### 3.2 HTTP/2 Frame Fingerprinting (Akamai Fingerprint)
Even after passing TLS, when establishing an HTTP/2 connection, the client immediately sends a **`SETTINGS` frame** (`HEADER_TABLE_SIZE`, `ENABLE_PUSH`, `MAX_CONCURRENT_STREAMS`, `INITIAL_WINDOW_SIZE`) and `WINDOW_UPDATE` / pseudo-header order (`:method`, `:authority`, `:scheme`, `:path` in Chrome vs `:method`, `:path`, `:authority`, `:scheme` in other clients). Anti-bot WAFs fingerprint this too!

### 3.3 The Solution in Python: `curl_cffi` & TLS-Impersonating Clients
How do you make fast, browserless HTTP calls in Python without getting blocked by JA3/JA4 or HTTP/2 fingerprinting?
- Use **`curl_cffi`** (Python bindings for `curl-impersonate`, which compiles `libcurl` against Chrome's **BoringSSL** and patches the HTTP/2 `SETTINGS` and header order to match real Chrome/Safari byte-for-byte!):
```python
from curl_cffi.requests import AsyncSession

async def fetch_protected_marketplace_page(url: str, proxy_url: str) -> dict:
    # Impersonates Chrome's exact TLS ClientHello (JA3/JA4) and HTTP/2 SETTINGS frame!
    async with AsyncSession(impersonate="chrome124", proxy=proxy_url, timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()
```
> **Drop this insight during Interview 1:** Explaining **JA3/JA4 TLS fingerprinting + HTTP/2 `SETTINGS` pseudo-header order + `curl_cffi` (`curl-impersonate`)** instantly signals to Luis and the team that you deeply understand real-world marketplace reverse engineering.

