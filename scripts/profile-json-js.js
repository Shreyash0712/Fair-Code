#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

// Load the profiler engine. It registers itself on globalThis.FairCodeProfiler.
require(path.join(__dirname, "..", "assets", "profiler-engine.js"));

const E = globalThis.FairCodeProfiler;

if (process.argv.length !== 3) {
  console.error("Usage: node scripts/profile-json-js.js <dataset.json>");
  process.exit(1);
}

const jsonPath = process.argv[2];
const text = fs.readFileSync(jsonPath, "utf8");

const table = E.parseJSON(text);
const result = E.profile(table);

process.stdout.write(JSON.stringify(result));
