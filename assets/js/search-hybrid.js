// File: assets/js/search-hybrid.js

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('search-input');
  const searchButton = document.getElementById('search-button');
  const resultsContainer = document.getElementById('search-results');

  function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function buildWordRegex(query) {
    const escaped = escapeRegex(query);
    // Matches exact words and hyphenated terms
    return new RegExp(`(?<![\\w-])(${escaped})(?![\\w-])`, 'gi');
  }

  function highlight(text, query) {
    if (!query) return text;
    const regex = buildWordRegex(query);
    return text.replace(regex, '<mark>$1</mark>');
  }

  function performSearch() {
    const rawQuery = searchInput.value.trim();
    if (!rawQuery) {
      resultsContainer.innerHTML = '';
      return;
    }

    const query = rawQuery.toLowerCase();
    const wordRegex = buildWordRegex(query);

    const results = window.posts.filter(post => {
      const title = post.title.toLowerCase();
      const content = post.content.toLowerCase();
      return wordRegex.test(title) || wordRegex.test(content);
    });

    renderResults(results, query);
  }

  function getSnippet(content, query, length = 100) {
    const regex = buildWordRegex(query);
    const match = regex.exec(content.toLowerCase());
    if (!match) return content.substring(0, length) + '...';

    const index = match.index;
    const start = Math.max(0, index - 30);
    const end = Math.min(content.length, index + query.length + 70);
    return '...' + content.substring(start, end) + '...';
  }

  function renderResults(results, query) {
    if (!results.length) {
      resultsContainer.innerHTML = '<div class="no-results">No matching posts found</div>';
      return;
    }

    let html = '<ul class="search-results-list">';
    results.forEach(post => {
      const highlightedTitle = highlight(post.title, query);
      const snippet = getSnippet(post.content, query);
      const highlightedSnippet = highlight(snippet, query);

      html += `
        <li class="search-result-item">
          <a href="${post.url}" class="search-result-link">
            <span class="result-filename">${post.filename}</span>
            <span class="result-title">${highlightedTitle}</span>
            <div class="result-snippet">${highlightedSnippet}</div>
          </a>
        </li>
      `;
    });
    html += '</ul>';

    resultsContainer.innerHTML = html;
  }

  searchButton.addEventListener('click', performSearch);
  searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
  });
});
