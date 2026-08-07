#!/usr/bin/env node
// Fetches the pinned SheetJS build (same version/URL as profiler.html) to a
// temp file and requires it normally, so tests/test_js_parity.py can check
// assets/profiler-engine.js's parseXLSX() against the Python CLI without
// vendoring an 800KB+ third-party library into the repo. Exits with a
// distinct code if the network is unavailable, so the test can skip rather
// than fail the whole suite.

const fs = require("fs");
const os = require("os");
const path = require("path");

const XLSX_CDN_URL = "https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js";
const NO_NETWORK_EXIT_CODE = 3;

if (process.argv.length !== 3) {
  console.error("Usage: node scripts/profile-xlsx-js.js <dataset.xlsx>");
  process.exit(1);
}

async function main() {
  const cachePath = path.join(os.tmpdir(), "fair-code-xlsx-0.18.5.min.js");
  if (!fs.existsSync(cachePath)) {
    let source;
    try {
      const res = await fetch(XLSX_CDN_URL);
      if (!res.ok) throw new Error("HTTP " + res.status);
      source = await res.text();
    } catch (err) {
      console.error("Could not fetch SheetJS from the CDN (" + err.message + ") - skipping.");
      process.exit(NO_NETWORK_EXIT_CODE);
    }
    fs.writeFileSync(cachePath, source);
  }

  global.XLSX = require(cachePath);

  require(path.join(__dirname, "..", "assets", "profiler-engine.js"));
  const E = globalThis.FairCodeProfiler;

  const xlsxPath = process.argv[2];
  const buf = fs.readFileSync(xlsxPath);
  const arrayBuffer = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);

  const table = E.parseXLSX(arrayBuffer);
  const result = E.profile(table);
  process.stdout.write(JSON.stringify(result));
}

main();
