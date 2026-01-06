import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
import OpenAI from 'openai';
import type { TTSOptions } from './types.js';

let openaiClient: OpenAI | null = null;

function getOpenAIClient(): OpenAI {
  if (!openaiClient) {
    if (!process.env.OPENAI_API_KEY) {
      throw new Error(
        'OPENAI_API_KEY environment variable is required. Please add it to your .env file.'
      );
    }
    openaiClient = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
  }
  return openaiClient;
}

function getTextHash(text: string, voice: string, model: string): string {
  const content = `${text}|${voice}|${model}`;
  return crypto.createHash('sha256').update(content).digest('hex').substring(0, 16);
}

export async function generateSpeech(options: TTSOptions): Promise<string> {
  const { text, voice, model, outputPath } = options;

  // Generate deterministic filename based on content hash
  const hash = getTextHash(text, voice, model);
  const outputDir = path.dirname(outputPath);
  const cachedPath = path.join(outputDir, `speech_${hash}.mp3`);

  // Check if cached audio exists
  try {
    await fs.access(cachedPath);
    console.log(`♻️  Using cached audio: ${cachedPath}`);
    return cachedPath;
  } catch {
    // Cache miss, generate new audio
  }

  console.log(`🎙️  Generating speech with voice: ${voice}`);

  try {
    const openai = getOpenAIClient();
    const mp3 = await openai.audio.speech.create({
      model,
      voice: voice as 'alloy' | 'echo' | 'fable' | 'onyx' | 'nova' | 'shimmer',
      input: text,
    });

    const buffer = Buffer.from(await mp3.arrayBuffer());

    // Ensure directory exists
    await fs.mkdir(outputDir, { recursive: true });

    // Write audio file with hash-based name
    await fs.writeFile(cachedPath, buffer);

    console.log(`✅ Audio generated: ${cachedPath}`);
    return cachedPath;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`TTS generation failed: ${error.message}`);
    }
    throw error;
  }
}

export async function textToSpeech(
  text: string,
  outputPath: string
): Promise<string> {
  const voice = process.env.TTS_VOICE || 'nova';
  const model = process.env.TTS_MODEL || 'tts-1';

  return generateSpeech({
    text,
    voice,
    model,
    outputPath,
  });
}
