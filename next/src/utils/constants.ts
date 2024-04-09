import { ENGLISH } from "./languages";
import type { ModelSettings } from "../types";
import { serverEnv } from "../env/schema.mjs";

export const GPT_35_TURBO = "gpt-3.5-turbo" as const;
export const GPT_4 = "gpt-4" as const;
export const GPT_4_32k = "gpt-4-32k" as const;
export const GPT_MODEL_NAMES = [GPT_35_TURBO, GPT_4, GPT_4_32k];

export const DEFAULT_MAX_LOOPS_FREE = 25 as const;
export const DEFAULT_MAX_LOOPS_CUSTOM_API_KEY = 10 as const;

export const getDefaultModelSettings = (): ModelSettings => {
  return {
    customApiKey: "",
    language: ENGLISH,
    // customModelName: serverEnv.OPENAI_AZURE_OPENAI_DEPLOYMENT_NAME,
    customModelName: GPT_4_32k,
    customTemperature: 0,
    customMaxLoops: DEFAULT_MAX_LOOPS_FREE,
    maxTokens: 5000,
  };
};
