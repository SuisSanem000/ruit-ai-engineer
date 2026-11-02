# Background Queues & Brokers: Celery, Redis & RabbitMQ

> **Code examples with detailed comments:** [test_concurrency_locks_and_errors.py](./fundamentals-labs/test_concurrency_locks_and_errors.py)

---

## 1. Why Ruit Needs Background Queues (Celery)

- When a seller publishes an item to 6 marketplaces or an item sells on Vinted, Ruit cannot make 6 external API calls inside the user's HTTP request:
  - Marketplace APIs are slow (1–10 seconds) and often fail with `429` or `503`.
  - Waiting inside the HTTP request would make the web app feel frozen and block web servers.
- **How Celery Works:**
  1. **Producer (Django Web Server):** Saves the change in PostgreSQL and pushes a small job message (with the `item_id`) into a **Broker (Redis or RabbitMQ)**.
  2. **Broker (Redis / RabbitMQ):** Holds the queue of waiting job messages.
  3. **Consumer (Celery Worker Processes):** Separate Python background processes that pick up jobs from the broker, call the marketplace APIs, and retry if needed.

---

## 2. Redis vs RabbitMQ as a Celery Broker

- **Redis as a Broker:**
  - **Pros:** Very simple to run because you already use Redis for caching and rate limiting.
  - **Main Quirk (`visibility_timeout`):** Redis does not have true per-connection message locks like RabbitMQ. If a Celery task takes longer than `visibility_timeout` (default 1 hour), Redis assumes the worker died and **gives the same task to a second worker**—running it twice!
- **RabbitMQ as a Broker:**
  - **Pros:** A real message broker (AMQP) with flexible message routing, strong disk durability, and true consumer acknowledgments (`ACK`/`NACK`) tied to the worker's open connection.
  - **Cons:** Extra service to manage and monitor.

---

## 3. 7 Key Rules for Reliable Celery Queues

- **1. Queue Tasks Only After the Database Transaction Commits (`transaction.on_commit`):**
  - If you send a Celery task *inside* an open database transaction, Redis is so fast that the Celery worker can wake up and query PostgreSQL *before* the transaction finishes committing—reading old data or `None`!
  - Always use `transaction.on_commit()` so the task is sent to Redis only after PostgreSQL saves the row.
- **2. Pass Only IDs (`item_id`), Never Full Database Objects:**
  - Passing a full object wastes Redis memory, and the data might already be outdated by the time the worker runs the task. Pass `item_id` and fetch fresh data from PostgreSQL inside the worker.
- **3. Turn On Late Acknowledgment (`acks_late=True`):**
  - By default, Celery deletes the message from the queue *before* running the task. If the server restarts mid-task, the job is lost.
  - `acks_late=True` tells Celery to delete the message from the queue **only after** the task finishes.
- **4. Make Every Task Idempotent (Safe to Run Twice):**
  - Because `acks_late=True` means a task can run a second time after a crash, check the database status (or use an idempotency key in Redis) before calling the marketplace API so you never post duplicate listings.
- **5. Use Exponential Backoff + Random Jitter on Retries:**
  - Wait longer between each retry (`2s`, `4s`, `8s`, `16s`) and add a small random delay (**jitter**) so 500 failed jobs do not retry at the exact same second.
- **6. Separate Queues by Priority:**
  - Never put all jobs in one single queue. If a seller uploads 20,000 items, an urgent **"Item Sold $\rightarrow$ Delist Now"** job would get stuck behind 20,000 slow jobs!
  - Create separate queues: `q_critical_delist` (runs in seconds), `q_catalog_sync` (normal speed), and `q_browser_workers` (heavy Playwright jobs).
- **7. Dead Letter Queue (DLQ) & Timeouts:**
  - Set task time limits (`soft_time_limit` and `time_limit`) so hung requests never block workers forever, and move tasks that fail all retries into a **Dead Letter Queue** for engineers to inspect.
