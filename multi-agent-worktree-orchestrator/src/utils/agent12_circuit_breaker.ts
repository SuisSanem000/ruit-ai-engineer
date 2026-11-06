export type CircuitState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export function evaluateCircuitState(
  failures: number,
  totalRequests: number,
  thresholdRatio: number = 0.15,
  minSampleSize: number = 10
): CircuitState {
  if (totalRequests < minSampleSize) return 'CLOSED';
  return failures / totalRequests >= thresholdRatio ? 'OPEN' : 'CLOSED';
}

export function runTestsAgent12(): boolean {
  if (evaluateCircuitState(5, 20, 0.15, 10) !== 'OPEN') throw new Error('circuit should open');
  if (evaluateCircuitState(1, 20, 0.15, 10) !== 'CLOSED') throw new Error('circuit should stay closed');
  return true;
}
runTestsAgent12();
