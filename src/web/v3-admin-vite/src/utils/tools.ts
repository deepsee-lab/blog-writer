export function parseJSON<T = unknown>(input: string): T | string {
  try {
    return JSON.parse(input)
  } catch (error) {
    return input
  }
}

export function stringifyJSON(input: unknown): string | unknown {
  try {
    return JSON.stringify(input)
  } catch (error) {
    return input
  }
}
