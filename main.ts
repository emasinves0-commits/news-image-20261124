// Copies the rendered poster (entry.png) into the output directory.
// Output dir comes from MAKEFUN_OUTPUT_DIR (default: out/). Standard library only.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const SOURCE = "entry.png";
const MAX_BYTES = 1024 * 1024; // bounty limit: 1 MiB
const PNG_MAGIC = "89504e470d0a1a0a";

function fail(message: string): never {
  console.error("main.ts: " + message);
  process.exit(1);
}

if (!existsSync(SOURCE)) {
  fail(
    `${SOURCE} not found in ${process.cwd()}. ` +
      "Render it first with: python3 draw24.py entry.png",
  );
}

const size = statSync(SOURCE).size;
if (size > MAX_BYTES) {
  fail(`${SOURCE} is ${size} bytes, over the 1 MiB (${MAX_BYTES}) limit.`);
}
if (readFileSync(SOURCE).subarray(0, 8).toString("hex") !== PNG_MAGIC) {
  fail(`${SOURCE} is not a PNG file (bad signature).`);
}

const outDir: string = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, SOURCE);
copyFileSync(SOURCE, dest);
console.log(`copied ${SOURCE} (${size} bytes) -> ${dest}`);
