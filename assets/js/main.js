/* ============================================================
   The Nigerian Entrepreneur — site behaviour
   Vanilla JS, no dependencies.
   ============================================================ */
(function () {
  'use strict';

  var $  = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ---------------------------------------------------------
     Toast helper
     --------------------------------------------------------- */
  var toastEl = $('.toast');
  var toastTimer;

  function toast(message) {
    if (!toastEl) return;
    toastEl.textContent = message;
    toastEl.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toastEl.classList.remove('is-visible');
    }, 2800);
  }

  /* ---------------------------------------------------------
     Header: dropdown menus (desktop) / accordion (mobile)
     --------------------------------------------------------- */
  var nav = $('#nav');
  var navToggle = $('#navToggle');
  var menuItems = $$('.nav__item.has-menu');

  function closeAllMenus(except) {
    menuItems.forEach(function (item) {
      if (item !== except) item.classList.remove('is-open');
    });
  }

  menuItems.forEach(function (item) {
    var trigger = $('.nav__trigger', item);
    if (!trigger) return;

    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = item.classList.contains('is-open');
      closeAllMenus(item);
      item.classList.toggle('is-open', !isOpen);
      trigger.setAttribute('aria-expanded', String(!isOpen));
    });
  });

  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(open));
      navToggle.innerHTML = open
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>';
    });
  }

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav__item')) closeAllMenus(null);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeAllMenus(null);
      if (nav) nav.classList.remove('is-open');
      var panel = $('#searchPanel');
      if (panel) panel.classList.remove('is-open');
    }
  });

  /* ---------------------------------------------------------
     Search panel
     --------------------------------------------------------- */
  var searchToggle = $('#searchToggle');
  var searchPanel  = $('#searchPanel');

  if (searchToggle && searchPanel) {
    searchToggle.addEventListener('click', function () {
      var open = searchPanel.classList.toggle('is-open');
      if (open) {
        var input = $('input', searchPanel);
        if (input) setTimeout(function () { input.focus(); }, 60);
      }
    });
  }

  $$('form[data-search]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = ($('input', form) || {}).value || '';
      if (!q.trim()) { toast('Type something to search first.'); return; }
      toast('Searching the site for “' + q.trim() + '”…');
    });
  });

  /* ---------------------------------------------------------
     Category chip filters
     --------------------------------------------------------- */
  $$('[data-filter-group]').forEach(function (group) {
    var targetSel = group.getAttribute('data-filter-group');
    var scope     = targetSel === 'this' ? group.closest('[data-filter-scope]') : document;
    var items     = $$('[data-tags]', scope);
    var chips     = $$('.chip', group);
    var empty     = $('[data-empty]', scope);

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        chips.forEach(function (c) { c.classList.remove('is-active'); });
        chip.classList.add('is-active');

        var value = chip.getAttribute('data-filter');
        var shown = 0;

        items.forEach(function (item) {
          var tags = (item.getAttribute('data-tags') || '').toLowerCase();
          var match = value === 'all' || tags.split(/\s+/).indexOf(value.toLowerCase()) > -1;
          item.style.display = match ? '' : 'none';
          if (match) shown++;
        });

        if (empty) empty.hidden = shown !== 0;
      });
    });
  });

  /* ---------------------------------------------------------
     "Load more" reveal
     --------------------------------------------------------- */
  $$('[data-more-btn]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var scope = btn.closest('[data-more-scope]') || document;
      var hidden = $$('[data-more-item][hidden]', scope);
      var batch = hidden.slice(0, 4);

      batch.forEach(function (item) {
        item.hidden = false;
        item.classList.add('reveal', 'is-in');
      });

      if (hidden.length <= batch.length) btn.remove();
      else toast('Showing more articles');

      // keep any active filter applied to the newly revealed items
      var activeChip = $('.chip.is-active');
      if (activeChip && activeChip.getAttribute('data-filter') !== 'all') activeChip.click();
    });
  });

  /* ---------------------------------------------------------
     Forms: newsletter / subscribe / contact
     --------------------------------------------------------- */
  var emailPattern = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;

  function validEmail(value) { return emailPattern.test(value.trim()); }

  $$('form[data-newsletter]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = $('input[type="email"]', form);
      var status = $('[data-form-status]', form);
      var value = input ? input.value : '';

      if (!validEmail(value)) {
        if (status) { status.textContent = 'Please enter a valid email address.'; status.style.color = '#dc2626'; status.classList.add('is-visible'); }
        if (input) input.focus();
        return;
      }

      if (status) { status.textContent = 'You’re on the list! Check your inbox to confirm.'; status.style.color = ''; status.classList.add('is-visible'); }
      form.reset();
      toast('Subscribed — welcome aboard!');
    });
  });

  $$('form[data-contact]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = $('[data-form-status]', form);
      var required = $$('[required]', form);
      var firstBad = null;

      required.forEach(function (field) {
        var ok = field.type === 'checkbox' ? field.checked : field.value.trim() !== '';
        field.style.borderColor = ok ? '' : '#ef4444';
        if (!ok && !firstBad) firstBad = field;
      });

      var emailField = $('input[type="email"]', form);
      if (emailField && !validEmail(emailField.value)) {
        emailField.style.borderColor = '#ef4444';
        if (!firstBad) firstBad = emailField;
      }

      if (firstBad) {
        if (status) { status.textContent = 'Please complete the highlighted fields.'; status.style.color = '#dc2626'; status.classList.add('is-visible'); }
        firstBad.focus();
        return;
      }

      if (status) { status.textContent = 'Thank you! Your message has been sent — we usually reply within one business day.'; status.style.color = ''; status.classList.add('is-visible'); }
      form.reset();
      toast('Message sent successfully');
    });

    $$('input, select, textarea', form).forEach(function (field) {
      field.addEventListener('input', function () { field.style.borderColor = ''; });
    });
  });

  /* ---------------------------------------------------------
     Share / copy link
     --------------------------------------------------------- */
  var copyBtn = $('[data-copy-link]');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      var url = window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () { toast('Link copied to clipboard'); });
      } else {
        var tmp = document.createElement('input');
        tmp.value = url;
        document.body.appendChild(tmp);
        tmp.select();
        try { document.execCommand('copy'); toast('Link copied to clipboard'); }
        catch (err) { toast('Copy failed — please copy the address bar'); }
        document.body.removeChild(tmp);
      }
    });
  }

  /* ---------------------------------------------------------
     Reveal on scroll (with a safety net so content can never
     stay hidden if an observer callback is missed)
     --------------------------------------------------------- */
  var revealables = $$('.reveal');
  var revealAll = function () {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
  };

  if ('IntersectionObserver' in window && revealables.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -60px 0px', threshold: .08 });

    revealables.forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i % 6, 5) * 60 + 'ms';
      io.observe(el);
    });

    setTimeout(revealAll, 1600);
  }

  /* ---------------------------------------------------------
     Inline CTA subscribe buttons (CTA bands on category pages)
     --------------------------------------------------------- */
  window.TNE_subscribe = function (btn) {
    var wrap = btn.closest('.cta__form');
    var input = wrap ? $('input', wrap) : null;
    var value = input ? input.value : '';

    if (!validEmail(value)) {
      toast('Please enter a valid email address.');
      if (input) input.focus();
      return;
    }
    if (input) input.value = '';
    toast('Subscribed — you’ll hear from us soon!');
  };

  /* ---------------------------------------------------------
     Custom toast events (used by inline buttons)
     --------------------------------------------------------- */
  document.addEventListener('tne:toast', function (e) {
    toast(e.detail || 'Done');
  });

  /* ---------------------------------------------------------
     Back to top
     --------------------------------------------------------- */
  var toTop = $('.to-top');
  if (toTop) {
    window.addEventListener('scroll', function () {
      toTop.classList.toggle('is-visible', window.scrollY > 500);
    }, { passive: true });

    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------------------------------------------------------
     Scroll-spy for legal page table of contents
     --------------------------------------------------------- */
  var tocLinks = $$('[data-spy] a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var sections = tocLinks
      .map(function (link) { return document.getElementById(link.getAttribute('href').slice(1)); })
      .filter(Boolean);

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        tocLinks.forEach(function (l) {
          l.classList.toggle('is-active', l.getAttribute('href') === '#' + entry.target.id);
        });
      });
    }, { rootMargin: '-90px 0px -70% 0px' });

    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------------------------------------------------------
     Footer year
     --------------------------------------------------------- */
  $$('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------------------------------------------------------
     404: search -> go home with query
     --------------------------------------------------------- */
  var nfForm = $('#nfSearch');
  if (nfForm) {
    nfForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = ($('input', nfForm) || {}).value || '';
      toast(q.trim() ? 'Searching for “' + q.trim() + '”…' : 'Type something to search first.');
    });
  }
})();
