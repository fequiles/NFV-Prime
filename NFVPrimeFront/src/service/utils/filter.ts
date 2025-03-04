export function removeAccents(str: string): string {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

export function filterOption(
  input: string,
  option?: { label: string; value: string }
) {
  const value = removeAccents(input.toLowerCase());
  const label = removeAccents(option?.label ?? "").toLowerCase();

  return label.includes(value);
}
