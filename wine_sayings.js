var randomStrings = [
'"Nothing more excellent or valuable than wine was every granted by the gods to man." - Plato',
'"God many only water, but man made wine." - Victor Hugo',
'"Wine - it should be enjoyed for the benefits of the soul - and nothing more." - Peter Fiduccia, Wine Lover',
'"Wine can be considered with good reason as the most healthful and hygenic of all beverages." - Louis Pasteur',
'"The wine in the bottle does not quench thirst." - George Herbert',
'"Sip, Swirl, Swallow!" - Micheline R. Ramos, wine lover',
'"A person with increasing knowledge and sensory education may derive infinite enjoyment from wine."  - Ernest Hemingway',
'"There must be always wine and fellowship or we are truly lost." - Ann Fairbairn',
'"Wine, it is in my veins and I cannnot get it out." - Burgess Meredith',
'"To take wine into our mouths is to savor a droplet of the river of human history." - New York Times, 1967',
'"Three be the things I shall never attain: envy, content and sufficient champagne." - Dorothy Parker',
'"Wine rejoices the heart of man and joy is the mother of all virtues." - Johann Wolfgang von Goethe',
'"A bottle of wine begs to be shared; I have never met a miserly wine lover." - Clifton Fadiman',
'"Let us have wine and women, mirth and laughter, Sermons and soda-water the day after." - Lord Byron',
'"You have only so many bottles in your life, never drink a bad one." - Len Evans, wine lover',
'"Wine makes daily living easier, less hurried, with fewer tensions and more tolerance." - Benjamin Franklin'
  ];
   document.addEventListener('DOMContentLoaded', function() {
    randomIndex = Math.ceil((Math.random() * randomStrings.length - 1));
    newText = randomStrings[randomIndex];
    document.querySelector('#WineSaying').innerHTML = newText;
  });