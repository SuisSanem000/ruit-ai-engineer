export function fnv1aHash(payload: string): string {
  let hash = 0x811c9dc5;
  for (let i = 0; i < payload.length; i++) {
    hash ^= payload.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193);
  }
  return (hash >>> 0).toString(16).padStart(8, '0');
}

export function runTestsAgent09(): boolean {
  const h1 = fnv1aHash('seller-42:item-99:delist');
  const h2 = fnv1aHash('seller-42:item-99:delist');
  if (h1 !== h2 || h1.length !== 8) throw new Error('fnv1aHash failed');
  return true;
}
runTestsAgent09();
