/* HIP3Radar — JS-driven animated favicon (Chrome dropped GIF favicon animation in 2017).
 * Pre-renders 32 frames of a green sweeping radar to canvas, swaps <link rel="icon"> every 80ms.
 * Include on every page: <script src="/favicon.js" defer></script>
 */
(function(){
  if (typeof document === 'undefined' || !document.createElement) return;
  var SIZE = 32, FRAMES = 32, INTERVAL = 80;
  var canvas = document.createElement('canvas'); canvas.width = SIZE; canvas.height = SIZE;
  var ctx = canvas.getContext('2d'); if (!ctx) return;

  var link = document.querySelector('link[rel="icon"]');
  if (!link) { link = document.createElement('link'); link.rel = 'icon'; document.head.appendChild(link); }

  var frameUrls = [];
  function renderFrame(angleDeg) {
    ctx.clearRect(0, 0, SIZE, SIZE);
    ctx.fillStyle = '#0a0c0b';
    ctx.fillRect(0, 0, SIZE, SIZE);
    var cx = SIZE / 2, cy = SIZE / 2;
    var rOuter = SIZE * 0.42, rInner = SIZE * 0.16;
    ctx.beginPath(); ctx.arc(cx, cy, rOuter, 0, Math.PI * 2); ctx.fillStyle = '#7ef3a0'; ctx.fill();
    var rad = angleDeg * Math.PI / 180;
    var sweep = 60 * Math.PI / 180;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, rOuter, rad, rad + sweep);
    ctx.closePath();
    ctx.fillStyle = 'rgba(255,255,255,0.42)';
    ctx.fill();
    ctx.beginPath(); ctx.arc(cx, cy, rInner, 0, Math.PI * 2); ctx.fillStyle = '#0b1510'; ctx.fill();
    return canvas.toDataURL('image/png');
  }
  for (var i = 0; i < FRAMES; i++) frameUrls.push(renderFrame((i / FRAMES) * 360 - 90));

  var idx = 0;
  setInterval(function(){
    link.href = frameUrls[idx];
    idx = (idx + 1) % FRAMES;
  }, INTERVAL);
})();
