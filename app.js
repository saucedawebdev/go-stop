/**
 * GoStop — Visual Cue Card PWA
 * Handles card flipping, accessibility, haptics, and service worker registration.
 */

(function () {
  'use strict';

  /** @type {HTMLElement | null} */
  const app = document.getElementById('app');

  /** @type {HTMLElement | null} */
  const card = document.getElementById('card');

  /** @type {HTMLElement | null} */
  const srAnnounce = document.getElementById('sr-announce');

  /** Whether the card currently shows STOP (true) or GO (false) */
  let isStop = false;

  /** Whether a flip animation is in progress */
  let isAnimating = false;

  /** Animation duration in ms — must match CSS */
  const FLIP_DURATION = 450;

  /** Reduced motion fade duration in ms */
  const FADE_DURATION = 300;

  /**
   * Returns the current animation duration based on motion preference.
   * @returns {number}
   */
  function getAnimationDuration() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches
      ? FADE_DURATION
      : FLIP_DURATION;
  }

  /**
   * Trigger a gentle haptic pulse when supported.
   */
  function triggerHaptic() {
    if ('vibrate' in navigator) {
      navigator.vibrate(10);
    }
  }

  /**
   * Update ARIA attributes and screen reader announcement for current state.
   */
  function updateAccessibility() {
    if (!app || !srAnnounce) return;

    const state = isStop ? 'STOP' : 'GO';
    const next = isStop ? 'GO' : 'STOP';

    app.setAttribute(
      'aria-label',
      `Cue card showing ${state}. Tap, press Space, or press Enter to flip to ${next}.`
    );
    app.setAttribute('aria-pressed', String(isStop));

    /* Update theme-color meta for status bar tint */
    const themeMeta = document.querySelector('meta[name="theme-color"]');
    if (themeMeta) {
      themeMeta.setAttribute('content', isStop ? '#FF3B30' : '#34C759');
    }

    /* Announce state change to screen readers */
    srAnnounce.textContent = state;
  }

  /**
   * Apply visual state to DOM without animation (initial load).
   */
  function applyState() {
    if (!app || !card) return;

    app.classList.toggle('app--stop', isStop);
    card.classList.toggle('card--flipped', isStop);
    updateAccessibility();
  }

  /**
   * Flip the card between GO and STOP.
   */
  function flip() {
    if (isAnimating || !app || !card) return;

    isAnimating = true;
    app.classList.add('app--animating');

    isStop = !isStop;
    app.classList.toggle('app--stop', isStop);
    card.classList.toggle('card--flipped', isStop);

    triggerHaptic();
    updateAccessibility();

    window.setTimeout(function () {
      isAnimating = false;
      app.classList.remove('app--animating');
    }, getAnimationDuration());
  }

  /**
   * Handle keyboard interaction (Space and Enter).
   * @param {KeyboardEvent} event
   */
  function handleKeydown(event) {
    if (event.key === ' ' || event.key === 'Enter') {
      event.preventDefault();
      flip();
    }
  }

  /**
   * Register the service worker for offline support.
   */
  function registerServiceWorker() {
    if (!('serviceWorker' in navigator)) return;

    window.addEventListener('load', function () {
      navigator.serviceWorker
        .register('./service-worker.js')
        .catch(function () {
          /* Fail silently — app works without offline support */
        });
    });
  }

  /**
   * Initialize the application.
   */
  function init() {
    if (!app || !card) return;

    applyState();

    app.addEventListener('click', flip);
    app.addEventListener('keydown', handleKeydown);

    /* Re-evaluate motion preference if user changes system setting */
    window
      .matchMedia('(prefers-reduced-motion: reduce)')
      .addEventListener('change', function () {
        /* No DOM changes needed — CSS handles the switch */
      });

    registerServiceWorker();
  }

  init();
})();
