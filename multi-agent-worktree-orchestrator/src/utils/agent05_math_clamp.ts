export function clamp(value: number, min: number, max: number): number {
  if (min > max) throw new Error('min cannot exceed max');
  return Math.min(max, Math.max(min, value));
}

export function lerp(start: number, end: number, alpha: number): number {
  return start + (end - start) * clamp(alpha, 0, 1);
}

export function runTestsAgent05(): boolean {
  if (clamp(150, 0, 100) !== 100) throw new Error('clamp upper bound failed');
  if (lerp(0, 200, 0.25) !== 50) throw new Error('lerp failed');
  return true;
}
runTestsAgent05();
