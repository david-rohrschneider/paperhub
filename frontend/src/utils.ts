import type { UserRefs } from "@/api/types";

export const hasChanged = <T extends object>(original: T, changes: Partial<T>): boolean => {
  const isDifferent = <T>(originalValue: T, newValue: T): boolean => {
    if (Array.isArray(originalValue) && Array.isArray(newValue)) {
      // Check shallow equality for arrays
      return (
        originalValue.length !== newValue.length ||
        originalValue.some((value, index) => value !== newValue[index])
      );
    }

    // Check if both are objects and neither is null
    if (
      originalValue &&
      newValue &&
      typeof originalValue === "object" &&
      typeof newValue === "object"
    )
      // Recurse for nested objects
      return hasChanged(originalValue, newValue);

    // Check primitive or other types
    return originalValue !== newValue;
  };
  for (const key in changes) {
    const originalValue = original[key];
    const newValue = changes[key];

    if (isDifferent(originalValue, newValue)) return true;
  }

  return false;
};

export const USER_REFS_EXP: Record<keyof UserRefs, RegExp> = {
  orcid: /^https:\/\/orcid\.org\/(\d{4}-){3}\d{3}(\d|X)$/,
  google_scholar:
    /^https:\/\/scholar\.google\.[a-z]{2,3}\/citations\?hl=[a-z]{2}(&user=[A-Za-z0-9]+)?$/,
  linkedin: /^https:\/\/www\.linkedin\.com\/in\/[A-Za-z0-9-]+\/?$/,
  researchgate: /^https:\/\/www\.researchgate\.net\/profile\/[A-Za-z0-9-]+$/,
};
