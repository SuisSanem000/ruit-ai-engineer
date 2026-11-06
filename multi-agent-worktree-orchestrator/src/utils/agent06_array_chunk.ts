export function chunkArray<T>(items: readonly T[], size: number): T[][] {
  if (size <= 0) throw new Error('chunk size must be positive');
  const chunks: T[][] = [];
  for (let i = 0; i < items.length; i += size) {
    chunks.push(items.slice(i, i + size));
  }
  return chunks;
}

export function runTestsAgent06(): boolean {
  const res = chunkArray([1, 2, 3, 4, 5], 2);
  if (res.length !== 3 || res[2][0] !== 5) throw new Error('chunkArray failed');
  return true;
}
runTestsAgent06();
