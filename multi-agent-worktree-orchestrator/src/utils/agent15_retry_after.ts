export function parseRetryAfterMs(
  headerVal: string | null | undefined,
  fallbackMs: number = 1000
): number {
  if (!headerVal) return fallbackMs;
  const seconds = Number(headerVal.trim());
  if (!Number.isNaN(seconds) && seconds >= 0) {
    return Math.round(seconds * 1000);
  }
  return fallbackMs;
}

export function runTestsAgent15(): boolean {
  if (parseRetryAfterMs('5') !== 5000) throw new Error('parseRetryAfterMs numeric failed');
  if (parseRetryAfterMs(undefined, 1500) !== 1500) throw new Error('parseRetryAfterMs fallback failed');
  return true;
}
runTestsAgent15();
