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
  var SEASON = {
    en: { open: 'Kymyz season is open', openText: 'Fresh Ak Bee kymyz is bottled every morning and in the shops by the afternoon, until the end of September.',
          closed: 'Kymyz season is closed', closedText: 'The mares are back from the summer pastures. The first Ak Bee kymyz of {y} will be bottled after the kymyz muryndyk in May. Until then, try our airan and qatiq.' },
    ru: { open: 'Сезон кымыза открыт', openText: 'Свежий кымыз Ak Bee разливают каждое утро, а после обеда он уже в магазинах — до конца сентября.',
          closed: 'Сезон кымыза закрыт', closedText: 'Кобылицы вернулись с летних пастбищ. Первый кымыз Ak Bee {y} года разольют после кымыз мурундука в мае. А пока попробуйте наш айран и катык.' },
    ky: { open: 'Kımız mezgili achık', openText: 'Jañı Ak Bee kımızı ar tañ kuyulup, tüshtön kiyin düköndördö bolot — sentyabrdın ayagına cheyin.',
          closed: 'Kımız mezgili jabık', closedText: 'Biyeler jayloodon kaytıp keldi. {y}-jıldın birinchi Ak Bee kımızı maydagı kımız murunduktan kiyin kuyulat. Aga cheyin airan menen qatiqtı tatıp köröñüz.' }
  };
  var season = document.querySelector('[data-season]');
  if (season) {
    var words = SEASON[document.documentElement.lang] || SEASON.en;
    var now = new Date();
    var m = now.getMonth();
    var title = season.querySelector('h3');
    var text = season.querySelector('p');
    if (m >= 4 && m <= 8) {
      title.textContent = words.open;
      text.textContent = words.openText;
    } else {
      var year = m > 8 ? now.getFullYear() + 1 : now.getFullYear();
      season.classList.add('closed');
      title.textContent = words.closed;
      text.textContent = words.closedText.replace('{y}', year);
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
