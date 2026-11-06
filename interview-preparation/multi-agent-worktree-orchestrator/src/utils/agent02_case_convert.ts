export function toSnakeCase(input: string): string {
  return input
    .replace(/([a-z0-9])([A-Z])/g, '$1_$2')
    .replace(/[-\s]+/g, '_')
    .toLowerCase();
}

export function toCamelCase(input: string): string {
  return input
    .toLowerCase()
    .replace(/[_-\s]+([a-z0-9])/g, (_, ch: string) => ch.toUpperCase());
}

export function runTestsAgent02(): boolean {
  if (toSnakeCase('marketplaceListingId') !== 'marketplace_listing_id') throw new Error('toSnakeCase failed');
  if (toCamelCase('marketplace_listing_id') !== 'marketplaceListingId') throw new Error('toCamelCase failed');
  return true;
}
runTestsAgent02();
