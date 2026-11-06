export interface InventorySnapshot {
  sku: string;
  availableQty: number;
  version: number;
}

export function canFulfillOrder(
  snapshot: InventorySnapshot,
  requestedQty: number,
  expectedVersion: number
): { allowed: boolean; nextVersion: number; reason?: string } {
  if (snapshot.version !== expectedVersion) {
    return { allowed: false, nextVersion: snapshot.version, reason: 'VERSION_CONFLICT' };
  }
  if (requestedQty <= 0 || snapshot.availableQty < requestedQty) {
    return { allowed: false, nextVersion: snapshot.version, reason: 'INSUFFICIENT_STOCK' };
  }
  return { allowed: true, nextVersion: snapshot.version + 1 };
}

export function runTestsAgent16(): boolean {
  const ok = canFulfillOrder({ sku: 'JKT-01', availableQty: 1, version: 3 }, 1, 3);
  const conflict = canFulfillOrder({ sku: 'JKT-01', availableQty: 1, version: 4 }, 1, 3);
  if (!ok.allowed || ok.nextVersion !== 4 || conflict.allowed) {
    throw new Error('canFulfillOrder failed');
  }
  return true;
}
runTestsAgent16();
