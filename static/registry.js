(() => {
  const search = document.querySelector('#registry-search');
  if (!search) return;
  const source = document.querySelector('#registry-source');
  const notes = document.querySelector('#registry-notes');
  const version = document.querySelector('#registry-version');
  const count = document.querySelector('#registry-count');
  const reset = document.querySelector('#registry-reset');
  const empty = document.querySelector('#registry-empty');
  const rows = [...document.querySelectorAll('[data-registry]')];
  const textByRow = new Map(rows.map(row => [row, AICanWhatSearch.normalize(row.dataset.search)]));
  const zh = document.documentElement.lang === 'zh-CN';
  const parameters = new URL(location.href).searchParams;
  search.value = parameters.get('q') || '';
  for (const [control, key] of [[source, 'source'], [notes, 'notes'], [version, 'version']]) {
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
        (!notes.value || notes.value === row.dataset.notes) &&
        (!version.value || version.value === row.dataset.versionStatus);
      row.hidden = !matches;
      if (matches) visible++;
    }
    count.textContent = zh ? `显示 ${visible} / ${rows.length} 条来源记录` : `${visible} of ${rows.length} source records`;
    AICanWhatSearch.showEmptyState(empty, visible === 0,
      zh ? '没有匹配的记录。' : 'No matching records.',
      zh ? '修改关键词或重置筛选。' : 'Change your search or reset the filters.');
    reset.hidden = !query && !source.value && !notes.value && !version.value;
    const next = new URL(location.href);
    for (const [key, value] of [['q', search.value.trim()], ['source', source.value], ['notes', notes.value], ['version', version.value]]) {
      if (value) next.searchParams.set(key, value); else next.searchParams.delete(key);
    }
    history.replaceState(null, '', next);
  }
  search.addEventListener('input', update);
  for (const control of [source, notes, version]) control.addEventListener('change', update);
  reset.addEventListener('click', () => {
    search.value = ''; source.value = ''; notes.value = ''; version.value = '';
    update(); search.focus();
  });
  update();
})();
