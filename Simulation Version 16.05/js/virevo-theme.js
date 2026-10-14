(function () {
  function getTheme() {
    const saved = localStorage.getItem('virevo-theme');
    return saved || document.documentElement.getAttribute('data-theme') || 'dark';
  }

  function setActiveOption(theme) {
    document.querySelectorAll('.virevo-theme-option').forEach(function (option) {
      option.classList.toggle('active', option.getAttribute('data-theme') === theme);
    });
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('virevo-theme', theme);
    setActiveOption(theme);
  }

  function initThemeControl() {
    const wrapper = document.querySelector('.virevo-theme-wrapper');
    const btn = document.getElementById('virevoThemeBtn');
    const dropdown = document.getElementById('virevoThemeDropdown');

    if (!wrapper || !btn || !dropdown) {
      return;
    }

    setTheme(getTheme());

    btn.addEventListener('click', function (event) {
      event.stopPropagation();
      dropdown.classList.toggle('open');
    });

    document.addEventListener('click', function (event) {
      if (!wrapper.contains(event.target)) {
        dropdown.classList.remove('open');
      }
    });

    dropdown.addEventListener('click', function (event) {
      const option = event.target.closest('.virevo-theme-option');
      if (!option) {
        return;
      }
      setTheme(option.getAttribute('data-theme'));
      dropdown.classList.remove('open');
    });
  }

  document.documentElement.setAttribute('data-theme', getTheme());

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initThemeControl);
  } else {
    initThemeControl();
  }
})();
