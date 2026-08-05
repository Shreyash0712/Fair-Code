#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

// Load the profiler engine. It registers itself on globalThis.FairCodeProfiler.
require(path.join(__dirname, "..", "assets", "profiler-engine.js"));

const E = globalThis.FairCodeProfiler;

if (process.argv.length !== 4) {
  console.error("Usage: node scripts/compare-js.js <a.csv> <b.csv>");
  process.exit(1);
}

const [pathA, pathB] = process.argv.slice(2);
const resultA = E.profile(E.parseCSV(fs.readFileSync(pathA, "utf8")));
const resultB = E.profile(E.parseCSV(fs.readFileSync(pathB, "utf8")));

const cmp = E.compare(resultA, resultB, path.basename(pathA), path.basename(pathB));

process.stdout.write(JSON.stringify(cmp));
