(() => {
  const search = document.querySelector('#catalog-search');
  if (!search) return;
  const rows = [...document.querySelectorAll('[data-project]')];
  const use = document.querySelector('#use-filter');
  const platform = document.querySelector('#platform-filter');
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#empty-state');
  const reset = document.querySelector('#reset-filters');
  const zh = document.documentElement.lang === 'zh-CN';
  const params = new URL(location.href).searchParams;
  search.value = params.get('q') || '';
  for (const [element, key] of [[use, 'use'], [platform, 'platform']]) {
    const value = params.get(key);
    if ([...element.options].some(option => option.value === value)) element.value = value;
  }
  function update() {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const row of rows) {
      const matches = (!query || row.dataset.search.includes(query)) &&
        (!use.value || row.dataset.uses.split(' ').includes(use.value)) &&
        (!platform.value || row.dataset.platforms.split(' ').includes(platform.value));
      row.hidden = !matches;
      if (matches) visible++;
    }
    count.textContent = zh ? `显示 ${visible} / ${rows.length} 个项目` : `${visible} of ${rows.length} projects`;
    empty.hidden = visible !== 0;
    reset.hidden = !query && !use.value && !platform.value;
    const next = new URL(location.href);
    for (const [key, value] of [['q', search.value.trim()], ['use', use.value], ['platform', platform.value]]) {
      if (value) next.searchParams.set(key, value); else next.searchParams.delete(key);
    }
    history.replaceState(null, '', next);
  }
  search.addEventListener('input', update);
  use.addEventListener('change', update);
  platform.addEventListener('change', update);
  reset.addEventListener('click', () => { search.value = ''; use.value = ''; platform.value = ''; update(); search.focus(); });
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !event.metaKey && !event.ctrlKey && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) {
      event.preventDefault(); search.focus();
    }
  });
  update();
})();
