export function parseEuropeanPrice(raw: string): number {
  const cleaned = raw.replace(/[^0-9,.-]/g, '').trim();
  const normalized = cleaned.includes(',') && cleaned.includes('.')
    ? cleaned.replace(/\./g, '').replace(',', '.')
    : cleaned.replace(',', '.');
  const value = Number.parseFloat(normalized);
  if (Number.isNaN(value) || value < 0) {
    throw new Error(`Invalid price format: ${raw}`);
  }
  return Math.round(value * 100) / 100;
}

export function runTestsAgent03(): boolean {
  if (parseEuropeanPrice('19,50 €') !== 19.5) throw new Error('parseEuropeanPrice failed 19,50');
  if (parseEuropeanPrice('1.250,99 EUR') !== 1250.99) throw new Error('parseEuropeanPrice failed thousands');
  return true;
}
runTestsAgent03();
