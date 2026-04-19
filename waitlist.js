/* HIP3Radar — Shared Waitlist Modal
 * Include on any page:  <script src="/waitlist.js" defer></script>
 * Trigger from any CTA: onclick="openWaitlistModal('pro')"  (plan: general|pro|team|verified deployer|enterprise)
 *                   or: <a href="#" data-waitlist="pro">Join the waitlist →</a>
 * Self-injects modal DOM + CSS. Posts to Supabase (hip3radar_waitlist table) then best-effort
 * confirmation email via /api/waitlist/send. Uses page's CSS vars if present, with green fallbacks.
 */
(function(){
  if (window.__hip3radarWaitlistLoaded) return;
  window.__hip3radarWaitlistLoaded = true;

  var SUPABASE_URL   = 'https://rrowmfxcfeegtazmkvtf.supabase.co';
  var SUPABASE_KEY   = 'sb_publishable_adcjSKP2wtoVXDt0l5mhnw_AoFpBgoa';
  var SUPABASE_TABLE = 'hip3radar_waitlist';
  var SEND_URL       = '/api/waitlist/send';

  var PLAN_LABELS = {
    general: '',
    pro: 'Pro ($49/mo)',
    team: 'Team ($499/mo)',
    'verified deployer': 'Verified Deployer ($2,500+/mo)',
    enterprise: 'Verified Deployer ($2,500+/mo)',
  };
  var currentPlan = 'general';

  var CSS = [
    '.wl-overlay{position:fixed;inset:0;z-index:9999;background:rgba(5,8,7,0.85);backdrop-filter:blur(8px);display:none;align-items:center;justify-content:center;opacity:0;transition:opacity .22s;font-family:var(--sans,-apple-system,"Geist",system-ui,sans-serif)}',
    '.wl-overlay.show{display:flex;opacity:1}',
    '.wl-modal{width:min(460px,calc(100% - 28px));background:linear-gradient(180deg,var(--surface,#0f1311) 0%,var(--bg,#0a0c0b) 100%);border:1px solid var(--accent,#7ef3a0);box-shadow:0 24px 64px -20px rgba(126,243,160,.4),0 8px 24px rgba(0,0,0,.6);padding:32px 30px 26px;position:relative;border-radius:0;transform:translateY(12px) scale(.97);transition:transform .22s}',
    '.wl-overlay.show .wl-modal{transform:translateY(0) scale(1)}',
    '@media(max-width:520px){.wl-modal{width:calc(100vw - 24px);max-width:480px;padding:24px 20px}}',
    '.wl-close{position:absolute;top:14px;right:14px;width:32px;height:32px;display:flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--line-2,#23302a);color:var(--ink-2,#9ba49f);font-size:18px;line-height:1;cursor:pointer;transition:all .15s;font-family:var(--mono,"Geist Mono",ui-monospace,monospace)}',
    '.wl-close:hover{background:var(--surface-2,#141a17);color:var(--ink,#e8ece4);border-color:var(--ink-3,#5a6a61)}',
    '.wl-badge{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono,"Geist Mono",ui-monospace,monospace);font-size:10.5px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--accent,#7ef3a0);background:rgba(126,243,160,.1);border:1px solid rgba(126,243,160,.3);padding:5px 11px;margin-bottom:16px}',
    '.wl-badge .dot{width:6px;height:6px;border-radius:50%;background:var(--accent,#7ef3a0);box-shadow:0 0 8px var(--accent,#7ef3a0)}',
    '.wl-title{font-family:var(--sans,-apple-system,"Geist",system-ui,sans-serif);font-size:26px;font-weight:500;line-height:1.05;letter-spacing:-.025em;color:var(--ink,#e8ece4);margin:0 0 10px}',
    '.wl-title em{font-family:var(--serif,"Instrument Serif",serif);font-style:italic;color:var(--ink-2,#9ba49f)}',
    '.wl-sub{font-size:13.5px;color:var(--ink-2,#9ba49f);line-height:1.55;margin:0 0 22px}',
    '.wl-sub .plan-chip{display:inline-block;padding:2px 8px;margin-left:4px;font-family:var(--mono,"Geist Mono",ui-monospace,monospace);font-size:11px;font-weight:500;background:rgba(126,243,160,.14);color:var(--accent,#7ef3a0);border:1px solid rgba(126,243,160,.3)}',
    '.wl-input{width:100%;padding:13px 16px;background:var(--bg,#0a0c0b);border:1px solid var(--line-2,#23302a);color:var(--ink,#e8ece4);font-family:var(--mono,"Geist Mono",ui-monospace,monospace);font-size:13px;outline:none;transition:border-color .15s;border-radius:0;box-sizing:border-box}',
    '.wl-input::placeholder{color:var(--ink-3,#5a6a61)}',
    '.wl-input:focus{border-color:var(--accent,#7ef3a0)}',
    '.wl-submit{width:100%;margin-top:12px;padding:13px 18px;background:var(--accent,#7ef3a0);color:var(--accent-ink,#0b1510);border:1px solid var(--accent,#7ef3a0);font-family:var(--mono,"Geist Mono",ui-monospace,monospace);font-weight:600;font-size:13px;letter-spacing:.04em;cursor:pointer;transition:filter .15s;border-radius:0}',
    '.wl-submit:hover{filter:brightness(1.06)}',
    '.wl-submit:active{transform:translateY(1px)}',
    '.wl-submit:disabled{opacity:.55;cursor:not-allowed;filter:grayscale(.2)}',
    '.wl-note{font-size:11px;color:var(--ink-3,#5a6a61);text-align:center;margin-top:14px;line-height:1.55;font-family:var(--mono,"Geist Mono",ui-monospace,monospace)}',
    '.wl-error{color:var(--danger,#ff6b6b);font-size:12px;margin-top:8px;min-height:14px;font-family:var(--mono,"Geist Mono",ui-monospace,monospace)}',
    '.wl-success{display:none;text-align:center;padding:14px 0 6px}',
    '.wl-success.show{display:block}',
    '.wl-check{width:56px;height:56px;border-radius:50%;margin:0 auto 14px;background:rgba(126,243,160,.16);border:1.5px solid rgba(126,243,160,.5);display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--accent,#7ef3a0);animation:wl-pop .4s cubic-bezier(.2,1.4,.4,1)}',
    '@keyframes wl-pop{0%{transform:scale(0);opacity:0}100%{transform:scale(1);opacity:1}}',
    '.wl-success-title{font-family:var(--sans,-apple-system,"Geist",system-ui,sans-serif);font-size:22px;font-weight:500;color:var(--ink,#e8ece4);margin:0 0 8px;letter-spacing:-.015em}',
    '.wl-success-title em{font-family:var(--serif,"Instrument Serif",serif);font-style:italic;color:var(--ink-2,#9ba49f)}',
    '.wl-success-sub{font-size:13px;color:var(--ink-2,#9ba49f);line-height:1.55;margin:0;font-family:var(--sans,-apple-system,"Geist",system-ui,sans-serif)}'
  ].join('');

  var HTML = '' +
    '<div id="wl-overlay" class="wl-overlay" role="dialog" aria-modal="true" aria-labelledby="wl-title">' +
      '<div class="wl-modal">' +
        '<button class="wl-close" aria-label="Close">×</button>' +
        '<div id="wl-form-view">' +
          '<div class="wl-badge"><span class="dot"></span> JOIN THE WAITLIST</div>' +
          '<h3 id="wl-title" class="wl-title">First in line. <em>When access opens.</em></h3>' +
          '<p class="wl-sub">Get notified the moment paid tiers go live<span id="wl-plan-chip"></span></p>' +
          '<input type="email" id="wl-email" class="wl-input" placeholder="you@example.com" autocomplete="email" />' +
          '<button id="wl-submit-btn" class="wl-submit">JOIN WAITLIST →</button>' +
          '<div id="wl-error" class="wl-error"></div>' +
          '<p class="wl-note">No spam. We only email about HIP3Radar access and major incidents.</p>' +
        '</div>' +
        '<div id="wl-success-view" class="wl-success">' +
          '<div class="wl-check">✓</div>' +
          '<h4 class="wl-success-title">You\u0027re <em>on the list.</em></h4>' +
          '<p class="wl-success-sub">Check your inbox — confirmation is on its way. We\u0027ll reach out the moment your tier opens.</p>' +
        '</div>' +
      '</div>' +
    '</div>';

  function inject(){
    if (document.getElementById('wl-overlay')) return;
    var style = document.createElement('style'); style.textContent = CSS; document.head.appendChild(style);
    var host = document.createElement('div'); host.innerHTML = HTML; document.body.appendChild(host.firstChild);

    var overlay = document.getElementById('wl-overlay');
    overlay.querySelector('.wl-close').addEventListener('click', closeWaitlistModal);
    overlay.addEventListener('click', function(e){ if (e.target.id === 'wl-overlay') closeWaitlistModal(); });
    document.getElementById('wl-submit-btn').addEventListener('click', submitWaitlist);
    document.getElementById('wl-email').addEventListener('keydown', function(e){ if (e.key === 'Enter') submitWaitlist(); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') closeWaitlistModal(); });

    // Wire any [data-waitlist] triggers already in the DOM
    document.querySelectorAll('[data-waitlist]').forEach(function(el){
      el.addEventListener('click', function(e){ e.preventDefault(); openWaitlistModal(el.getAttribute('data-waitlist') || 'general'); });
    });
  }

  function openWaitlistModal(plan){
    currentPlan = (plan || 'general').toLowerCase();
    var chip = document.getElementById('wl-plan-chip');
    if (chip) {
      var label = PLAN_LABELS[currentPlan] || '';
      chip.innerHTML = label ? ' · <span class="plan-chip">' + label + '</span>' : '';
    }
    document.getElementById('wl-form-view').style.display = '';
    document.getElementById('wl-success-view').classList.remove('show');
    document.getElementById('wl-error').textContent = '';
    var btn = document.getElementById('wl-submit-btn'); btn.disabled = false; btn.innerHTML = 'JOIN WAITLIST &rarr;';
    var email = document.getElementById('wl-email'); email.value = '';
    document.getElementById('wl-overlay').classList.add('show');
    setTimeout(function(){ email.focus(); }, 140);
    if (window.umami && typeof umami.track === 'function') umami.track('waitlist-open', { plan: currentPlan });
  }

  function closeWaitlistModal(){
    var o = document.getElementById('wl-overlay'); if (o) o.classList.remove('show');
  }

  async function submitWaitlist(){
    var emailInput = document.getElementById('wl-email');
    var errEl = document.getElementById('wl-error');
    var btn = document.getElementById('wl-submit-btn');
    var email = (emailInput.value || '').trim().toLowerCase();
    errEl.textContent = '';
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { errEl.textContent = 'Please enter a valid email address.'; return; }
    btn.disabled = true; btn.textContent = 'Joining…';

    var planLabel = PLAN_LABELS[currentPlan] || 'HIP3Radar Waitlist';
    var callSign = 'HIP3Radar:' + currentPlan;

    var supabaseOk = false;
    try {
      var resp = await fetch(SUPABASE_URL + '/rest/v1/' + SUPABASE_TABLE, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': 'Bearer ' + SUPABASE_KEY,
          'Content-Type': 'application/json',
          'Prefer': 'return=minimal'
        },
        body: JSON.stringify({
          email: email,
          plan: currentPlan,
          call_sign: callSign,
          source: location.hostname || 'hip3radar.xyz',
          created_at: new Date().toISOString()
        })
      });
      supabaseOk = resp.ok;
      if (!resp.ok) {
        var txt = await resp.text();
        if (resp.status === 409 || /duplicate/i.test(txt)) supabaseOk = true;
        else console.warn('Supabase insert failed:', resp.status, txt);
      }
    } catch (e) { console.warn('Supabase insert error:', e); }

    if (!supabaseOk) {
      errEl.textContent = 'Something went wrong. Please try again.';
      btn.disabled = false; btn.innerHTML = 'JOIN WAITLIST &rarr;';
      return;
    }

    try {
      await fetch(SEND_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, plan: currentPlan, plan_label: planLabel || 'HIP3Radar Waitlist' })
      });
    } catch (e) { console.warn('Email send error:', e); }

    document.getElementById('wl-form-view').style.display = 'none';
    document.getElementById('wl-success-view').classList.add('show');
    if (window.umami && typeof umami.track === 'function') umami.track('waitlist-submit', { plan: currentPlan });
    setTimeout(closeWaitlistModal, 4500);
  }

  window.openWaitlistModal = openWaitlistModal;
  window.closeWaitlistModal = closeWaitlistModal;
  window.submitWaitlist = submitWaitlist;

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject);
  else inject();
})();
