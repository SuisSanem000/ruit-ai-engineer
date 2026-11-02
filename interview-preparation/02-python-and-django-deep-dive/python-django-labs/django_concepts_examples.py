"""
Basic Django & Python Concept Examples (With Clear Explanatory Comments)

Note: This file shows what basic Django ORM and Python patterns look like
so you can read and recognize them easily during your interview.
"""

from __future__ import annotations

# =====================================================================
# 1. CLASSIC PYTHON GOTCHA: MUTABLE DEFAULT ARGUMENTS
# =====================================================================


# BAD WAY (Never do this in Python!):
# def add_tag_bad(tag: str, tags: List[str] = []) -> List[str]:
#     tags.append(tag)
#     return tags
# Why it is bad: Python creates the default `[]` list only ONCE when the file loads.
# Every time you call `add_tag_bad("new")`, it keeps adding to the OLD list from previous calls!


# GOOD WAY: Use `None` as the default, and create a new list inside the function.
def add_tag_safe(tag: str, tags: list[str] | None = None) -> list[str]:
    if tags is None:
        result_list: list[str] = []
    else:
        # Copy the list so we do not mutate the caller's original list
        result_list = list(tags)

    result_list.append(tag)
    return result_list


# =====================================================================
# 2. HOW DJANGO ORM QUERIES WORK (REFERENCE EXAMPLES)
# Below are commented examples of how Django ORM looks in a real project.
# =====================================================================


def explain_django_orm_patterns() -> dict:
    """Returns a dictionary summarizing the 4 most important Django ORM patterns
    and explains the exact SQL they generate in the comments below.
    """

    # -----------------------------------------------------------------
    # PATTERN A: `select_related` (For single ForeignKey / 1-to-1)
    # -----------------------------------------------------------------
    # Problem (N+1 queries):
    #   items = Item.objects.all()
    #   for item in items:
    #       print(item.seller.name)  # Runs 1 extra SQL query per item!
    #
    # Fix with `select_related`:
    #   items = Item.objects.select_related("seller").all()
    #   # Generates 1 single SQL query using `INNER JOIN / LEFT JOIN sellers`!

    # -----------------------------------------------------------------
    # PATTERN B: `prefetch_related` (For Many-to-Many or 1-to-Many lists)
    # -----------------------------------------------------------------
    # If one Item has MANY MarketplaceListings (Wallapop, Vinted, eBay):
    #   items = Item.objects.prefetch_related("marketplace_listings").all()
    #   # Runs 2 separate SQL queries:
    #   #   Query 1: SELECT * FROM items;
    #   #   Query 2: SELECT * FROM marketplace_listings WHERE item_id IN (1, 2, 3...);
    #   # Then Django connects them in Python memory!

    # -----------------------------------------------------------------
    # PATTERN C: Locking a Row to Prevent Double-Sells (`select_for_update`)
    # -----------------------------------------------------------------
    # When an item sells on Vinted, we lock the row inside a transaction
    # so another worker cannot sell it at the same time:
    #
    #   from django.db import transaction
    #
    #   with transaction.atomic():
    #       item = (
    #           Item.objects.select_for_update(nowait=True)
    #           .filter(id=item_id, status="active")
    #           .first()
    #       )
    #       if item is not None:
    #           item.status = "sold"
    #           # Always pass `update_fields` so Django only updates changed columns!
    #           item.save(update_fields=["status"])
    #
    #           # IMPORTANT: Only send the Celery background job AFTER Postgres commits!
    #           transaction.on_commit(lambda: delist_other_marketplaces.delay(item.id))

    # -----------------------------------------------------------------
    # PATTERN D: Streaming Large Tables Without Running Out of RAM (`.iterator()`)
    # -----------------------------------------------------------------
    # Bad for 100,000 rows (loads everything into RAM):
    #   for item in Item.objects.all(): ...
    #
    # Good for 100,000 rows (streams in chunks of 2,000 rows):
    #   for item in Item.objects.iterator(chunk_size=2000): ...

    return {
        "single_foreign_key": "select_related (1 query with SQL JOIN)",
        "many_to_many_or_reverse_list": "prefetch_related (2 queries joined in Python)",
        "row_lock": "select_for_update inside transaction.atomic()",
        "celery_after_commit": "transaction.on_commit()",
        "large_queryset_streaming": ".iterator(chunk_size=2000)",
    }
