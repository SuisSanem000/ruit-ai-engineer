export function computeBackoffMs(attempt: number, baseMs: number = 200, maxMs: number = 10_000): number {
  const exp = Math.min(maxMs, baseMs * Math.pow(2, Math.max(0, attempt)));
  const deterministicJitter = (attempt * 37) % 100;
  return Math.min(maxMs, exp + deterministicJitter);
}

export function runTestsAgent08(): boolean {
  const first = computeBackoffMs(0, 200, 5000);
  const third = computeBackoffMs(2, 200, 5000);
  if (first < 200 || third <= first) throw new Error('computeBackoffMs failed');
  return true;
}
runTestsAgent08();
