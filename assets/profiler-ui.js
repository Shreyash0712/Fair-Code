/* ════════════════════════════════════════════════════════════════════════
   Fair Code - Dataset Profiler UI controller

   Wires the dropzone / file input / sample button to the engine
   (assets/profiler-engine.js) and renders the result. No network, no upload -
   FileReader reads the dropped file locally and the engine runs in-page.
   ════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var DISPLAY_GROUPS = 12; // mirror faircode/report.py
  var E = window.FairCodeProfiler;

  var dropzone = document.getElementById('dropzone');
  var fileInput = document.getElementById('fileInput');
  var sampleBtn = document.getElementById('sampleBtn');
  var errorEl = document.getElementById('error');
  var results = document.getElementById('results');
  var downloadHtmlBtn = document.getElementById('downloadHtmlBtn');
  var copyJsonBtn = document.getElementById('copyJsonBtn');

  var currentResult = null;
  var currentName = '';

  // ── Embedded sample dataset (health-themed, deliberately imbalanced) ─────
  // Skewed toward young Caucasian patients in two regions, with a sparse
  // elderly band and an under-sampled region - so the audit clearly fires.
  function buildSampleCSV() {
    var rows = [['patient_id', 'age', 'sex', 'race', 'region', 'diabetic']];
    // Heavily Caucasian; minorities rare. Skewed male. Concentrated young/mid age.
    var races = ['Caucasian', 'Caucasian', 'Caucasian', 'Caucasian', 'Caucasian',
                 'Caucasian', 'AfricanAmerican', 'Hispanic'];
    var regions = ['Northeast', 'Northeast', 'Northeast', 'Northeast', 'Midwest', 'Midwest'];
    var ages = [27, 29, 31, 33, 34, 36, 38, 41]; // tightly clustered; few elderly
    for (var i = 0; i < 160; i++) {
      var age = ages[i % ages.length];
      if (i % 53 === 0) age = 72;          // a rare elderly row
      var sex = i % 10 < 7 ? 'male' : 'female';  // ~70/30 skew
      var race = races[i % races.length];
      if (i % 80 === 0) race = 'Asian';    // a barely-present group
      var region = regions[i % regions.length];
      if (i % 80 === 0) region = 'West';   // a barely-present region
      var diabetic = i % 3 === 0 ? 'Yes' : 'No';
      rows.push([String(1000 + i), String(age), sex, race, region, diabetic]);
    }
    return rows.map(function (r) { return r.join(','); }).join('\n');
  }

  // ── Event wiring ─────────────────────────────────────────────────────────
  dropzone.addEventListener('click', function () { fileInput.click(); });
  dropzone.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); }
  });
  fileInput.addEventListener('change', function (e) {
    if (e.target.files && e.target.files[0]) readFile(e.target.files[0]);
  });
  ['dragenter', 'dragover'].forEach(function (ev) {
    dropzone.addEventListener(ev, function (e) {
      e.preventDefault(); dropzone.classList.add('dragover');
    });
  });
  ['dragleave', 'drop'].forEach(function (ev) {
    dropzone.addEventListener(ev, function (e) {
      e.preventDefault();
      if (ev === 'dragleave' && dropzone.contains(e.relatedTarget)) return;
      dropzone.classList.remove('dragover');
    });
  });
  dropzone.addEventListener('drop', function (e) {
    var f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    if (f) readFile(f);
  });
  sampleBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    runText(buildSampleCSV(), 'sample-health-data.csv');
  });
  downloadHtmlBtn.addEventListener('click', downloadHtmlReport);
  copyJsonBtn.addEventListener('click', copyResultAsJSON);

  function readFile(file) {
    if (!/\.csv$/i.test(file.name) && file.type !== 'text/csv') {
      return showError('Please choose a .csv file.');
    }
    var reader = new FileReader();
    reader.onload = function () { runText(String(reader.result), file.name); };
    reader.onerror = function () { showError('Could not read that file.'); };
    reader.readAsText(file);
  }

  function runText(text, name) {
    try {
      var table = E.parseCSV(text);
      if (!table.columns.length || !table.rows.length) {
        return showError('That CSV looks empty or has no data rows.');
      }
      var result = E.profile(table);
      errorEl.hidden = true;
      render(result, name);
    } catch (err) {
      showError('Could not profile that file: ' + err.message);
    }
  }

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.hidden = false;
    results.hidden = true;
  }

  // ── Rendering ─────────────────────────────────────────────────────────────
  var GRADE_COLOR = { A: 'var(--accent3)', B: 'var(--accent3)',
                      C: '#b08a2f', D: 'var(--accent)', F: 'var(--accent)' };

  function pct(x) { return (x * 100).toFixed(1) + '%'; }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function render(r, name) {
    currentResult = r;
    currentName = name;

    // Score ring
    var ring = document.getElementById('scoreRing');
    ring.style.setProperty('--pct', r.overall_score);
    ring.style.setProperty('--ring', GRADE_COLOR[r.grade] || 'var(--accent3)');
    document.getElementById('scoreNum').textContent = r.overall_score;
    document.getElementById('scoreGrade').textContent = 'GRADE ' + r.grade;
    document.getElementById('scoreFileName').textContent = name;
    document.getElementById('scoreSummary').textContent =
      r.n_rows.toLocaleString() + ' rows · ' + r.n_cols + ' columns · ' +
      r.dimensions.length + ' demographic dimension' +
      (r.dimensions.length === 1 ? '' : 's') + ' detected';

    // Flags
    var flagsBlock = document.getElementById('flagsBlock');
    var flagsList = document.getElementById('flagsList');
    flagsList.innerHTML = '';
    if (r.flags.length) {
      document.getElementById('flagCount').textContent = '(' + r.flags.length + ')';
      r.flags.forEach(function (f) {
        var li = document.createElement('li');
        li.textContent = f;
        flagsList.appendChild(li);
      });
      flagsBlock.hidden = false;
    } else {
      flagsBlock.hidden = true;
    }

    // Dimensions
    var dimsEl = document.getElementById('dimensions');
    dimsEl.innerHTML = '';
    r.dimensions.forEach(function (d) {
      dimsEl.appendChild(dimCard(d));
    });

    // Intersections
    renderIntersections(r.intersections);

    results.hidden = false;
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function dimCard(d) {
    var card = document.createElement('div');
    card.className = 'dim-card';

    var head = '<div class="dim-head"><div><span class="dim-name">' + esc(d.name) +
      '</span><span class="dim-kind">' + esc(d.kind) + '</span></div>' +
      '<span class="dim-score">' + d.dimension_score + '/100</span></div>';

    var maxShare = d.groups.length ? d.groups[0].share : 1;
    var bars = d.groups.slice(0, DISPLAY_GROUPS).map(function (g) {
      var under = d.under_represented.indexOf(g.label) !== -1 ? ' under' : '';
      var w = maxShare > 0 ? (g.share / maxShare) * 100 : 0;
      return '<div class="bar-row' + under + '">' +
        '<span class="bar-label" title="' + esc(g.label) + '">' + esc(g.label) + '</span>' +
        '<span class="bar-track"><span class="bar-fill" style="width:' + w.toFixed(1) + '%"></span></span>' +
        '<span class="bar-pct">' + pct(g.share) + ' (' + g.count.toLocaleString() + ')</span>' +
        '</div>';
    }).join('');

    var more = d.groups.length > DISPLAY_GROUPS
      ? '<div class="dim-more">… and ' + (d.groups.length - DISPLAY_GROUPS) + ' more groups</div>'
      : '';

    var meta = [];
    if (d.imbalance_ratio !== null) meta.push('imbalance ' + d.imbalance_ratio.toFixed(1) + '×');
    else if (d.n_groups > 1) meta.push('imbalance ∞ (empty subgroup)');
    if (d.missing_pct > 0) meta.push('missing ' + pct(d.missing_pct));
    if (d.skewness !== null) meta.push('skew ' + (d.skewness >= 0 ? '+' : '') + d.skewness.toFixed(2));

    card.innerHTML = head + bars + more +
      (meta.length ? '<div class="dim-meta">' + meta.join('  ·  ') + '</div>' : '');
    return card;
  }

  function renderIntersections(inters) {
    var block = document.getElementById('intersectionsBlock');
    var host = document.getElementById('intersections');
    host.innerHTML = '';
    if (!inters.length) { block.hidden = true; return; }
    var inter = inters[0];
    document.getElementById('intersectionNote').textContent =
      'Subgroups of ' + inter.dims[0] + ' × ' + inter.dims[1] +
      ' that are empty or near-empty:';
    var wrap = document.createElement('div');
    wrap.className = 'inter-cells';
    inter.cells.forEach(function (c) {
      var el = document.createElement('span');
      el.className = 'inter-cell' + (c.count === 0 ? ' empty' : '');
      el.textContent = c.a + ' × ' + c.b + ' = ' + c.count;
      wrap.appendChild(el);
    });
    host.appendChild(wrap);
    block.hidden = false;
  }

  // ── Report export: "Download report (HTML)" / "Copy as JSON" ────────────
  // Ports faircode/report.py's to_html so the browser report matches the
  // CLI's --html output (same palette, same layout).
  function buildHtmlReport(r) {
    var dimBlocks = r.dimensions.map(function (d) {
      var rows = d.groups.slice(0, DISPLAY_GROUPS).map(function (g) {
        var under = d.under_represented.indexOf(g.label) !== -1 ? 'under' : 'ok';
        return '<tr class="' + under + '"><td>' + esc(g.label) + '</td>' +
          '<td class="num">' + (g.share * 100).toFixed(1) + '%</td>' +
          '<td class="num">' + g.count.toLocaleString() + '</td>' +
          '<td class="bar"><span style="width:' + (g.share * 100).toFixed(1) + '%"></span></td></tr>';
      }).join('');
      return '<section class="dim"><h2>' + esc(d.name) +
        ' <span class="kind">' + esc(d.kind) + '</span> ' +
        '<span class="score">' + d.dimension_score + '/100</span></h2>' +
        '<table>' + rows + '</table></section>';
    }).join('');

    var flagHtml = '';
    if (r.flags.length) {
      var items = r.flags.map(function (f) { return '<li>' + esc(f) + '</li>'; }).join('');
      flagHtml = '<section class="flags"><h2>Flags</h2><ul>' + items + '</ul></section>';
    }

    return '<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8">\n' +
      '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
      '<title>Fair Code - Dataset Profile</title>\n<style>\n' +
      ' :root { --bg:#f4f1e8; --surface:#ebe7d9; --border:#d9d3c0; --accent:#a63a22;\n' +
      '          --accent3:#2f6b4f; --text:#36321f; --muted:#7d7459; }\n' +
      ' body { font-family:\'Helvetica Neue\',sans-serif; background:var(--bg); color:var(--text);\n' +
      '         max-width:820px; margin:0 auto; padding:48px 24px; }\n' +
      ' h1 { font-family:Georgia,serif; }\n' +
      ' .score { color:var(--accent3); font-size:.7em; font-weight:600; }\n' +
      ' .kind { color:var(--muted); font-size:.6em; text-transform:uppercase; letter-spacing:.08em; }\n' +
      ' .dim { background:var(--surface); border:1px solid var(--border); border-radius:8px;\n' +
      '         padding:16px 20px; margin:16px 0; }\n' +
      ' table { width:100%; border-collapse:collapse; }\n' +
      ' td { padding:4px 8px; font-size:14px; border-bottom:1px solid var(--border); }\n' +
      ' td.num { text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }\n' +
      ' td.bar { width:40%; }\n' +
      ' td.bar span { display:block; height:10px; background:var(--accent3); border-radius:3px; }\n' +
      ' tr.under td.bar span { background:var(--accent); }\n' +
      ' tr.under td:first-child::after { content:\' (under-represented)\'; color:var(--accent); font-size:11px; }\n' +
      ' .flags ul { list-style:none; padding:0; }\n' +
      ' .flags li { background:#fbeae3; border-left:3px solid var(--accent); padding:8px 12px; margin:6px 0; border-radius:0 4px 4px 0; }\n' +
      ' .head { border-bottom:2px solid var(--accent); padding-bottom:12px; }\n' +
      '</style></head><body>\n' +
      '<div class="head"><h1>Dataset Representation Profile</h1>\n' +
      '<p>' + r.n_rows.toLocaleString() + ' rows · ' + r.n_cols + ' columns · Score\n' +
      '<strong>' + r.overall_score + '/100</strong> (Grade ' + r.grade + ')</p></div>\n' +
      dimBlocks + '\n' + flagHtml + '\n' +
      '<p style="color:var(--muted);font-size:12px;margin-top:32px">\n' +
      'Generated by <a href="https://github.com/yakew7/Fair-Code">Fair Code</a> - diagnostic only.</p>\n' +
      '</body></html>';
  }

  function reportBaseName() {
    return (currentName || 'dataset').replace(/\.csv$/i, '') + '-profile-report';
  }

  function downloadHtmlReport() {
    if (!currentResult) return;
    var blob = new Blob([buildHtmlReport(currentResult)], { type: 'text/html' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = reportBaseName() + '.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function flashButton(btn, msg) {
    var original = btn.textContent;
    btn.textContent = msg;
    btn.disabled = true;
    setTimeout(function () {
      btn.textContent = original;
      btn.disabled = false;
    }, 1500);
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (err) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  function copyResultAsJSON() {
    if (!currentResult) return;
    var text = JSON.stringify(currentResult, null, 2);
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        flashButton(copyJsonBtn, '✓ Copied');
      }, function () {
        flashButton(copyJsonBtn, fallbackCopy(text) ? '✓ Copied' : 'Copy failed');
      });
    } else {
      flashButton(copyJsonBtn, fallbackCopy(text) ? '✓ Copied' : 'Copy failed');
    }
  }

  // Shareable demo link: profiler.html?demo loads the sample automatically.
  // Placed last so all declarations above (e.g. GRADE_COLOR) are initialized.
  if (/(?:\?|&)demo\b/.test(window.location.search)) {
    runText(buildSampleCSV(), 'sample-health-data.csv');
  }
})();
