/* ════════════════════════════════════════════════════════════════════════
   Fair Code - Dataset Profiler: COMPARE controller (representation drift)

   Wires the two "A / B" dropzones to the engine's compare() and renders the
   side-by-side drift view. Like the single-profile UI, nothing is uploaded -
   both files are read locally with FileReader and diffed in-page.
   ════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var DISPLAY_GROUPS = 12; // mirror faircode/report.py
  var E = window.FairCodeProfiler;
  if (!E || !E.compare) return;

  var dropA = document.getElementById('dropA');
  var dropB = document.getElementById('dropB');
  var fileA = document.getElementById('fileA');
  var fileB = document.getElementById('fileB');
  var nameAEl = document.getElementById('nameA');
  var nameBEl = document.getElementById('nameB');
  var sampleBtn = document.getElementById('compareSampleBtn');
  var errorEl = document.getElementById('compareError');
  var resultsEl = document.getElementById('compareResults');
  var announcer = document.getElementById('compareAnnouncer');

  // Loaded datasets: each { table, name } once a valid file is parsed.
  var slot = { A: null, B: null };

  function pct(x) { return (x * 100).toFixed(1) + '%'; }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function signed(x, dp) {
    var s = x.toFixed(dp === undefined ? 1 : dp);
    return (x > 0 ? '+' : '') + s;
  }
  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  // ── File wiring for one slot ('A' or 'B') ──────────────────────────────
  function wireSlot(key, drop, input, nameEl) {
    drop.addEventListener('click', function () { input.click(); });
    drop.addEventListener('keydown', function (e) {
      if (e.target !== drop) return;
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); }
    });
    input.addEventListener('change', function (e) {
      if (e.target.files && e.target.files[0]) readFile(key, e.target.files[0], drop, nameEl);
      drop.focus();
    });
    ['dragenter', 'dragover'].forEach(function (ev) {
      drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('dragover'); });
    });
    ['dragleave', 'drop'].forEach(function (ev) {
      drop.addEventListener(ev, function (e) {
        e.preventDefault();
        if (ev === 'dragleave' && drop.contains(e.relatedTarget)) return;
        drop.classList.remove('dragover');
      });
    });
    drop.addEventListener('drop', function (e) {
      var f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
      if (f) readFile(key, f, drop, nameEl);
    });
  }

  function readFile(key, file, drop, nameEl) {
    if (/\.xlsx$/i.test(file.name)) {
      return showError('Excel (.xlsx) isn\'t supported in the browser profiler yet - ' +
        'export to CSV/TSV first, or use the "faircode compare" CLI.');
    }
    var okExt = /\.(csv|tsv)$/i.test(file.name);
    var okType = file.type === 'text/csv' || file.type === 'text/tab-separated-values';
    if (!okExt && !okType) return showError('Please choose a .csv or .tsv file.');

    var reader = new FileReader();
    reader.onload = function () {
      try {
        var table = E.parseCSV(String(reader.result));
        if (!table.columns.length || !table.rows.length) {
          return showError('Dataset ' + key + ' looks empty or has no data rows.');
        }
        setSlot(key, table, file.name, drop, nameEl);
      } catch (err) {
        showError('Could not read dataset ' + key + ': ' + err.message);
      }
    };
    reader.onerror = function () { showError('Could not read dataset ' + key + '.'); };
    reader.readAsText(file);
  }

  function setSlot(key, table, name, drop, nameEl) {
    slot[key] = { table: table, name: name };
    nameEl.textContent = name;
    drop.classList.add('loaded');
    errorEl.hidden = true;
    maybeCompare();
  }

  function maybeCompare() {
    if (!slot.A || !slot.B) return;
    try {
      var cmp = E.compare(E.profile(slot.A.table), E.profile(slot.B.table),
                          slot.A.name, slot.B.name);
      errorEl.hidden = true;
      render(cmp);
    } catch (err) {
      showError('Could not compare those files: ' + err.message);
    }
  }

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.hidden = false;
    resultsEl.hidden = true;
  }

  // ── Rendering ──────────────────────────────────────────────────────────
  function render(cmp) {
    var d = cmp.score_delta;
    var deltaClass = d > 0 ? 'up' : d < 0 ? 'down' : 'flat';
    var arrow = d === 0 ? '=' : '→';

    var summary =
      '<div class="drift-summary">' +
        scoreCell(cmp.a) +
        '<div class="drift-arrow" aria-hidden="true">' + arrow + '</div>' +
        scoreCell(cmp.b) +
        '<div class="drift-delta ' + deltaClass + '">' +
          'score ' + signed(d, 0) + '</div>' +
      '</div>';

    var flags = '';
    if (cmp.flags.length) {
      flags = '<div class="flags-block" style="margin-top:24px">' +
        '<h3><span aria-hidden="true">⚑</span> Drift flags <span class="count">(' +
        cmp.flags.length + ')</span></h3><ul>' +
        cmp.flags.map(function (f) { return '<li>' + esc(f) + '</li>'; }).join('') +
        '</ul></div>';
    }

    var cards = cmp.dimensions.map(driftCard).join('');
    if (!cmp.dimensions.length) {
      cards = '<p class="section-note" style="margin-top:16px">No demographic dimension is ' +
        'present in both datasets, so there is nothing to compare directly.</p>';
    }

    var only = '';
    if (cmp.added_dimensions.length) {
      only += '<div class="drift-only">Only in B (' + esc(cmp.b.name) + '): <strong>' +
        cmp.added_dimensions.map(esc).join(', ') + '</strong></div>';
    }
    if (cmp.removed_dimensions.length) {
      only += '<div class="drift-only">Only in A (' + esc(cmp.a.name) + '): <strong>' +
        cmp.removed_dimensions.map(esc).join(', ') + '</strong></div>';
    }

    resultsEl.innerHTML = summary + flags + cards + only;
    resultsEl.hidden = false;
    resultsEl.scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'nearest' });

    announcer.textContent = 'Comparison complete. Overall score change ' + signed(d, 0) +
      ' points. ' + cmp.flags.length + ' drift flag' + (cmp.flags.length === 1 ? '' : 's') + '.';
  }

  function scoreCell(side) {
    return '<div class="drift-score"><span class="n">' + side.overall_score + '</span>' +
      '<span class="l">' + esc(side.name) + '</span></div>';
  }

  function driftCard(cd) {
    var head = '<div class="drift-card-head"><div>' +
      '<span class="dim-name">' + esc(cd.name) + '</span>' +
      '<span class="dim-kind">' + esc(cd.kind) + '</span>' +
      '<span class="drift-badge ' + cd.drift_level + '">' + cd.drift_level + ' drift</span>' +
      '</div><span class="drift-metrics">PSI ' + cd.psi.toFixed(3) +
      ' · TVD ' + cd.tvd.toFixed(3) +
      ' · score ' + cd.dimension_score_a + '→' + cd.dimension_score_b +
      ' (' + signed(cd.dimension_score_delta, 0) + ')</span></div>';

    // Scale bars to the largest share on either side, so shifts read visually.
    var maxShare = 0;
    cd.groups.forEach(function (g) {
      maxShare = Math.max(maxShare, g.share_a, g.share_b);
    });
    if (maxShare <= 0) maxShare = 1;

    var rows = cd.groups.slice(0, DISPLAY_GROUPS).map(function (g) {
      var cls = g.status === 'disappeared' ? ' gone' : g.status === 'appeared' ? ' new' : '';
      var wa = (g.share_a / maxShare) * 100;
      var wb = (g.share_b / maxShare) * 100;
      var deltaPP = g.share_delta * 100;
      var dCls = deltaPP > 0 ? 'up' : deltaPP < 0 ? 'down' : '';
      return '<div class="drift-row' + cls + '">' +
        '<span class="drift-row-label" title="' + esc(g.label) + '">' + esc(g.label) + '</span>' +
        '<span class="drift-bars" role="img" aria-label="' + pct(g.share_a) + ' to ' + pct(g.share_b) + '">' +
          '<span class="a" style="width:' + wa.toFixed(1) + '%"></span>' +
          '<span class="b" style="width:' + wb.toFixed(1) + '%"></span>' +
        '</span>' +
        '<span class="drift-row-delta">' + pct(g.share_a) + ' → ' + pct(g.share_b) +
          ' <span class="' + dCls + '">(' + signed(deltaPP) + 'pp)</span></span>' +
        '</div>';
    }).join('');

    var more = cd.groups.length > DISPLAY_GROUPS
      ? '<div class="dim-more">… and ' + (cd.groups.length - DISPLAY_GROUPS) + ' more groups</div>'
      : '';

    return '<div class="drift-card">' + head + rows + more + '</div>';
  }

  // ── Sample drift data ───────────────────────────────────────────────────
  // Baseline A is broadly balanced; current B drifts male-skewed, older, more
  // Caucasian, with one region collapsing and 'Asian' disappearing entirely -
  // so PSI clearly fires on race, age, sex, and region.
  function buildSample(key) {
    var header = ['patient_id', 'age', 'sex', 'race', 'region'];
    var rows = [header];
    var racesA = ['Caucasian', 'AfricanAmerican', 'Hispanic', 'Asian'];
    var racesB = ['Caucasian', 'Caucasian', 'Caucasian', 'AfricanAmerican', 'Hispanic'];
    var regionsA = ['Northeast', 'Midwest', 'South', 'West'];
    var regionsB = ['Northeast', 'Northeast', 'Midwest', 'South'];
    var agesA = [24, 29, 34, 41, 52, 63];
    var agesB = [38, 45, 52, 58, 64, 71];
    for (var i = 0; i < 300; i++) {
      var isB = key === 'B';
      var age = (isB ? agesB : agesA)[i % 6];
      var sex = isB ? (i % 10 < 7 ? 'male' : 'female') : (i % 2 === 0 ? 'male' : 'female');
      var race = (isB ? racesB : racesA)[i % (isB ? racesB.length : racesA.length)];
      var region = (isB ? regionsB : regionsA)[i % (isB ? regionsB.length : regionsA.length)];
      rows.push([String(1000 + i), String(age), sex, race, region]);
    }
    return rows.map(function (r) { return r.join(','); }).join('\n');
  }

  // ── Init ────────────────────────────────────────────────────────────────
  wireSlot('A', dropA, fileA, nameAEl);
  wireSlot('B', dropB, fileB, nameBEl);
  sampleBtn.addEventListener('click', function () {
    setSlot('A', E.parseCSV(buildSample('A')), 'sample-baseline.csv', dropA, nameAEl);
    setSlot('B', E.parseCSV(buildSample('B')), 'sample-current.csv', dropB, nameBEl);
  });
})();
