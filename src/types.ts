export interface TTSOptions {
  text: string;
  voice: string;
  model: string;
  outputPath: string;
}

export interface GenerateVideoParams {
  imagePath: string;
  audioPath: string;
  outputPath: string;
  fps?: number;
  steps?: number;
  lipWeight?: number;
  cfgScale?: number;
  quality?: 'balanced' | 'high' | 'ultra';
}
