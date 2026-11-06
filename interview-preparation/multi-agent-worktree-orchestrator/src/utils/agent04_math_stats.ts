export function mean(values: readonly number[]): number {
  if (values.length === 0) return 0;
  const sum = values.reduce((acc, v) => acc + v, 0);
  return sum / values.length;
}

export function percentile(values: readonly number[], p: number): number {
  if (values.length === 0) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const idx = Math.min(sorted.length - 1, Math.max(0, Math.ceil((p / 100) * sorted.length) - 1));
  return sorted[idx];
}

export function runTestsAgent04(): boolean {
  if (mean([10, 20, 30]) !== 20) throw new Error('mean failed');
  if (percentile([10, 20, 30, 40, 100], 95) !== 100) throw new Error('percentile failed');
  return true;
}
runTestsAgent04();
