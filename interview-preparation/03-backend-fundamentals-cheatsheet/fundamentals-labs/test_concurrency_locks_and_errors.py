"""Runnable code labs for Module 3: Concurrency Locks, Idempotency & Error Handling.

Demonstrates:
1. Optimistic Locking (Compare-and-Swap version counter) to prevent double-selling an item
   when Vinted and Wallapop webhooks arrive simultaneously.
2. Idempotency Guard for Celery `acks_late=True` tasks so re-delivered tasks never duplicate side effects.
3. Token-Bucket Rate Limiter for per-marketplace API quota enforcement.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field


@dataclass
class InventoryRow:
    item_id: int
    status: str = "active"
    quantity: int = 1
    version: int = 1
    sold_on: str | None = None


class OptimisticInventoryStore:
    """Simulates PostgreSQL atomic conditional UPDATE with optimistic locking."""

    def __init__(self) -> None:
        self._rows: dict[int, InventoryRow] = {}
        self._lock = asyncio.Lock()

    def seed(self, row: InventoryRow) -> None:
        self._rows[row.item_id] = row

    async def try_mark_sold(
        self, item_id: int, expected_version: int, marketplace: str
    ) -> bool:
        """Equivalent to:
        UPDATE items SET status='sold', quantity=0, version=version+1, sold_on=:mp
        WHERE id=:id AND status='active' AND quantity >= 1 AND version=:expected_version
        """
        async with self._lock:
            row = self._rows.get(item_id)
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


@dataclass
class IdempotentTaskExecutor:
    """Prevents duplicate marketplace API calls when Celery redelivers an `acks_late` task."""

    completed_keys: dict[str, str] = field(default_factory=dict)
    side_effect_count: int = 0

    def execute_publish(self, idempotency_key: str, sku: str) -> str:
        if idempotency_key in self.completed_keys:
            return self.completed_keys[idempotency_key]

        self.side_effect_count += 1
        external_id = f"ext-{sku}-{self.side_effect_count}"
        self.completed_keys[idempotency_key] = external_id
        return external_id


class TokenBucketRateLimiter:
    """In-memory simulation of a Redis Lua token-bucket rate limiter per marketplace."""

    def __init__(self, capacity: int, refill_rate_per_sec: float) -> None:
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = refill_rate_per_sec
        self.last_refill_timestamp = 0.0

    def allow_request(self, now_sec: float, cost: float = 1.0) -> bool:
        elapsed = max(0.0, now_sec - self.last_refill_timestamp)
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill_timestamp = now_sec

        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


def test_optimistic_locking_prevents_double_sell_under_race() -> None:
    async def _simulate_race() -> None:
        store = OptimisticInventoryStore()
        store.seed(InventoryRow(item_id=42, status="active", quantity=1, version=1))

        # Both workers read version=1 simultaneously and try to claim the item
        vinted_ok, wallapop_ok = await asyncio.gather(
            store.try_mark_sold(42, expected_version=1, marketplace="vinted"),
            store.try_mark_sold(42, expected_version=1, marketplace="wallapop"),
        )
        # Exactly ONE marketplace sale must succeed; the other must be rejected!
        assert (vinted_ok, wallapop_ok) in {(True, False), (False, True)}
        assert store._rows[42].version == 2
        assert store._rows[42].quantity == 0

    asyncio.run(_simulate_race())


def test_idempotent_task_executor_prevents_duplicate_listings() -> None:
    executor = IdempotentTaskExecutor()
    first_id = executor.execute_publish("pub:seller-1:item-99:vinted", sku="JKT-01")
    # Simulate Celery worker crash + Redis visibility_timeout re-delivery of the same task
    second_id = executor.execute_publish("pub:seller-1:item-99:vinted", sku="JKT-01")

    assert first_id == second_id == "ext-JKT-01-1"
    assert executor.side_effect_count == 1


def test_token_bucket_rate_limiter_enforces_quota_and_refills() -> None:
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate_per_sec=1.0)
    assert limiter.allow_request(now_sec=0.0) is True
    assert limiter.allow_request(now_sec=0.0) is True
    assert limiter.allow_request(now_sec=0.0) is False  # Bucket empty!

    # After 1.0 second, 1 token refills
    assert limiter.allow_request(now_sec=1.0) is True
    assert limiter.allow_request(now_sec=1.0) is False
