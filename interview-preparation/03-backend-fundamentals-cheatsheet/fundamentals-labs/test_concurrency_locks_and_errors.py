"""Basic Python Practice Examples for Module 3 (Locks, Idempotency, Rate Limits & Result Pattern).

WHAT THIS FILE DOES:
Shows simple, easy-to-read Python code for 4 key backend concepts from Luis's cheat sheet:
1. Optimistic Locking (version check) so two simultaneous webhooks cannot double-sell the same item.
2. Idempotency Guard so if a Celery background task runs twice, it never creates duplicate listings.
3. Token-Bucket Rate Limiter to stay under a marketplace's API speed limit.
4. Rust/Go-style explicit `Result` object in Python so errors are returned as clear values.

Run in terminal:
    .venv/bin/pytest interview-preparation/03-backend-fundamentals-cheatsheet/fundamentals-labs/ -v
"""

from __future__ import annotations

import asyncio

# ============================================================================
# 1. Optimistic Locking to Prevent Double-Selling
# ============================================================================


class InventoryRow:
    """Represents a single product row in our database."""

    def __init__(
        self,
        item_id: int,
        status: str = "active",
        quantity: int = 1,
        version: int = 1,
        sold_on: str | None = None,
    ) -> None:
        self.item_id = item_id
        self.status = status
        self.quantity = quantity
        self.version = version
        self.sold_on = sold_on


class OptimisticInventoryStore:
    """Simulates a PostgreSQL atomic UPDATE using a `version` column:

    SQL equivalent:
        UPDATE items
        SET status = 'sold', quantity = 0, version = version + 1, sold_on = :marketplace
        WHERE id = :item_id AND status = 'active' AND quantity >= 1 AND version = :expected_version;

    If two workers read `version = 1` at the same time and both try to update,
    the first worker changes `version` to `2` and succeeds (`True`).
    The second worker checks `version == 1`, sees it is now `2`, and fails (`False`)!
    """

    def __init__(self) -> None:
        self.rows: dict[int, InventoryRow] = {}
        self.lock = asyncio.Lock()

    def seed(self, row: InventoryRow) -> None:
        self.rows[row.item_id] = row

    async def try_mark_sold(
        self, item_id: int, expected_version: int, marketplace: str
    ) -> bool:
        async with self.lock:
            row = self.rows.get(item_id)
            if (
                row is None
                or row.status != "active"
                or row.quantity < 1
                or row.version != expected_version
            ):
                return False

            row.status = "sold"
            row.quantity = 0
            row.version += 1
            row.sold_on = marketplace
            return True


# ============================================================================
# 2. Idempotency Guard for Background Tasks (Celery)
# ============================================================================


class IdempotentTaskExecutor:
    """In Celery with `acks_late=True`, if a worker crashes right after publishing
    an item to Vinted, Redis will hand the task to another worker to run again.

    By checking a unique `idempotency_key` before calling the external API,
    we return the saved result instead of creating a duplicate listing!
    """

    def __init__(self) -> None:
        self.completed_keys: dict[str, str] = {}
        self.api_call_count: int = 0

    def execute_publish(self, idempotency_key: str, sku: str) -> str:
        # 1. If we already finished this exact job, return the existing ID immediately
        if idempotency_key in self.completed_keys:
            return self.completed_keys[idempotency_key]

        # 2. Otherwise, call the marketplace API once and save the result
        self.api_call_count += 1
        external_listing_id = f"ext-{sku}-{self.api_call_count}"
        self.completed_keys[idempotency_key] = external_listing_id
        return external_listing_id


# ============================================================================
# 3. Token-Bucket Rate Limiter
# ============================================================================


class TokenBucketRateLimiter:
    """Simple rate limiter (in production, this runs as a short Lua script in Redis).
    - Holds up to `capacity` tokens.
    - Refills `refill_rate_per_sec` tokens every second.
    - Each API request costs 1 token. If 0 tokens are left, the request must wait!
    """

    def __init__(self, capacity: int, refill_rate_per_sec: float) -> None:
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = refill_rate_per_sec
        self.last_refill_time = 0.0

    def allow_request(self, current_time_sec: float) -> bool:
        elapsed = max(0.0, current_time_sec - self.last_refill_time)
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill_time = current_time_sec

        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


# ============================================================================
# 4. Rust/Go-Style Explicit `Result` Object in Basic Python
# ============================================================================


class SyncResult:
    """Instead of throwing hidden exceptions, this simple class returns success
    or error as an explicit value (similar to Go's `(val, err)` or Rust's `Result<T, E>`).
    """

    def __init__(
        self,
        is_ok: bool,
        value: str | None = None,
        error_code: str | None = None,
    ) -> None:
        self.is_ok = is_ok
        self.value = value
        self.error_code = error_code


def parse_price_cents_safely(raw_price: str) -> SyncResult:
    """Parses a price string into integer cents without raising unhandled exceptions."""
    cleaned = raw_price.replace("€", "").strip()
    if not cleaned:
        return SyncResult(is_ok=False, error_code="EMPTY_PRICE")

    try:
        cents = int(float(cleaned) * 100)
    except ValueError:
        return SyncResult(is_ok=False, error_code="INVALID_NUMBER")

    if cents <= 0:
        return SyncResult(is_ok=False, error_code="NON_POSITIVE_PRICE")

    return SyncResult(is_ok=True, value=str(cents))


# ============================================================================
# Pytest Tests
# ============================================================================


def test_optimistic_locking_stops_double_sell() -> None:
    async def run_race() -> None:
        store = OptimisticInventoryStore()
        store.seed(InventoryRow(item_id=42, status="active", quantity=1, version=1))

        # Vinted and Wallapop webhooks arrive at the same time, both seeing version=1
        vinted_ok, wallapop_ok = await asyncio.gather(
            store.try_mark_sold(42, expected_version=1, marketplace="vinted"),
            store.try_mark_sold(42, expected_version=1, marketplace="wallapop"),
        )

        # Only ONE can succeed; the other must return False!
        assert (vinted_ok, wallapop_ok) in {(True, False), (False, True)}
        assert store.rows[42].version == 2
        assert store.rows[42].quantity == 0

    asyncio.run(run_race())


def test_idempotency_guard_runs_api_call_only_once() -> None:
    executor = IdempotentTaskExecutor()

    first_id = executor.execute_publish("pub:seller-1:item-99:vinted", sku="JKT-01")
    second_id = executor.execute_publish("pub:seller-1:item-99:vinted", sku="JKT-01")

    assert first_id == second_id == "ext-JKT-01-1"
    assert executor.api_call_count == 1


def test_token_bucket_rate_limiter() -> None:
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate_per_sec=1.0)

    assert limiter.allow_request(current_time_sec=0.0) is True
    assert limiter.allow_request(current_time_sec=0.0) is True
    assert limiter.allow_request(current_time_sec=0.0) is False  # Out of tokens!

    # 1 second later, 1 token has refilled
    assert limiter.allow_request(current_time_sec=1.0) is True
    assert limiter.allow_request(current_time_sec=1.0) is False


def test_rust_go_style_sync_result() -> None:
    ok_res = parse_price_cents_safely("25.50 €")
    assert ok_res.is_ok is True
    assert ok_res.value == "2550"

    err_res = parse_price_cents_safely("free")
    assert err_res.is_ok is False
    assert err_res.error_code == "INVALID_NUMBER"
