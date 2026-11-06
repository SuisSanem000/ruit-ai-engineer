export function dedupeBy<T, K>(items: readonly T[], keyFn: (item: T) => K): T[] {
  const seen = new Set<K>();
  const result: T[] = [];
  for (const item of items) {
    const k = keyFn(item);
    if (!seen.has(k)) {
      seen.add(k);
      result.push(item);
    }
  }
  return result;
}

export function runTestsAgent07(): boolean {
  const out = dedupeBy([{ id: 'a' }, { id: 'b' }, { id: 'a' }], (x) => x.id);
  if (out.length !== 2) throw new Error('dedupeBy failed');
  return true;
}
runTestsAgent07();
