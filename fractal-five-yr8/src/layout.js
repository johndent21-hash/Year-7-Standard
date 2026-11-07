// Runs inside each booklet page: places question bodies under their prompts,
// scales diagrams/tables to fit the cell, shrinks long formula text, and
// records any overflow so the build can report it.
(function () {
  const PT = 96 / 72;
  function flowRefs(warns) {
    const g1 = document.querySelector('.refgrid[data-flow="1"]');
    const g2 = document.querySelector('.refgrid[data-flow="2"]');
    if (!g1 || !g2) return;
    const limit = 788 * PT;
    const bottom = el => { const pg = el.closest('.page'); return el.getBoundingClientRect().bottom - pg.getBoundingClientRect().top; };
    let guard = 0;
    while (bottom(g1.parentElement) > limit && g1.lastElementChild && guard++ < 200) {
      const last = g1.lastElementChild;
      g2.insertBefore(last, g2.firstElementChild);
      // never leave a heading stranded at the bottom of page 1
      const tail = g1.lastElementChild;
      if (tail && tail.classList.contains('refgroup')) g2.insertBefore(tail, g2.firstElementChild);
    }
    const first = g2.firstElementChild;
    if (first && first.classList.contains('refitem')) {
      const g = first.dataset.g;
      const h = g1.querySelector('.refgroup[data-g="' + g + '"]');
      const c = document.createElement('div');
      c.className = 'refgroup'; c.dataset.g = g;
      c.textContent = (h ? h.dataset.name : '') + ' (CONTINUED)';
      g2.insertBefore(c, first);
    }
    if (bottom(g2.parentElement) > limit) warns.push('reference page 2 overflows');
  }
  function flowAnswers(warns) {
    const boxes = Array.from(document.querySelectorAll('.ans-wrap[data-flow]'));
    if (!boxes.length) return;
    const limit = 788 * PT;
    const bottom = el => { const pg = el.closest('.page'); return el.getBoundingClientRect().bottom - pg.getBoundingClientRect().top; };
    for (let k = 0; k < boxes.length - 1; k++) {
      let guard = 0;
      while (bottom(boxes[k]) > limit && boxes[k].lastElementChild && guard++ < 50) {
        boxes[k + 1].insertBefore(boxes[k].lastElementChild, boxes[k + 1].firstElementChild);
      }
    }
    if (bottom(boxes[boxes.length - 1]) > limit) warns.push('answers overflow the last page');
    boxes.forEach(b => { if (!b.children.length) b.closest('.page').style.display = 'none'; });
  }
  function fit() {
    const warns = [];
    flowRefs(warns);
    flowAnswers(warns);
    document.querySelectorAll('.qrow').forEach(row => {
      const id = row.dataset.id || '';
      const p = row.querySelector('.prompt');
      const b = row.querySelector('.qbody');
      const rowH = row.clientHeight;
      if (p && p.scrollHeight > p.clientHeight + 2 && p.style.height) warns.push(id + ' prompt overflow');
      if (b) {
        const top = (p ? p.offsetTop + p.offsetHeight : 12 * PT) + 5 * PT;
        const bottom = rowH - 7 * PT;
        const availH = bottom - top;
        b.style.top = top + 'px';
        b.style.height = availH + 'px';
        const child = b.firstElementChild;
        if (child) {
          const r = child.getBoundingClientRect();
          const availW = b.clientWidth - 6;
          const s = Math.min(1, availH / r.height, availW / r.width);
          if (s < 1) {
            if (child.tagName.toLowerCase() === 'svg') {
              child.setAttribute('width', (r.width * s) + 'px');
              child.setAttribute('height', (r.height * s) + 'px');
            } else {
              child.style.transform = 'scale(' + s + ')';
              child.style.transformOrigin = 'center center';
            }
            if (s < 0.72) warns.push(id + ' body scaled to ' + s.toFixed(2));
          }
          if (availH < 18) warns.push(id + ' little room for body (' + (availH / PT).toFixed(1) + 'pt)');
        }
      }
      const fb = row.querySelector('.fbox');
      if (fb) {
        const ft = fb.querySelector('.ftxt');
        if (fb.offsetHeight > 26.5 * PT && !ft.classList.contains('sm')) ft.classList.add('sm');
        if (fb.offsetHeight > 26.5 * PT) { ft.style.fontSize = '8pt'; ft.style.lineHeight = '9.6pt'; }
        if (fb.offsetHeight > 30 * PT) warns.push(id + ' formula box too tall (' + (fb.offsetHeight / PT).toFixed(1) + 'pt)');
      }
    });
    document.querySelectorAll('.page').forEach((pg, i) => {
      if (pg.scrollHeight > pg.clientHeight + 2) warns.push('page ' + (i + 1) + ' overflows');
    });
    document.querySelectorAll('.panel').forEach((el, i) => {
      const pg = el.closest('.page');
      const bottomLimit = 790 * PT;
      if (el.offsetTop + el.offsetHeight > bottomLimit) warns.push('panel on page ' + (Array.from(document.querySelectorAll('.page')).indexOf(pg) + 1) + ' runs into the footer');
    });
    document.body.dataset.warn = warns.join('\n');
    document.body.dataset.ready = '1';
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => setTimeout(fit, 50));
  else window.addEventListener('load', fit);
})();
