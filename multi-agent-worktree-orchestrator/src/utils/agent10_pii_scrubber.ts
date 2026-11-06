export function scrubSensitiveText(input: string): string {
  return input
    .replace(/Bearer\s+[A-Za-z0-9._-]+/gi, 'Bearer [REDACTED]')
    .replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, '[EMAIL_REDACTED]');
}

export function runTestsAgent10(): boolean {
  const sample = 'Auth Bearer eyJhbGciOiJIUzI1NiJ9 for seller@example.com';
  const scrubbed = scrubSensitiveText(sample);
  if (scrubbed.includes('eyJhbG') || scrubbed.includes('seller@example.com')) {
    throw new Error('scrubSensitiveText failed');
  }
  return true;
}
runTestsAgent10();
