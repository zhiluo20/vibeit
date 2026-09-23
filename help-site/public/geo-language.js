(() => {
  const base = '/vibeit/help/';
  const locales = new Set(['en', 'fr', 'de', 'th', 'ja', 'ko', 'zh-hans', 'zh-hant', 'es', 'ar', 'it']);
  const countryLocales = {
    CN: 'zh-hans', HK: 'zh-hant', MO: 'zh-hant', TW: 'zh-hant',
    JP: 'ja', KR: 'ko', KP: 'ko',
    FR: 'fr', MC: 'fr', BE: 'fr', LU: 'fr',
    IT: 'it', SM: 'it', VA: 'it',
    DE: 'de', AT: 'de', CH: 'de', LI: 'de',
    ES: 'es', MX: 'es', AR: 'es', CL: 'es', CO: 'es', PE: 'es',
    VE: 'es', EC: 'es', GT: 'es', CU: 'es', BO: 'es', DO: 'es',
    HN: 'es', PY: 'es', SV: 'es', NI: 'es', CR: 'es', PA: 'es',
    UY: 'es', GQ: 'es', PR: 'es',
    SA: 'ar', AE: 'ar', EG: 'ar', QA: 'ar', KW: 'ar', BH: 'ar', OM: 'ar',
    JO: 'ar', IQ: 'ar', LB: 'ar', LY: 'ar', DZ: 'ar', MA: 'ar', TN: 'ar',
    YE: 'ar', SD: 'ar', SY: 'ar', PS: 'ar', MR: 'ar',
    TH: 'th',
  };

  function normalize(value) {
    const language = String(value || '').toLowerCase();
    if (language.startsWith('zh')) {
      return /(?:hant|tw|hk|mo)/.test(language) ? 'zh-hant' : 'zh-hans';
    }
    const short = language.split('-')[0];
    return locales.has(short) ? short : '';
  }

  function preference() {
    try {
      return normalize(localStorage.getItem('vibeit_help_lang')) ||
        normalize(localStorage.getItem('vibeit_lang'));
    } catch {
      return '';
    }
  }

  // Starlight navigates as soon as its select changes. Save the choice first.
  document.addEventListener('change', (event) => {
    const select = event.target;
    if (!(select instanceof HTMLSelectElement) || !select.closest('starlight-lang-select')) return;
    const path = new URL(select.value, location.href).pathname;
    if (!path.startsWith(base)) return;
    const segment = path.slice(base.length).split('/')[0];
    const locale = locales.has(segment) ? segment : 'en';
    try { localStorage.setItem('vibeit_help_lang', locale); } catch {}
  }, true);

  // A localized article URL is an explicit choice; only the language-neutral entry redirects.
  if (location.pathname !== base && location.pathname !== base.slice(0, -1)) return;

  function show(locale) {
    if (!locale || locale === 'en') return;
    location.replace(base + locale + '/' + location.search + location.hash);
  }

  const saved = preference();
  if (saved) { show(saved); return; }

  function browserLocale() {
    const languages = navigator.languages?.length ? navigator.languages : [navigator.language];
    for (const language of languages) {
      const locale = normalize(language);
      if (locale) return locale;
    }
    return 'en';
  }

  async function country() {
    try {
      const cached = sessionStorage.getItem('vibeit_country');
      if (/^[A-Z]{2}$/.test(cached || '')) return cached;
    } catch {}
    if (!window.fetch || !window.AbortController) return '';
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 4000);
    try {
      const response = await fetch('https://get.geojs.io/v1/ip/country.json', {
        signal: controller.signal,
        cache: 'no-store',
        referrerPolicy: 'strict-origin-when-cross-origin',
      });
      if (!response.ok) return '';
      const code = String((await response.json()).country || '').toUpperCase();
      if (!/^[A-Z]{2}$/.test(code)) return '';
      try { sessionStorage.setItem('vibeit_country', code); } catch {}
      return code;
    } catch {
      return '';
    } finally {
      clearTimeout(timeout);
    }
  }

  country().then((code) => {
    // A visitor may have selected a language while the IP lookup was pending.
    show(preference() || countryLocales[code] || browserLocale());
  });
})();
