#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

// Load the profiler engine. It registers itself on globalThis.FairCodeProfiler.
require(path.join(__dirname, "..", "assets", "profiler-engine.js"));

const E = globalThis.FairCodeProfiler;

if (process.argv.length !== 3) {
  console.error("Usage: node scripts/parse-json-js.js <dataset.json>");
  process.exit(1);
}

const jsonPath = process.argv[2];
const text = fs.readFileSync(jsonPath, "utf8");

// Report parseJSON()'s outcome as JSON on stdout (exit 0 either way) so
// callers - namely tests/test_json_edge_cases.py - can assert on the error
// message for malformed input without having to parse a Node stack trace.
try {
  const table = E.parseJSON(text);
  process.stdout.write(JSON.stringify({ ok: true, table: table }));
} catch (e) {
  process.stdout.write(JSON.stringify({ ok: false, error: e.message }));
}
