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
  var announcer = document.getElementById('resultsAnnouncer');
  var mappingBlock = document.getElementById('mappingBlock');
  var mappingList = document.getElementById('mappingList');

  var crossControls = document.getElementById('crossControls');
  var crossA = document.getElementById('crossA');
  var crossB = document.getElementById('crossB');
  var referenceBtn = document.getElementById('referenceBtn');
  var referenceClearBtn = document.getElementById('referenceClearBtn');
  var referenceInput = document.getElementById('referenceInput');
  var referenceStatus = document.getElementById('referenceStatus');

  var currentResult = null;
  var currentName = '';
  var currentTable = null;   // parsed table, kept so overrides can re-profile
  var currentOverrides = {}; // column -> forced kind (issue #62)
  var currentOpts = {};      // cross / reference / thresholds (issues #56, #58)
  var autoKinds = {};        // column -> auto-detected kind (for the mapping hints)

  // Kinds a column can be manually mapped to, plus Auto / Not-demographic.
  var MAP_OPTIONS = [
    ['auto', 'Auto'], ['sex', 'Sex'], ['race', 'Race'], ['age', 'Age'],
    ['geography', 'Geography'], ['categorical', 'Categorical'], ['ignore', 'Not demographic']
  ];

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
    // Ignore keydowns bubbling up from the nested "sample" button - otherwise
    // pressing Enter/Space to activate it also re-triggers the file picker.
    if (e.target !== dropzone) return;
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); }
  });
  fileInput.addEventListener('change', function (e) {
    if (e.target.files && e.target.files[0]) readFile(e.target.files[0]);
    // The hidden input can't visibly hold focus after the native picker
    // closes - return it to the dropzone so keyboard users aren't stranded.
    dropzone.focus();
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
    var okExt = /\.(csv|tsv|json|xlsx)$/i.test(file.name);
    var okType = file.type === 'text/csv' || file.type === 'text/tab-separated-values' ||
      file.type === 'application/json' ||
      file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
    if (!okExt && !okType) {
      return showError('Please choose a .csv, .tsv, .json, or .xlsx file.');
    }
    var reader = new FileReader();
    reader.onerror = function () { showError('Could not read that file.'); };
    if (/\.xlsx$/i.test(file.name)) {
      reader.onload = async function () {
        try {
          runTable(await E.parseXLSX(reader.result), file.name);
        } catch (err) {
          showError('Could not profile that file: ' + err.message);
        }
      };
      reader.readAsArrayBuffer(file);
    } else {
      reader.onload = function () { runText(String(reader.result), file.name); };
      reader.readAsText(file);
    }
  }

  function runText(text, name) {
    try {
      if (/\.json$/i.test(name) || text.trim().startsWith('{')) {
        var table = E.parseJSON(text);
      } else {
        var table = E.parseCSV(text);
      }
      runTable(table, name);
    } catch (err) {
      showError('Could not profile that file: ' + err.message);
    }
  }

  // Shared tail for every input format (CSV/TSV, JSON, XLSX): validate the
  // parsed table isn't empty, then profile and render it.
  function runTable(table, name) {
    if (!table.columns.length || !table.rows.length) {
      return showError('That file looks empty or has no data rows.');
    }
    currentTable = table;
    currentOverrides = {};
    currentOpts = {};
    resetReference();
    var result = E.profile(table);
    autoKinds = {};
    result.dimensions.forEach(function (d) { autoKinds[d.name] = d.kind; });
    errorEl.hidden = true;
    render(result, name, true);
    renderMapping(table.columns);
  }

  // Re-run the engine with the current overrides + opts and re-render in place.
  function reprofile(scroll) {
    if (!currentTable) return;
    try {
      var result = E.profile(currentTable, currentOverrides, currentOpts);
      errorEl.hidden = true;
      render(result, currentName, scroll);
    } catch (err) {
      showError('Could not re-profile: ' + err.message);
    }
  }

  function resetReference() {
    referenceStatus.textContent = '';
    referenceClearBtn.hidden = true;
    referenceInput.value = '';
  }

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.hidden = false;
    results.hidden = true;
  }

  // ── Rendering ─────────────────────────────────────────────────────────────
  var GRADE_COLOR = { A: 'var(--accent3)', B: 'var(--accent3)',
                      C: 'var(--warn)', D: 'var(--accent)', F: 'var(--accent)' };

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function pct(x) { return (x * 100).toFixed(1) + '%'; }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function render(r, name, scroll) {
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
    renderIntersections(r);

    results.hidden = false;
    if (scroll) {
      results.scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'start' });
    }

    announcer.textContent = 'Profile complete for ' + name + ': score ' + r.overall_score +
      ' out of 100, grade ' + r.grade + '. ' + r.dimensions.length + ' demographic dimension' +
      (r.dimensions.length === 1 ? '' : 's') + ' detected' +
      (r.flags.length ? ', ' + r.flags.length + ' flag' + (r.flags.length === 1 ? '' : 's') + ' raised.' : '.');
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
      var ci = (g.ci_low != null && g.ci_high != null)
        ? '<span class="bar-ci" title="95% Wilson confidence interval on this share">95% CI '
          + (g.ci_low * 100).toFixed(1) + '–' + (g.ci_high * 100).toFixed(1) + '%</span>'
        : '';
      var small = g.small_group
        ? '<span class="bar-small" title="Fewer than the minimum group size - this metric may be unreliable">⚠ small group</span>'
        : '';
      return '<div class="bar-row' + under + '">' +
        '<span class="bar-label" title="' + esc(g.label) + '">' + esc(g.label) + '</span>' +
        '<span class="bar-track"><span class="bar-fill" style="width:' + w.toFixed(1) + '%"></span></span>' +
        '<span class="bar-pct">' + pct(g.share) + ' (' + g.count.toLocaleString() + ')</span>' +
        ci + small +
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

    var ref = '';
    if (d.reference) {
      var refRows = d.reference.groups.slice(0, DISPLAY_GROUPS).map(function (g) {
        var dCls = g.delta < 0 ? 'under' : g.delta > 0 ? 'over' : '';
        return '<div class="ref-row">' +
          '<span class="ref-label" title="' + esc(g.label) + '">' + esc(g.label) + '</span>' +
          '<span class="ref-vals">exp ' + pct(g.expected) + ' · act ' + pct(g.actual) + '</span>' +
          '<span class="ref-delta ' + dCls + '">' +
            (g.delta > 0 ? '+' : '') + (g.delta * 100).toFixed(1) + ' pp</span>' +
          '</div>';
      }).join('');
      ref = '<div class="dim-reference"><div class="dim-reference-head">vs reference · ' +
        'deviation ' + pct(d.reference.deviation) + '</div>' + refRows + '</div>';
    }

    card.innerHTML = head + bars + more +
      (meta.length ? '<div class="dim-meta">' + meta.join('  ·  ') + '</div>' : '') + ref;
    return card;
  }

  function renderIntersections(r) {
    var block = document.getElementById('intersectionsBlock');
    var host = document.getElementById('intersections');
    var note = document.getElementById('intersectionNote');
    host.innerHTML = '';
    // Need at least two dimensions before a cross is meaningful.
    if (r.dimensions.length < 2) { block.hidden = true; return; }
    block.hidden = false;
    populateCrossSelects(r.dimensions);

    if (!r.intersections.length) {
      note.textContent = 'No empty or near-empty subgroups for the selected pair.';
      return;
    }
    var inter = r.intersections[0];
    note.textContent = 'Subgroups of ' + inter.dims[0] + ' × ' + inter.dims[1] +
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
  }

  // ── Column mapping (manual override, issue #62) ─────────────────────────
  // Lists every column with its auto-detected kind and a dropdown to override
  // it. Built once per file; changing a dropdown re-profiles in place without
  // rebuilding the list, so selections and focus survive.
  function renderMapping(columns) {
    mappingList.innerHTML = '';
    columns.forEach(function (col) {
      var auto = autoKinds[col];
      var row = document.createElement('div');
      row.className = 'map-row';

      var hint = auto
        ? 'auto: <span class="on">' + esc(auto) + '</span>'
        : 'auto: not detected';

      var opts = MAP_OPTIONS.map(function (o) {
        return '<option value="' + o[0] + '">' + o[1] + '</option>';
      }).join('');

      row.innerHTML =
        '<span class="map-col" title="' + esc(col) + '">' + esc(col) + '</span>' +
        '<span class="map-auto">' + hint + '</span>' +
        '<select class="map-select" data-col="' + esc(col) +
        '" aria-label="Map column ' + esc(col) + '">' + opts + '</select>';

      mappingList.appendChild(row);
    });
    mappingBlock.hidden = false;
  }

  function readOverrides() {
    var overrides = {};
    var selects = mappingList.querySelectorAll('.map-select');
    for (var i = 0; i < selects.length; i++) {
      var sel = selects[i];
      var row = sel.closest('.map-row');
      if (sel.value !== 'auto') {
        overrides[sel.getAttribute('data-col')] = sel.value;
        if (row) row.classList.add('overridden');
      } else if (row) {
        row.classList.remove('overridden');
      }
    }
    return overrides;
  }

  // Delegated so it keeps working across re-renders of the list.
  mappingList.addEventListener('change', function (e) {
    if (!e.target.classList.contains('map-select') || !currentTable) return;
    currentOverrides = readOverrides();
    reprofile(false);
  });

  // ── Intersection cross-selectors (issue #58) ───────────────────────────
  function populateCrossSelects(dims) {
    var names = dims.map(function (d) { return d.name; });
    var selA = currentOpts.cross ? currentOpts.cross[0] : names[0];
    var selB = currentOpts.cross ? currentOpts.cross[1] : names[1];
    [[crossA, selA], [crossB, selB]].forEach(function (pair) {
      var sel = pair[0], chosen = pair[1];
      sel.innerHTML = names.map(function (n) {
        return '<option value="' + esc(n) + '"' + (n === chosen ? ' selected' : '') +
          '>' + esc(n) + '</option>';
      }).join('');
    });
  }

  crossControls.addEventListener('change', function () {
    if (!currentTable) return;
    currentOpts.cross = [crossA.value, crossB.value];
    reprofile(false);
  });

  // ── Reference baseline (issue #56) ──────────────────────────────────────
  referenceBtn.addEventListener('click', function () { referenceInput.click(); });
  referenceInput.addEventListener('change', function (e) {
    var f = e.target.files && e.target.files[0];
    if (!f) return;
    var reader = new FileReader();
    reader.onerror = function () { showError('Could not read the reference file.'); };
    function applyReferenceTable(table) {
      try {
        currentOpts.reference = E.parseReference(table);
        referenceStatus.textContent = '⚖ scored vs ' + f.name;
        referenceClearBtn.hidden = false;
        reprofile(false);
      } catch (err) {
        showError('Could not read reference baseline: ' + err.message);
      }
    }
    if (/\.xlsx$/i.test(f.name)) {
      reader.onload =async function () {
        try {
          applyReferenceTable(await E.parseXLSX(reader.result));
        } catch (err) {
          showError('Could not read reference baseline: ' + err.message);
        }
      };
      reader.readAsArrayBuffer(f);
    } else {
      reader.onload = function () {
        try {
          var text = String(reader.result);
          var table = (/\.json$/i.test(f.name) || f.type === 'application/json')
            ? E.parseJSON(text) : E.parseCSV(text);
          applyReferenceTable(table);
        } catch (err) {
          showError('Could not read reference baseline: ' + err.message);
        }
      };
      reader.readAsText(f);
    }
  });
  referenceClearBtn.addEventListener('click', function () {
    delete currentOpts.reference;
    resetReference();
    reprofile(false);
  });

  // ── Report export: "Download report (HTML)" / "Copy as JSON" ────────────
  // Ports faircode/report.py's to_html so the browser report matches the
  // CLI's --html output (same palette, same layout).
  function buildHtmlReport(r) {
    var dimBlocks = r.dimensions.map(function (d) {
      var rows = d.groups.slice(0, DISPLAY_GROUPS).map(function (g) {
        var classes = [];
        if (d.under_represented.indexOf(g.label) !== -1) classes.push('under');
        if (g.small_group) classes.push('small-group');
        var ci = (g.ci_low != null && g.ci_high != null)
          ? (g.ci_low * 100).toFixed(1) + '–' + (g.ci_high * 100).toFixed(1) + '%' : '';
        return '<tr class="' + classes.join(' ') + '"><td>' + esc(g.label) + '</td>' +
          '<td class="num">' + (g.share * 100).toFixed(1) + '%</td>' +
          '<td class="num ci">' + ci + '</td>' +
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
      ' td.ci { color:var(--muted); font-size:12px; }\n' +
      ' td.bar { width:40%; }\n' +
      ' td.bar span { display:block; height:10px; background:var(--accent3); border-radius:3px; }\n' +
      ' tr.under td.bar span { background:var(--accent); }\n' +
      ' tr.under td:first-child::after { content:\' (under-represented)\'; color:var(--accent); font-size:11px; }\n' +
      ' tr.small-group td:first-child::before { content:\'⚠ small group \'; color:var(--accent); }\n' +
      ' .flags ul { list-style:none; padding:0; }\n' +
      ' .flags li { background:#fbeae3; border-left:3px solid var(--accent); padding:8px 12px; margin:6px 0; border-radius:0 4px 4px 0; }\n' +
      ' .head { border-bottom:2px solid var(--accent); padding-bottom:12px; }\n' +
      ' .print-btn { position:fixed; top:16px; right:16px; background:var(--accent); color:#fff;\n' +
      '              border:0; border-radius:6px; padding:8px 14px; font-size:13px; cursor:pointer;\n' +
      '              font-family:inherit; }\n' +
      ' @media print { .print-btn { display:none; } body { padding:24px; max-width:none; } }\n' +
      '</style></head><body>\n' +
      '<button class="print-btn" onclick="window.print()">🖨 Print / Save as PDF</button>\n' +
      '<div class="head"><h1>Dataset Representation Profile</h1>\n' +
      '<p>' + r.n_rows.toLocaleString() + ' rows · ' + r.n_cols + ' columns · Score\n' +
      '<strong>' + r.overall_score + '/100</strong> (Grade ' + r.grade + ')</p></div>\n' +
      dimBlocks + '\n' + flagHtml + '\n' +
      '<p style="color:var(--muted);font-size:12px;margin-top:32px">\n' +
      'Generated by <a href="https://github.com/yakew7/Fair-Code">Fair Code</a> - diagnostic only.</p>\n' +
      '</body></html>';
  }

  function reportBaseName() {
    return (currentName || 'dataset').replace(/\.(csv|tsv|json|xlsx)$/i, '') + '-profile-report';
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
