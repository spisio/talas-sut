// Talas Süt: menu toggle, kymyz season notice, product filters.
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Ak Bee kymyz is bottled from the first of May to the end of September.
  var season = document.querySelector('[data-season]');
  if (season) {
    var now = new Date();
    var m = now.getMonth();
    var title = season.querySelector('h3');
    var text = season.querySelector('p');
    if (m >= 4 && m <= 8) {
      title.textContent = 'Kymyz season is open';
      text.textContent = 'Fresh Ak Bee kymyz is bottled every morning and in the shops by the afternoon, until the end of September.';
    } else {
      var year = m > 8 ? now.getFullYear() + 1 : now.getFullYear();
      season.classList.add('closed');
      title.textContent = 'Kymyz season is closed';
      text.textContent = 'The mares are back from the summer pastures. The first Ak Bee kymyz of ' + year + ' will be bottled after the kymyz muryndyk in May. Until then, try our airan and qatiq.';
    }
  }

  // Catalogue filters
  var chips = document.querySelectorAll('.chip[data-filter]');
  var blocks = document.querySelectorAll('.cat-block');
  function show(filter) {
    chips.forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.filter === filter ? 'true' : 'false'); });
    blocks.forEach(function (b) { b.hidden = filter !== 'all' && b.id !== filter; });
  }
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      show(c.dataset.filter);
      history.replaceState(null, '', c.dataset.filter === 'all' ? location.pathname : '#' + c.dataset.filter);
    });
  });
  if (chips.length && location.hash) {
    var id = location.hash.slice(1);
    if (document.getElementById(id) && document.getElementById(id).classList.contains('cat-block')) show(id);
  }
})();
