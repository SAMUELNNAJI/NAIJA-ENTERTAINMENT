/* ============================================================
   The Nigerian Entrepreneur — site behaviour
   Vanilla JS, no dependencies.
   ============================================================ */
(function () {
  'use strict';

  var $  = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* Official contact destinations used by every reusable social-icon row. */
  var officialLinks = {
    's-x': 'https://x.com/tneforafrica',
    's-yt': 'https://www.youtube.com/@Thenigerianentrepreneur',
    's-ig': 'https://www.instagram.com/the_nigerian_entrepreneur/',
    's-wa': 'https://wa.me/2349040649218'
  };
  Object.keys(officialLinks).forEach(function (className) {
    $$('a.' + className).forEach(function (link) {
      link.href = officialLinks[className];
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
    });
  });

  /* Sponsor campaigns rotate through active banners; dismissal lasts this browser session. */
  (function () {
    var banner = document.querySelector('[data-sponsor-banner]');
    if (!banner || sessionStorage.getItem('tne-sponsor-closed')) return;
    var slides = Array.prototype.slice.call(banner.querySelectorAll('[data-sponsor-slide]'));
    if (!slides.length) return;
    banner.hidden = false;
    var index = Math.floor(Math.random() * slides.length);
    function show(n) { slides.forEach(function (slide, i) { slide.hidden = i !== n; slide.classList.toggle('is-active', i === n); }); }
    show(index);
    if (slides.length > 1) setInterval(function () { index = (index + 1) % slides.length; show(index); }, 7000);
    banner.querySelector('[data-sponsor-close]').addEventListener('click', function () { banner.hidden = true; sessionStorage.setItem('tne-sponsor-closed', '1'); });
  })();
  $$('a[href="tel:+2348000000000"]').forEach(function (link) {
    link.href = 'tel:+2349040649218';
    link.textContent = '0904 064 9218';
  });

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
     Theme toggle (light / dark)
     --------------------------------------------------------- */
  var themeBtn = $('#themeToggle');
  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    if (themeBtn) {
      themeBtn.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false');
      themeBtn.setAttribute('aria-label', t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    }
  }
  applyTheme(document.documentElement.getAttribute('data-theme') || 'light');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
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

  var navBackdrop = $('#navBackdrop');
  var navClose = $('#navClose');

  function setDrawer(open) {
    if (!nav || !navToggle) return;
    nav.classList.toggle('is-open', open);
    navToggle.classList.toggle('is-open', open);
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (navBackdrop) navBackdrop.hidden = !open;
    document.documentElement.classList.toggle('no-scroll', open);
    if (!open) closeAllMenus(null);
  }

  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      setDrawer(!nav.classList.contains('is-open'));
    });
    if (navBackdrop) navBackdrop.addEventListener('click', function () { setDrawer(false); });
    if (navClose) navClose.addEventListener('click', function () { setDrawer(false); });
    $$('a', nav).forEach(function (a) {
      a.addEventListener('click', function () { setDrawer(false); });
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1100 && nav.classList.contains('is-open')) setDrawer(false);
    });
  }

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav__item')) closeAllMenus(null);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeAllMenus(null);
      setDrawer(false);
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
      // Real site search: the form carries the action (/search/ by default)
      // so pages with static search markup keep working too.
      var action = form.getAttribute('action') || '/search/';
      window.location.href = action + '?q=' + encodeURIComponent(q.trim());
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
          // Extra cards are hidden in the default home feed, but
          // become available whenever their category is selected.
          var isExtra = item.hasAttribute('data-filter-extra');
          var shouldShow = match && !(value === 'all' && isExtra);
          item.hidden = !shouldShow;
          item.style.display = shouldShow ? '' : 'none';
          if (shouldShow) shown++;
        });

        if (empty) empty.hidden = shown !== 0;
      });
    });
  });

  /* ---------------------------------------------------------
     Deep links: honour ?filter=<value> in the URL so header /
     footer category links land with the right chip active
     instead of always showing "All".
     --------------------------------------------------------- */
  try {
    var initialFilter = new URLSearchParams(window.location.search).get('filter');
    if (initialFilter) {
      initialFilter = initialFilter.toLowerCase();
      var deepLinkChip = $$('.chip[data-filter]').filter(function (c) {
        return (c.getAttribute('data-filter') || '').toLowerCase() === initialFilter;
      })[0];
      if (deepLinkChip) deepLinkChip.click();
    }
  } catch (e) {}

  /* ---------------------------------------------------------
     "Load more" reveal
     --------------------------------------------------------- */
  $$('[data-more-btn]').forEach(function (btn) {
    // The button sits below the card grid, so use the surrounding page
    // filter scope rather than the button's own wrapper.
    var scope = btn.closest('[data-filter-scope]') || btn.closest('[data-more-scope]') || document;

    // Nothing left to reveal (section already fully loaded) — hide the button.
    if (!$$('[data-more-item][hidden]', scope).length) { btn.remove(); return; }

    btn.addEventListener('click', function () {
      var hidden = $$('[data-more-item][hidden]', scope);
      var size  = parseInt(btn.getAttribute('data-batch'), 10) || 4;
      var batch = hidden.slice(0, size);

      batch.forEach(function (item) {
        item.hidden = false;
        item.classList.add('reveal', 'is-in');
      });

      // Remove the button once the last batch has been revealed so it never
      // lingers with nothing left to load.
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
     Category cards — mad coverflow carousel
     Progressively enhances the static .cat-cards grid inside any
     [data-carousel] section into a 3D, draggable, auto-rotating
     carousel. Leaves the accessible grid untouched for no-JS and
     reduced-motion visitors.
     --------------------------------------------------------- */
  function initCategoryCarousel(track) {
    var slides = $$('.cat-card', track);
    var n = slides.length;
    if (n < 3) return;

    // Carousel cards own their positioning via JS transforms.
    // Remove reveal-animation hooks so hover/focus can never trigger
    // a conflicting transform or transition-delay from the reveal system.
    slides.forEach(function (slide) {
      slide.classList.remove('reveal');
      slide.classList.add('is-in');
      slide.style.transitionDelay = '0ms';
    });

    var wrap = document.createElement('div');
    wrap.className = 'carousel';
    wrap.setAttribute('tabindex', '0');
    wrap.setAttribute('role', 'region');
    wrap.setAttribute('aria-roledescription', 'carousel');
    wrap.setAttribute('aria-label', 'Browse categories');
    track.parentNode.insertBefore(wrap, track);
    wrap.appendChild(track);
    track.classList.add('cat-cards--carousel');

    function arrowBtn(dir, label, path) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'carousel__arrow carousel__arrow--' + dir;
      b.setAttribute('aria-label', label);
      b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + path + '"/></svg>';
      return b;
    }
    var prevBtn = arrowBtn('prev', 'Previous category', 'M15 6l-6 6 6 6');
    var nextBtn = arrowBtn('next', 'Next category', 'M9 6l6 6-6 6');
    wrap.appendChild(prevBtn);
    wrap.appendChild(nextBtn);

    var dots = document.createElement('div');
    dots.className = 'carousel__dots';
    dots.setAttribute('role', 'tablist');
    dots.setAttribute('aria-label', 'Category slides');
    var dotEls = slides.map(function (slide, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'carousel__dot';
      var title = $('h3', slide);
      b.setAttribute('aria-label', 'Show ' + (title ? title.textContent : 'slide ' + (i + 1)));
      b.addEventListener('click', function () { goTo(i); kick(); });
      dots.appendChild(b);
      return b;
    });
    wrap.appendChild(dots);

    var current = 0;

    function layout() {
      var w = wrap.clientWidth || 900;
      var spacing = Math.max(130, Math.min(w * 0.23, 260));
      slides.forEach(function (slide, i) {
        var d = i - current;
        d = ((d % n) + n) % n;
        if (d > n / 2) d -= n;
        var ad = Math.abs(d);
        var tx = d * spacing;
        var tz = -ad * 170;
        var ry = d * -28;
        var sc = Math.max(0.6, 1 - ad * 0.16);
        var op = ad > 2 ? 0 : 1 - ad * 0.3;
        slide.style.transform = 'translate(-50%,-50%) translate3d(' + tx + 'px,0,' + tz + 'px) rotateY(' + ry + 'deg) scale(' + sc + ')';
        slide.style.opacity = String(op);
        slide.style.zIndex = String(100 - ad);
        slide.style.pointerEvents = ad > 2 ? 'none' : 'auto';
        slide.classList.toggle('is-active', d === 0);
        slide.setAttribute('aria-hidden', d === 0 ? 'false' : 'true');
        slide.tabIndex = d === 0 ? 0 : -1;
      });
      dotEls.forEach(function (dot, i) { dot.classList.toggle('is-active', i === current); });
    }

    function goTo(i) { current = ((i % n) + n) % n; layout(); }
    function next() { goTo(current + 1); }
    function prev() { goTo(current - 1); }

    nextBtn.addEventListener('click', function () { next(); kick(); });
    prevBtn.addEventListener('click', function () { prev(); kick(); });

    slides.forEach(function (slide, i) {
      slide.addEventListener('click', function (e) {
        if (i !== current) { e.preventDefault(); goTo(i); kick(); }
      });
    });

    wrap.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { next(); kick(); }
      else if (e.key === 'ArrowLeft') { prev(); kick(); }
    });

    // Drag / swipe support (mouse + touch via Pointer Events)
    var dragStartX = null, dragging = false, dragMoved = false;
    wrap.addEventListener('pointerdown', function (e) {
      dragging = true; dragMoved = false; dragStartX = e.clientX;
    });
    wrap.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      if (Math.abs(e.clientX - dragStartX) > 6) dragMoved = true;
    });
    window.addEventListener('pointerup', function (e) {
      if (!dragging) return;
      dragging = false;
      if (!dragMoved) return;
      var dx = e.clientX - dragStartX;
      if (Math.abs(dx) > 40) { dx < 0 ? next() : prev(); kick(); }
    });

    // Autoplay — paused on hover/focus/hidden tab, off for reduced motion
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var timer = null;
    function start() { if (reduced) return; stop(); timer = setInterval(next, 3800); }
    function stop() { if (timer) clearInterval(timer); timer = null; }
    function kick() { start(); }
    wrap.addEventListener('mouseenter', stop);
    wrap.addEventListener('mouseleave', start);
    wrap.addEventListener('focusin', stop);
    wrap.addEventListener('focusout', start);
    document.addEventListener('visibilitychange', function () {
      document.hidden ? stop() : start();
    });

    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(layout, 120);
    });

    layout();
    start();
  }

  if (!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    $$('[data-carousel] .cat-cards').forEach(initCategoryCarousel);
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

  /* ---------------------------------------------------------
     DESIGN LAYER v3 — "Emerald Luxe" motion enhancements
     Cursor spotlight on heroes, 3D tilt on cards, magnetic
     buttons. Purely progressive: no-ops where unsupported and
     disabled entirely under prefers-reduced-motion.
     --------------------------------------------------------- */
  (function luxeEnhance() {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return;

    /* --- hero cursor spotlight (desktop pointers only) --- */
    var fine = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
    if (fine) {
      $$('.page-hero').forEach(function (hero) {
        var glow = document.createElement('span');
        glow.setAttribute('aria-hidden', 'true');
        glow.style.cssText =
          'position:absolute;inset:0;pointer-events:none;z-index:-1;opacity:0;' +
          'transition:opacity .35s ease;' +
          'background:radial-gradient(340px 340px at var(--mx,50%) var(--my,50%), rgba(232,198,106,.22), transparent 65%);';
        hero.style.position = hero.style.position || 'relative';
        hero.appendChild(glow);
        hero.addEventListener('pointermove', function (e) {
          var r = hero.getBoundingClientRect();
          glow.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
          glow.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
          glow.style.opacity = '1';
        });
        hero.addEventListener('pointerleave', function () { glow.style.opacity = '0'; });
      });
    }

    /* --- 3D tilt on cards --- */
    if (fine) {
      var TILT = '.feature-card, .cat-card, .service-card';
      $$(TILT).forEach(function (card) {
        // Never tilt cards inside the coverflow carousel — the inline
        // transform would override the carousel's JS positioning and make
        // the cards scatter out of place on hover.
        if (card.closest('.cat-cards--carousel')) return;
        card.style.transformStyle = 'preserve-3d';
        card.addEventListener('pointermove', function (e) {
          var r = card.getBoundingClientRect();
          var px = (e.clientX - r.left) / r.width - 0.5;
          var py = (e.clientY - r.top) / r.height - 0.5;
          card.style.transform =
            'perspective(900px) rotateX(' + (-py * 4).toFixed(2) + 'deg) rotateY(' + (px * 5).toFixed(2) + 'deg) translateY(-6px)';
        });
        card.addEventListener('pointerleave', function () { card.style.transform = ''; });
      });
    }

    /* --- magnetic primary buttons --- */
    if (fine) {
      $$('.btn--primary').forEach(function (btn) {
        btn.addEventListener('pointermove', function (e) {
          var r = btn.getBoundingClientRect();
          var x = (e.clientX - (r.left + r.width / 2)) * 0.18;
          var y = (e.clientY - (r.top + r.height / 2)) * 0.28;
          btn.style.transform = 'translate(' + x.toFixed(1) + 'px,' + (y - 2).toFixed(1) + 'px)';
        });
        btn.addEventListener('pointerleave', function () { btn.style.transform = ''; });
      });
    }
  })();

})();
