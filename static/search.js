(() => {
  const normalize = value => value.normalize('NFKD')
    .replace(/\p{M}/gu, '').toLocaleLowerCase()
    .replace(/[^\p{L}\p{N}+#]+/gu, ' ').trim().replace(/\s+/g, ' ');

  function terms(query) {
    const result = [];
    for (const match of query.replace(/[“”]/g, '"').matchAll(/"([^"]+)"|(\S+)/gu)) {
      const value = normalize(match[1] ?? match[2]);
      if (!value) continue;
      // Quoted text stays together; other words can appear in any order.
      result.push(...(match[1] === undefined ? value.split(' ') : [value]));
    }
    return [...new Set(result)];
  }

  function showEmptyState(element, visible, title, message, headingTag = 'h3') {
    if (visible && !element.firstChild) {
      const heading = document.createElement(headingTag);
      const paragraph = document.createElement('p');
      heading.textContent = title;
      paragraph.textContent = message;
      element.append(heading, paragraph);
    } else if (!visible) {
      element.replaceChildren();
    }
    element.hidden = !visible;
  }

  window.AICanWhatSearch = Object.freeze({ normalize, terms, showEmptyState });
})();
