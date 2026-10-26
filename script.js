const projectList = document.getElementById('project-list');

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  }[character]));
}

function renderProjects(projects) {
  if (!projects.length) {
    projectList.innerHTML = '<article class="project-card project-placeholder"><div><span class="project-label">Project directory</span><h3>No published projects yet</h3><p>Published research websites will appear here automatically.</p></div></article>';
    return;
  }

  projectList.innerHTML = projects.map((project) => `
    <article class="project-card">
      <div>
        <span class="project-label">${escapeHtml(project.year || 'Research project')}</span>
        <h3>${escapeHtml(project.title)}</h3>
        <p>${escapeHtml(project.description)}</p>
        <small>${escapeHtml(project.authors.join(' · '))}</small>
        <div class="project-links">
          <a class="button button-small" href="${escapeHtml(project.url)}">View project ↗</a>
          <a class="project-source" href="${escapeHtml(project.repository)}">Source code ↗</a>
        </div>
      </div>
    </article>
  `).join('');
}

fetch('data/projects.json')
  .then((response) => {
    if (!response.ok) {
      throw new Error(`Project registry request failed: ${response.status}`);
    }
    return response.json();
  })
  .then(renderProjects)
  .catch((error) => {
    console.error(error);
    projectList.innerHTML = '<article class="project-card project-placeholder"><div><span class="project-label">Project directory</span><h3>Project list temporarily unavailable</h3><p>Please check back later.</p></div></article>';
  });
