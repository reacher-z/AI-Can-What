(() => {
  const search = document.querySelector('#paper-search');
  if (!search) return;
  const source = document.querySelector('#paper-source');
  const status = document.querySelector('#paper-status');
  const year = document.querySelector('#paper-year');
  const count = document.querySelector('#paper-count');
  const reset = document.querySelector('#paper-reset');
  const empty = document.querySelector('#paper-empty');
  const rows = [...document.querySelectorAll('[data-paper]')];
  const textByRow = new Map(rows.map(row => [row, AICanWhatSearch.normalize(row.dataset.search)]));
  const zh = document.documentElement.lang === 'zh-CN';
  const parameters = new URL(location.href).searchParams;
  search.value = parameters.get('q') || '';
  for (const [control, key] of [[source, 'source'], [status, 'status'], [year, 'year']]) {
    const value = parameters.get(key);
    if ([...control.options].some(option => option.value === value)) control.value = value;
  }
  function update() {
    const query = search.value.trim();
    const terms = AICanWhatSearch.terms(query);
    let visible = 0;
    for (const row of rows) {
      const matches = terms.every(term => textByRow.get(row).includes(term)) &&
        (!source.value || source.value === row.dataset.source) &&
        (!status.value || status.value === row.dataset.catalogStatus) &&
        (!year.value || year.value === row.dataset.year);
      row.hidden = !matches;
      if (matches) visible++;
    }
    count.textContent = zh ? `显示 ${visible} / ${rows.length} 篇文献` : `${visible} of ${rows.length} papers`;
    empty.hidden = visible !== 0;
    reset.hidden = !query && !source.value && !status.value && !year.value;
    const next = new URL(location.href);
    for (const [key, value] of [['q', query], ['source', source.value], ['status', status.value], ['year', year.value]]) {
      if (value) next.searchParams.set(key, value); else next.searchParams.delete(key);
    }
    history.replaceState(null, '', next);
  }
  search.addEventListener('input', update);
  for (const control of [source, status, year]) control.addEventListener('change', update);
  reset.addEventListener('click', () => {
    search.value = ''; source.value = ''; status.value = ''; year.value = '';
    update(); search.focus();
  });
  update();
})();
