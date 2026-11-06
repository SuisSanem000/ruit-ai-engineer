export function detectMissingFields(
  payload: Record<string, unknown>,
  requiredFields: readonly string[]
): string[] {
  return requiredFields.filter(
    (field) => !(field in payload) || payload[field] === undefined || payload[field] === null
  );
}

export function runTestsAgent13(): boolean {
  const missing = detectMissingFields({ id: '123', title: 'Jacket' }, ['id', 'title', 'price']);
  if (missing.length !== 1 || missing[0] !== 'price') throw new Error('detectMissingFields failed');
  return true;
}
runTestsAgent13();
