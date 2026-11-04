# 00 — Low-Level Networking: TCP, UDP, DNS & HTTP Protocol Fundamentals

> **Direct Match to Luis's Email Cheat Sheet:**  
> *"some low level networking and difrerent protocols (http, ws, etc.) and their peculiarities ... http clients and tls"*

---

## 1. The Core Networking Mental Model (OSI & TCP/IP Layers)

- **Layer 7 — Application Layer (HTTP, WebSocket, DNS, SSH):**
  - Where our Python code, browsers, and marketplace APIs live. Deals with messages, headers, and JSON.
- **Layer 4 — Transport Layer (TCP, UDP):**
  - Moves data between ports on two machines. Deals with packets, ports, acknowledgments, and connection state.
- **Layer 3 — Network Layer (IP):**
  - Routes packets between IP addresses across the internet.
- **The Golden Rule for Integration Engineers:**
  - An HTTP error (`401`, `429`, `500`) is an **Application-layer response** (the server received your request and replied).
  - A connection timeout, connection refused, or TLS reset is a **Transport-layer failure** (the network or server dropped before HTTP started).

---

## 2. TCP vs. UDP: Definitions & Peculiarities

- **TCP (Transmission Control Protocol):**
  - **Connection-Oriented & Reliable:** Guarantees that every byte arrives in the exact order it was sent, with zero loss.
  - **The 3-Way Handshake (Starting a Connection):**
    1. **SYN:** Client sends: *"Can we talk? Here is my initial sequence number."*
    2. **SYN-ACK:** Server replies: *"Yes, I hear you. Here is my sequence number."*
    3. **ACK:** Client confirms: *"Got it, let's start sending data."*
    - *Cost:* Adds 1 full network round-trip time (RTT) before any data can be sent.
  - **The 4-Way Teardown & `TIME_WAIT` Socket Exhaustion:**
    - When a TCP connection closes (`FIN` $\rightarrow$ `ACK` $\rightarrow$ `FIN` $\rightarrow$ `ACK`), the OS kernel keeps the local socket in a **`TIME_WAIT`** state for 60 seconds to catch delayed packets.
    - *The Danger:* If your integration script opens and closes 500 new HTTP connections every second instead of reusing a connection pool, you exhaust all local ephemeral ports (error: `Can't assign requested address`).
  - **Flow Control & Congestion Control:**
    - TCP uses a **Sliding Window** and **Slow Start** algorithm so a fast server does not overwhelm a slow network or receiver.
- **UDP (User Datagram Protocol):**
  - **Connectionless & Fire-and-Forget:** No handshake, no acknowledgments, no ordering, and no retransmissions.
  - **Why It Matters:** Used for DNS lookups, video streaming, and modern **HTTP/3 (QUIC)** to avoid TCP head-of-line blocking.

---

## 3. How DNS Resolution Works (And Why It Matters for Integrations)

- **The Step-by-Step Resolution Path:**
  1. **Browser / App Cache:** Checks if the IP for `api.vinted.com` was resolved recently.
  2. **OS Resolver Cache:** Checks the local operating system's DNS cache.
  3. **Recursive DNS Resolver (e.g., 1.1.1.1 or 8.8.8.8):** Queries on behalf of the client.
  4. **Root Nameserver (`.`):** Points to the `.com` TLD nameserver.
  5. **TLD Nameserver (`.com`):** Points to Vinted's Authoritative Nameserver (e.g., Cloudflare DNS).
  6. **Authoritative Nameserver:** Returns the exact IP address and a **TTL (Time to Live)** in seconds.
- **Integration Peculiarity:**
  - If your Celery worker makes a fresh DNS lookup for every single marketplace API call, you add 20–100ms of latency per call.
  - Reusing an `httpx.AsyncClient` or `requests.Session` caches the DNS resolution in the connection pool.

---

## 4. HTTP Protocol Anatomy, Idempotency & Safety

- **Anatomy of an HTTP Request:**
  - **Request Line:** Method (`GET`, `POST`), Path (`/api/v2/items`), Protocol (`HTTP/1.1`).
  - **Headers:** Key-value pairs (`User-Agent`, `Authorization`, `Content-Type`, `Accept-Encoding`).
  - **Body:** The raw payload (JSON, form data, multipart images).
- **HTTP Method Semantics (Crucial for Marketplace Design):**
  - **Safe Methods (`GET`, `HEAD`):** Read-only operations. Calling them never modifies state on the server.
  - **Idempotent Methods (`GET`, `PUT`, `DELETE`):**
    - Making the same request 1 time or 10 times produces the exact same end state.
    - *Example:* `DELETE /listings/123` is idempotent. If it is already deleted, the end state is still "deleted" (the server should return `200` or `404`, but not fail).
  - **Non-Idempotent Methods (`POST`, `PATCH`):**
    - Calling `POST /listings/create` twice creates **two duplicate listings**.
    - *Fix:* Always send an **Idempotency Key** (`Idempotency-Key: <unique-uuid>`) in the header so the marketplace knows to ignore the second request if a network timeout occurs.

---

## 5. The Integration Status Codes Cheat Sheet

- **2xx (Success):**
  - `200 OK`: Standard success with body.
  - `201 Created`: Resource created successfully (e.g., new listing published).
  - `204 No Content`: Action succeeded with no body returned (common on `DELETE` or `UPDATE`).
- **3xx (Redirections):**
  - `301 Moved Permanently`: Browser/client caches the new URL permanently.
  - `307 Temporary Redirect` & `308 Permanent Redirect`: Preserves the HTTP method and request body (unlike old `301`/`302` which browsers historically turned into `GET`).
- **4xx (Client / Integration Errors):**
  - `400 Bad Request`: Payload violates the marketplace's schema.
  - `401 Unauthorized`: Authentication token is missing, expired, or invalid $\rightarrow$ **Never retry automatically; alert the seller to reconnect**.
  - `403 Forbidden`: Token is valid, but the user lacks permissions OR **Cloudflare/DataDome bot protection detected Python and blocked the request**.
  - `404 Not Found`: Listing does not exist $\rightarrow$ **In delist workers, treat `404` as success (already delisted)**.
  - `409 Conflict`: Race condition (e.g., item already sold or version mismatch).
  - `422 Unprocessable Entity`: Valid JSON syntax, but semantic validation failed (e.g., negative price).
  - `429 Too Many Requests`: Rate limit hit $\rightarrow$ **Read the `Retry-After` header and back off with jitter**.
- **5xx (Server / Upstream Errors):**
  - `500 Internal Server Error`: Marketplace server crashed $\rightarrow$ Retry with exponential backoff.
  - `502 Bad Gateway`: Upstream reverse proxy (Nginx/Cloudflare) received an invalid response from the backend application (e.g., Django crashed).
  - `503 Service Unavailable`: Marketplace is down for maintenance $\rightarrow$ Pause integration queue.
  - `504 Gateway Timeout`: The marketplace backend took too long to reply to Cloudflare/Nginx.

