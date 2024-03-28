import { type Language } from "../utils/languages";

export const [GPT_35_TURBO, GPT_35_TURBO_16K, GPT_4, GPT_4_32K] = [
  "gpt-3.5-turbo" as const,
  "gpt-3.5-turbo-16k" as const,
  "gpt-4" as const,
  "gpt-4-32k" as const,
  
];
export const GPT_MODEL_NAMES = [GPT_35_TURBO, GPT_35_TURBO_16K, GPT_4,  GPT_4_32K];
export type GPTModelNames = "gpt-3.5-turbo" | "gpt-3.5-turbo-16k" | "gpt-4" | "gpt-4-32k";

export const MAX_TOKENS: Record<GPTModelNames, number> = {
  "gpt-3.5-turbo": 4000,
  "gpt-3.5-turbo-16k": 16000,
  "gpt-4": 4000,
  "gpt-4-32k": 28000,
};

export interface ModelSettings {
  language: Language;
  customApiKey: string;
  customModelName: GPTModelNames;
  customTemperature: number;
  customMaxLoops: number;
  maxTokens: number;
}
