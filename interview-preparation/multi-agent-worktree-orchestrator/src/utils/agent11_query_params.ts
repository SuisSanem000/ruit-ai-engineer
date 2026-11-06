export function buildQueryString(params: Record<string, string | number | boolean | undefined>): string {
  const entries = Object.entries(params)
    .filter(([, v]) => v !== undefined)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`);
  return entries.length > 0 ? `?${entries.join('&')}` : '';
}

export function runTestsAgent11(): boolean {
  const q = buildQueryString({ page: 2, sort: 'price asc', empty: undefined });
  if (q !== '?page=2&sort=price%20asc') throw new Error('buildQueryString failed');
  return true;
}
runTestsAgent11();
