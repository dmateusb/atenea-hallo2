#!/usr/bin/env node
import { Command } from 'commander';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import ora from 'ora';
import { config } from 'dotenv';
import { textToSpeech } from './tts.js';
import { generateVideo } from './video-generator.js';

config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const program = new Command();

program
  .name('atenea-hallo2')
  .description('AI Avatar Video Generator using Hallo2')
  .version('1.0.0');

program
  .command('generate')
  .description('Generate a talking head video from text input')
  .option('-i, --input <file>', 'Input text file', 'input.txt')
  .option('-a, --avatar <image>', 'Avatar image path', 'data/images/avatar.png')
  .option('-o, --output <file>', 'Output video path', 'output.mp4')
  .option('-v, --voice <voice>', 'TTS voice (nova, alloy, echo, fable, onyx, shimmer)', 'nova')
  .option('--fps <number>', 'Frame rate (default: 25)', '25')
  .option('--steps <number>', 'Inference steps - 40=balanced, 50=high quality (default: 40)', '40')
  .action(async (options) => {
    const spinner = ora();

    try {
      // Validate OpenAI API key
      if (!process.env.OPENAI_API_KEY) {
        console.error(
          chalk.red('❌ OPENAI_API_KEY not found in environment variables')
        );
        console.log(chalk.yellow('\nPlease create a .env file with:'));
        console.log(chalk.cyan("OPENAI_API_KEY='your-key-here'"));
        process.exit(1);
      }

      // Read input text
      spinner.start('Reading input text...');
      const inputPath = path.resolve(options.input);
      const inputText = await fs.readFile(inputPath, 'utf-8');
      spinner.succeed(`Input text loaded (${inputText.length} characters)`);

      // Validate avatar image
      const avatarPath = path.resolve(options.avatar);
      try {
        await fs.access(avatarPath);
        spinner.succeed(`Avatar image found: ${path.basename(avatarPath)}`);
      } catch {
        spinner.fail(`Avatar image not found: ${avatarPath}`);
        console.log(
          chalk.yellow('\nPlease add an avatar image to:')
        );
        console.log(chalk.cyan('data/images/avatar.png'));
        process.exit(1);
      }

      // Setup paths
      const audioDir = path.join(__dirname, '..', 'data', 'audio');
      const tempAudioPath = path.join(audioDir, 'temp.mp3');
      const videoPath = path.resolve(options.output);

      console.log(chalk.blue('\n🎬 Starting Hallo2 video generation\n'));

      // Generate audio from text
      spinner.start('Generating speech from text...');
      process.env.TTS_VOICE = options.voice;
      const audioPath = await textToSpeech(inputText, tempAudioPath);
      spinner.succeed('Speech generated');

      // Parse numeric options
      const fps = parseInt(options.fps, 10);
      const steps = parseInt(options.steps, 10);

      if (isNaN(fps) || fps <= 0) {
        console.error(chalk.red('❌ Invalid FPS value'));
        process.exit(1);
      }

      if (isNaN(steps) || steps <= 0) {
        console.error(chalk.red('❌ Invalid steps value'));
        process.exit(1);
      }

      // Generate video
      spinner.start(
        chalk.yellow(
          'Generating talking head video with Hallo2 (5-8 min on RTX 4090 for 1-min video)...'
        )
      );

      await generateVideo({
        imagePath: avatarPath,
        audioPath,
        outputPath: videoPath,
        fps,
        steps,
      });

      spinner.succeed('Video generated successfully!');

      console.log(chalk.green('\n✅ Success!\n'));
      console.log(chalk.cyan(`Video saved to: ${videoPath}`));
      console.log(chalk.cyan(`Audio saved to: ${audioPath}`));
      console.log(chalk.cyan(`\nOpen video: open "${videoPath}"`));
    } catch (error) {
      spinner.fail('Failed');
      console.error(chalk.red('\n❌ Error:'), error);
      process.exit(1);
    }
  });

program.parse();
