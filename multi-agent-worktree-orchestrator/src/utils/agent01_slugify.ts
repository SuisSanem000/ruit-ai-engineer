export function slugify(input: string): string {
  return input
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function runTestsAgent01(): boolean {
  if (slugify('Hello, World! 2026') !== 'hello-world-2026') throw new Error('slugify failed basic test');
  if (slugify('  Café & Résumé  ') !== 'cafe-resume') throw new Error('slugify failed accent test');
  return true;
}
runTestsAgent01();
