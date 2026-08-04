#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

// Load the profiler engine. It registers itself on globalThis.FairCodeProfiler.
require(path.join(__dirname, "..", "assets", "profiler-engine.js"));

const E = globalThis.FairCodeProfiler;

if (process.argv.length !== 3) {
  console.error("Usage: node scripts/profile-js.js <dataset.csv>");
  process.exit(1);
}

const csvPath = process.argv[2];
const text = fs.readFileSync(csvPath, "utf8");

const table = E.parseCSV(text);
const result = E.profile(table);

process.stdout.write(JSON.stringify(result));
