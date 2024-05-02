import { type Language } from "../utils/languages";

export const [GPT_35_TURBO, GPT_35_TURBO_16K, GPT_4, GPT_4_32K, GPT4_TURBO] = [
  "gpt-3.5-turbo" as const,
  "gpt-3.5-turbo-16k" as const,
  "gpt-4" as const,
  "gpt-4-32k" as const,
  "gpt4-turbo" as const,
  
];
export const GPT_MODEL_NAMES = [GPT_35_TURBO, GPT_35_TURBO_16K, GPT_4,  GPT_4_32K, GPT4_TURBO];
export type GPTModelNames = "gpt-3.5-turbo" | "gpt-3.5-turbo-16k" | "gpt-4" | "gpt-4-32k" | "gpt4-turbo";

export const MAX_TOKENS: Record<GPTModelNames, number> = {
  "gpt-3.5-turbo": 4000,
  "gpt-3.5-turbo-16k": 16000,
  "gpt-4": 4000,
  "gpt-4-32k": 28000,
  "gpt4-turbo": 10000,
};

export interface ModelSettings {
  language: Language;
  customApiKey: string;
  customModelName: string;
  customTemperature: number;
  customMaxLoops: number;
  maxTokens: number;
}
