const urlParams = new URLSearchParams(window.location.search);
const model = urlParams.get('model');
const make = urlParams.get('make');
const year = (urlParams.get('year'));
const vin = (urlParams.get('vin'));


var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        setChart(this);
   }
};

xhttp.open("GET", '/api/api_chart/?make=' + make + '&model=' + model + '&year=' + year, true);
xhttp.send();

window.points = []
// window.points = [
//     {
//         x: 62500,
//         y: 37900,
//         r: 4,
//         id: 1001065837,
//         picture: 'https://galeria.autotrader.pl/mid/f/87/fc/75f1e5b67a78876c6c51e1fc8ab6fdb7f0d36334.jpg',
//         url: '/oferta/volkswagen-golf-krakow-1001065837',
//         year: 2010
//     },
//     {
//         x: 231052,
//         y: 14900,
//         r: 4,
//         id: 1001056624,
//         picture: 'https://galeria.autotrader.pl/mid/d/d5/f7/36d66912b1dad5a0ae0a60f7929cb3aefe1fdfc0.jpg',
//         url: '/oferta/volkswagen-golf-krakow-1001056624',
//         year: 2005
//     },
//     {
//         x: 64560,
//         y: 25500,
//         r: 4,
//         id: 1001069040,
//         picture: 'https://galeria.autotrader.pl/mid/d/e4/5d/ebd9c4ec6ec1e4312a37eb5d1165a4e5306766d7.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001069040',
//         year: 2007
//     },
//     {
//         x: 119856,
//         y: 28300,
//         r: 4,
//         id: 1001068468,
//         picture: 'https://galeria.autotrader.pl/mid/9/38/a4/82901a8d8092383edb5b8da43b7cc0acf7cfb380.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001068468',
//         year: 2009
//     },
//     {
//         x: 222777,
//         y: 11500,
//         r: 4,
//         id: 1001068457,
//         picture: 'https://galeria.autotrader.pl/mid/b/8f/58/ccbe0642900e8f171e11f758b166b25116c88b3b.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001068457',
//         year: 2005
//     },
//     {
//         x: 255415,
//         y: 7499,
//         r: 4,
//         id: 1001068395,
//         picture: 'https://galeria.autotrader.pl/mid/8/40/da/6f8959bdfb2840409fe27cdad8313fec5033d728.jpg',
//         url: '/oferta/volkswagen-golf-jelenia-gora-1001068395',
//         year: 2001
//     },
//     {
//         x: 260000,
//         y: 22500,
//         r: 4,
//         id: 1001068375,
//         picture: 'https://galeria.autotrader.pl/mid/8/f6/ca/7d8ba4a6141bf692542da1ca8e581d5ececc2e81.jpg',
//         url: '/oferta/volkswagen-golf-pyzdry-1001068375',
//         year: 2011
//     },
//     {
//         x: 182000,
//         y: 3499,
//         r: 4,
//         id: 1001068355,
//         picture: 'https://galeria.autotrader.pl/mid/f/56/f4/eefd4c664e8056c1898c58f419bf6dd6917f7b8b.jpg',
//         url: '/oferta/volkswagen-golf-dobieszowice-1001068355',
//         year: 1998
//     },
//     {
//         x: 310000,
//         y: 4600,
//         r: 4,
//         id: 1001068347,
//         picture: 'https://galeria.autotrader.pl/mid/0/19/f8/a700e8459a4d19a9a6b40ef8d7cf60fe06ce7cd5.jpg',
//         url: '/oferta/volkswagen-golf-1001068347',
//         year: 2003
//     },
//     {
//         x: 70192,
//         y: 44700,
//         r: 4,
//         id: 1001068027,
//         picture: 'https://galeria.autotrader.pl/mid/e/f9/9e/1fed24a831e0f9a05272829ea1a90613b0454eea.jpg',
//         url: '/oferta/volkswagen-golf-komorniki-1001068027',
//         year: 2015
//     },
//     {
//         x: 127561,
//         y: 21900,
//         r: 4,
//         id: 1001067993,
//         picture: 'https://galeria.autotrader.pl/mid/2/79/25/b72b09dcb561794c87f9ff2562fd632071688f4f.jpg',
//         url: '/oferta/volkswagen-golf-czestochowa-1001067993',
//         year: 2007
//     },
//     {
//         x: 168069,
//         y: 45600,
//         r: 4,
//         id: 1001067957,
//         picture: 'https://galeria.autotrader.pl/mid/1/f5/63/971f757ecba7f58f60588963bf0e91fa80dbecb8.jpg',
//         url: '/oferta/volkswagen-golf-ozarow-mazowiecka-1001067957',
//         year: 2015
//     },
//     {
//         x: 0,
//         y: 49700,
//         r: 4,
//         id: 1001067856,
//         picture: 'https://galeria.autotrader.pl/mid/9/a5/fb/849d9d82f210a586d523b6fb50f7471909839c14.jpg',
//         url: '/oferta/volkswagen-golf-grzedy-1001067856',
//         year: 2017
//     },
//     {
//         x: 154689,
//         y: 39000,
//         r: 4,
//         id: 1001067836,
//         picture: 'https://galeria.autotrader.pl/mid/4/4f/f9/a7478aad59304ff2105623f99e8b24adc81ab77c.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001067836',
//         year: 2014
//     },
//     {
//         x: 139000,
//         y: 39900,
//         r: 4,
//         id: 1001067402,
//         picture: 'https://galeria.autotrader.pl/mid/b/19/bf/adbfe962d2f519611c94bdbf998007e491a9e961.jpg',
//         url: '/oferta/volkswagen-golf-warszawa-1001067402',
//         year: 2014
//     },
//     {
//         x: 155956,
//         y: 51900,
//         r: 4,
//         id: 1001067398,
//         picture: 'https://galeria.autotrader.pl/mid/1/8f/e9/271b26b0aa5f8f1d9e84b0e95e4f9649713678ab.jpg',
//         url: '/oferta/volkswagen-golf-warszawa-1001067398',
//         year: 2015
//     },
//     {
//         x: 189000,
//         y: 19900,
//         r: 4,
//         id: 1001067214,
//         picture: 'https://galeria.autotrader.pl/mid/4/2f/7b/8d4b36a765182f1bad30da7b7a93ebf52b439d66.jpg',
//         url: '/oferta/volkswagen-golf-wegrow-1001067214',
//         year: 2008
//     },
//     {
//         x: 43025,
//         y: 46500,
//         r: 4,
//         id: 1001066877,
//         picture: 'https://galeria.autotrader.pl/mid/b/ee/79/c3b2d08b2ea7ee013d39de79d80281a477ded4ec.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001066877',
//         year: 2015
//     },
//     {
//         x: 151459,
//         y: 41000,
//         r: 4,
//         id: 1001066876,
//         picture: 'https://galeria.autotrader.pl/mid/2/37/70/a227eb47f22037f23e23387031b6a903ec6dc63d.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001066876',
//         year: 2014
//     },
//     {
//         x: 151796,
//         y: 39000,
//         r: 4,
//         id: 1001066875,
//         picture: 'https://galeria.autotrader.pl/mid/5/49/a3/0d5f1d634b114977c3e982a332b47322561ff2b1.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001066875',
//         year: 2015
//     },
//     {
//         x: 13869,
//         y: 58000,
//         r: 4,
//         id: 1001066871,
//         picture: 'https://galeria.autotrader.pl/mid/8/1d/85/9684d03e5b341dcf564776853b8887e80c4effab.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001066871',
//         year: 2017
//     },
//     {
//         x: 136369,
//         y: 39000,
//         r: 4,
//         id: 1001066870,
//         picture: 'https://galeria.autotrader.pl/mid/c/8d/40/5ac8ff394e1a8d31cdfe6d40cbb2dfdab0aac9ec.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001066870',
//         year: 2015
//     },
//     {
//         x: 135775,
//         y: 38000,
//         r: 4,
//         id: 1001066867,
//         picture: 'https://galeria.autotrader.pl/mid/c/68/21/08c77dbb43f768077e63892172adc00ce75e4ddc.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001066867',
//         year: 2015
//     },
//     {
//         x: 313000,
//         y: 13200,
//         r: 4,
//         id: 1001066856,
//         picture: 'https://galeria.autotrader.pl/mid/a/42/5e/2eaf7e70611a4277b74ef45efbab5e1c000fca87.jpg',
//         url: '/oferta/volkswagen-golf-1001066856',
//         year: 2002
//     },
//     {
//         x: 243000,
//         y: 5700,
//         r: 4,
//         id: 1001066544,
//         picture: 'https://galeria.autotrader.pl/mid/d/d5/db/15d8de33d88cd52f040d81dbc91278de79a18112.jpg',
//         url: '/oferta/volkswagen-golf-goczalkowice-zdroj-1001066544',
//         year: 2001
//     },
//     {
//         x: 170000,
//         y: 7900,
//         r: 4,
//         id: 1001066065,
//         picture: 'https://galeria.autotrader.pl/mid/e/69/39/b0e93d45303a699a6cc898398ce5e74e798d2791.jpg',
//         url: '/oferta/volkswagen-golf-zieleniowo-1001066065',
//         year: 1998
//     },
//     {
//         x: 113000,
//         y: 45900,
//         r: 4,
//         id: 1001065036,
//         picture: 'https://galeria.autotrader.pl/mid/e/50/ac/34e4f18a8ae550d5252e0eac047c14954434e91d.jpg',
//         url: '/oferta/volkswagen-golf-sokolow-1001065036',
//         year: 2015
//     },
//     {
//         x: 280000,
//         y: 19900,
//         r: 4,
//         id: 1001064968,
//         picture: 'https://galeria.autotrader.pl/mid/a/7a/f3/63a37dc143167ab5cdae2cf3f71b5137aa75dce3.jpg',
//         url: '/oferta/volkswagen-golf-kutno-1001064968',
//         year: 2007
//     },
//     {
//         x: 110372,
//         y: 45900,
//         r: 4,
//         id: 1001063538,
//         picture: 'https://galeria.autotrader.pl/mid/5/64/76/df5a7865f08e64a1dadd2e7653685629133e930b.jpg',
//         url: '/oferta/volkswagen-golf-bielsko-biala-1001063538',
//         year: 2015
//     },
//     {
//         x: 149000,
//         y: 31900,
//         r: 4,
//         id: 1001063466,
//         picture: 'https://galeria.autotrader.pl/mid/7/c0/8c/e3762b2158c8c0d3aac96c8c210cd27a7c6fb818.jpg',
//         url: '/oferta/volkswagen-golf-stalowa-wola-1001063466',
//         year: 2015
//     },
//     {
//         x: 142000,
//         y: 24400,
//         r: 4,
//         id: 1001029554,
//         picture: 'https://galeria.autotrader.pl/mid/4/0d/91/19484fb01df80d6a69c780916041740d61497f1a.jpg',
//         url: '/oferta/volkswagen-golf-sanok-1001029554',
//         year: 2010
//     },
//     {
//         x: 143000,
//         y: 16000,
//         r: 4,
//         id: 1001063272,
//         picture: 'https://galeria.autotrader.pl/mid/b/66/00/94b36f6cb33066535a41c200cf274dee1ce5bd49.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001063272',
//         year: 2006
//     },
//     {
//         x: 190500,
//         y: 12200,
//         r: 4,
//         id: 1001063191,
//         picture: 'https://galeria.autotrader.pl/mid/7/77/ea/1572a091698377d9106e63ea0b22ee2625689039.jpg',
//         url: '/oferta/volkswagen-golf-tychy-1001063191',
//         year: 2005
//     },
//     {
//         x: 148000,
//         y: 41900,
//         r: 4,
//         id: 1001063074,
//         picture: 'https://galeria.autotrader.pl/mid/f/46/96/7bf32d39151846c372e2de966f16d572d5094497.jpg',
//         url: '/oferta/volkswagen-golf-wodzislaw-slaski-1001063074',
//         year: 2014
//     },
//     {
//         x: 152000,
//         y: 23500,
//         r: 4,
//         id: 1001062684,
//         picture: 'https://galeria.autotrader.pl/mid/7/1d/5c/0c7d225681f31d8ac4e9455ce8ee6e5f0c873a31.jpg',
//         url: '/oferta/volkswagen-golf-stalowa-wola-1001062684',
//         year: 2013
//     },
//     {
//         x: 189000,
//         y: 28900,
//         r: 4,
//         id: 1001062679,
//         picture: 'https://galeria.autotrader.pl/mid/1/47/15/5e125ef70c1c47c518890f15f4c912bfa6d6b9f3.jpg',
//         url: '/oferta/volkswagen-golf-konstantynow-lodzki-1001062679',
//         year: 2015
//     },
//     {
//         x: 267000,
//         y: 17900,
//         r: 4,
//         id: 1001062079,
//         picture: 'https://galeria.autotrader.pl/mid/7/3a/38/0f7a9fdef9d83adbf325323827dd3b690064bbdb.jpg',
//         url: '/oferta/volkswagen-golf-lublin-1001062079',
//         year: 2009
//     },
//     {
//         x: 168000,
//         y: 25800,
//         r: 4,
//         id: 1001061764,
//         picture: 'https://galeria.autotrader.pl/mid/5/27/0a/005cf0ae087227c25740530a86d9c9908411fbbf.jpg',
//         url: '/oferta/volkswagen-golf-czestochowa-1001061764',
//         year: 2009
//     },
//     {
//         x: 108425,
//         y: 45900,
//         r: 4,
//         id: 1001061450,
//         picture: 'https://galeria.autotrader.pl/mid/5/98/58/585fe2cc7fd098be2d554f58a7a1efee9d538d4e.jpg',
//         url: '/oferta/volkswagen-golf-krakow-1001061450',
//         year: 2015
//     },
//     {
//         x: 259000,
//         y: 26900,
//         r: 4,
//         id: 1001061379,
//         picture: 'https://galeria.autotrader.pl/mid/1/47/15/5e125ef70c1c47c518890f15f4c912bfa6d6b9f3.jpg',
//         url: '/oferta/volkswagen-golf-konstantynow-lodzki-1001061379',
//         year: 2015
//     },
//     {
//         x: 212000,
//         y: 27900,
//         r: 4,
//         id: 1001061378,
//         picture: 'https://galeria.autotrader.pl/mid/1/47/15/5e125ef70c1c47c518890f15f4c912bfa6d6b9f3.jpg',
//         url: '/oferta/volkswagen-golf-konstantynow-lodzki-1001061378',
//         year: 2015
//     },
//     {
//         x: 130000,
//         y: 54500,
//         r: 4,
//         id: 1001061339,
//         picture: 'https://galeria.autotrader.pl/mid/c/3a/43/37ce4e12ce493aeabf4e76436b4ffc7a2f217542.jpg',
//         url: '/oferta/volkswagen-golf-warszawa-1001061339',
//         year: 2014
//     },
//     {
//         x: 157000,
//         y: 16500,
//         r: 4,
//         id: 1001061290,
//         picture: 'https://galeria.autotrader.pl/mid/8/0f/c2/d6816eb6aa330f6df89de0c262a2499f221b38df.jpg',
//         url: '/oferta/volkswagen-golf-pyzdry-1001061290',
//         year: 2005
//     },
//     {
//         x: 130151,
//         y: 41199,
//         r: 4,
//         id: 1001060952,
//         picture: 'https://galeria.autotrader.pl/mid/e/8d/59/72e2951e88268d508549255974e0faed431921fc.jpg',
//         url: '/oferta/volkswagen-golf-klaudyn-1001060952',
//         year: 2015
//     },
//     {
//         x: 142500,
//         y: 18800,
//         r: 4,
//         id: 1001059572,
//         picture: 'https://galeria.autotrader.pl/mid/e/87/e6/79e941195db98718adfee9e66afde7bee5a6c13d.jpg',
//         url: '/oferta/volkswagen-golf-gorzow-wlkp-1001059572',
//         year: 2006
//     },
//     {
//         x: 115104,
//         y: 44900,
//         r: 4,
//         id: 1001058044,
//         picture: 'https://galeria.autotrader.pl/mid/7/64/cc/e2764bf0a1da64a8da9e76ccbf9266c74711afd5.jpg',
//         url: '/oferta/volkswagen-golf-sosnowiec-1001058044',
//         year: 2015
//     },
//     {
//         x: 75695,
//         y: 24900,
//         r: 4,
//         id: 1001057833,
//         picture: 'https://galeria.autotrader.pl/mid/1/c7/4f/c21d15f15c2cc71ba8938d4f767130c1b9143ac4.jpg',
//         url: '/oferta/volkswagen-golf-lodz-1001057833',
//         year: 2007
//     },
//     {
//         x: 178000,
//         y: 25900,
//         r: 4,
//         id: 1001057297,
//         picture: 'https://galeria.autotrader.pl/mid/e/51/64/00e08cbb515d5195122f48648513125607697b6a.jpg',
//         url: '/oferta/volkswagen-golf-lodz-1001057297',
//         year: 2009
//     },
//     {
//         x: 174000,
//         y: 29500,
//         r: 4,
//         id: 1001057281,
//         picture: 'https://galeria.autotrader.pl/mid/5/db/98/185f6ea030b2db0a688b7398f6c62a3be9c5c6ec.jpg',
//         url: '/oferta/volkswagen-golf-zyrardow-1001057281',
//         year: 2012
//     },
//     {
//         x: 89000,
//         y: 45000,
//         r: 4,
//         id: 1001057267,
//         picture: 'https://galeria.autotrader.pl/mid/d/94/cf/53da9b7d979a944fc51fafcff5b1f0db9c2da945.jpg',
//         url: '/oferta/volkswagen-golf-elblag-1001057267',
//         year: 2015
//     },
//     {
//         x: 22664,
//         y: 59000,
//         r: 4,
//         id: 1001056461,
//         picture: 'https://galeria.autotrader.pl/mid/d/74/77/47da9c865d5774dcc6603577ecbeafda0aa19574.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001056461',
//         year: 2016
//     },
//     {
//         x: 72000,
//         y: 59900,
//         r: 4,
//         id: 1001055918,
//         picture: 'https://galeria.autotrader.pl/mid/8/8f/31/06802075400d8fe44ce1d13184c843949b880ca7.jpg',
//         url: '/oferta/volkswagen-golf-falenty-janki-1001055918',
//         year: 2016
//     },
//     {
//         x: 212000,
//         y: 18400,
//         r: 4,
//         id: 1001055847,
//         picture: 'https://galeria.autotrader.pl/mid/c/27/d0/4acc80e4cdf32715573acdd094cf20a40d9cc5c0.jpg',
//         url: '/oferta/volkswagen-golf-goczalkowice-zdroj-1001055847',
//         year: 2008
//     },
//     {
//         x: 155282,
//         y: 15500,
//         r: 4,
//         id: 1001055697,
//         picture: 'https://galeria.autotrader.pl/mid/f/55/78/0afe221de4d255e4fdc98a78b5855e3d32b2f976.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001055697',
//         year: 2005
//     },
//     {
//         x: 19622,
//         y: 52200,
//         r: 4,
//         id: 1001031243,
//         picture: 'https://galeria.autotrader.pl/mid/5/db/05/cc552f67029adb98245f5705d686fac2d91958df.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001031243',
//         year: 2016
//     },
//     {
//         x: 31326,
//         y: 55000,
//         r: 4,
//         id: 1001039540,
//         picture: 'https://galeria.autotrader.pl/mid/a/4f/4d/1ba522fec2bb4f42ccb3ee4d235676e83a487bac.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001039540',
//         year: 2014
//     },
//     {
//         x: 7,
//         y: 67000,
//         r: 4,
//         id: 1001044378,
//         picture: 'https://galeria.autotrader.pl/mid/4/e0/ab/014b30784fd4e0be5f043cab20d88d6fea5b3f0e.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001044378',
//         year: 2017
//     },
//     {
//         x: 8,
//         y: 67000,
//         r: 4,
//         id: 1001051673,
//         picture: 'https://galeria.autotrader.pl/mid/d/50/2c/f4de24a0ac02500d950eff2c3c11c855db95cad7.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001051673',
//         year: 2017
//     },
//     {
//         x: 179000,
//         y: 36900,
//         r: 4,
//         id: 1001054674,
//         picture: 'https://galeria.autotrader.pl/mid/f/cc/79/58fdcf488529cceff320a37985add7e1805696b1.jpg',
//         url: '/oferta/volkswagen-golf-lodz-1001054674',
//         year: 2014
//     },
//     {
//         x: 98000,
//         y: 17900,
//         r: 4,
//         id: 1001053453,
//         picture: 'https://galeria.autotrader.pl/mid/9/3c/27/309e89f23cf23cf5925af127c3f416be7af19702.jpg',
//         url: '/oferta/volkswagen-golf-poznan-1001053453',
//         year: 2007
//     },
//     {
//         x: 71354,
//         y: 58900,
//         r: 4,
//         id: 1001053133,
//         picture: 'https://galeria.autotrader.pl/mid/2/d0/cf/3c2a9fe5d898d0dfe7f786cf0a1948c21d8189ac.jpg',
//         url: '/oferta/volkswagen-golf-elk-1001053133',
//         year: 2016
//     },
//     {
//         x: 60989,
//         y: 46800,
//         r: 4,
//         id: 1001053002,
//         picture: 'https://galeria.autotrader.pl/mid/5/bb/d6/9e5c895b70aabb47879f8ad65fa46bef740b5e0c.jpg',
//         url: '/oferta/volkswagen-golf-bialystok-1001053002',
//         year: 2015
//     },
//     {
//         x: 190955,
//         y: 24900,
//         r: 4,
//         id: 1001052057,
//         picture: 'https://galeria.autotrader.pl/mid/d/39/1a/56d19cefd7123955c0510a1a760ae2b5f25ee038.jpg',
//         url: '/oferta/volkswagen-golf-szamotuly-1001052057',
//         year: 2011
//     },
//     {
//         x: 152000,
//         y: 16900,
//         r: 4,
//         id: 1001051842,
//         picture: 'https://galeria.autotrader.pl/mid/6/76/38/4d637ede560c76cfc97d4638e7603cb5fb11ca41.jpg',
//         url: '/oferta/volkswagen-golf-ostrow-mazowiecka-1001051842',
//         year: 2008
//     },
//     {
//         x: 192000,
//         y: 23999,
//         r: 4,
//         id: 1001051219,
//         picture: 'https://galeria.autotrader.pl/mid/3/e9/1f/3f3623156981e9afa6d0f91faaff82d32123fa2e.jpg',
//         url: '/oferta/volkswagen-golf-swiebodzin-1001051219',
//         year: 2012
//     },
//     {
//         x: 201877,
//         y: 11200,
//         r: 4,
//         id: 1001050285,
//         picture: 'https://galeria.autotrader.pl/mid/9/63/f1/649127450d15633c41d271f16ba2478afab5a34c.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001050285',
//         year: 2004
//     },
//     {
//         x: 169529,
//         y: 30900,
//         r: 4,
//         id: 1001048836,
//         picture: 'https://galeria.autotrader.pl/mid/4/5f/1e/3b43996d81f55fe90e48311ebe5372d03add1cc3.jpg',
//         url: '/oferta/volkswagen-golf-czestochowa-1001048836',
//         year: 2012
//     },
//     {
//         x: 195106,
//         y: 36900,
//         r: 4,
//         id: 1001048646,
//         picture: 'https://galeria.autotrader.pl/mid/7/36/5e/4f73a35d22f436c82ed0b75e509ebc82393d5adf.jpg',
//         url: '/oferta/volkswagen-golf-warszawa-1001048646',
//         year: 2014
//     },
//     {
//         x: 166608,
//         y: 48900,
//         r: 4,
//         id: 1001048645,
//         picture: 'https://galeria.autotrader.pl/mid/5/69/3f/625a7ff662f96912bb1e343f841fe7a8042b27c3.jpg',
//         url: '/oferta/volkswagen-golf-warszawa-1001048645',
//         year: 2014
//     },
//     {
//         x: 157189,
//         y: 34000,
//         r: 4,
//         id: 1001048140,
//         picture: 'https://galeria.autotrader.pl/mid/c/87/6f/99c00b6bdbc987ad5fcc0d6f393029b43e6c7ea4.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001048140',
//         year: 2014
//     },
//     {
//         x: 77969,
//         y: 44000,
//         r: 4,
//         id: 1001047908,
//         picture: 'https://galeria.autotrader.pl/mid/5/37/02/1b5e41e3ceb8379b95374c028cb661624944aee4.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001047908',
//         year: 2014
//     },
//     {
//         x: 122765,
//         y: 42999,
//         r: 4,
//         id: 1001047091,
//         picture: 'https://galeria.autotrader.pl/mid/1/7a/14/4b148178d1287ab6872b8514ec655e0b5057362c.jpg',
//         url: '/oferta/volkswagen-golf-klaudyn-1001047091',
//         year: 2014
//     },
//     {
//         x: 271000,
//         y: 8400,
//         r: 4,
//         id: 1001046303,
//         picture: 'https://galeria.autotrader.pl/mid/f/56/ac/2ef7122e1bf6561aa3674bace5055f3f44af7a12.jpg',
//         url: '/oferta/volkswagen-golf-otmuchow-1001046303',
//         year: 2002
//     },
//     {
//         x: 89240,
//         y: 34200,
//         r: 4,
//         id: 1001045758,
//         picture: 'https://galeria.autotrader.pl/mid/5/b9/59/965747700b70b954891569591d29af48e8607735.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001045758',
//         year: 2012
//     },
//     {
//         x: 160830,
//         y: 39000,
//         r: 4,
//         id: 1001043570,
//         picture: 'https://galeria.autotrader.pl/mid/8/4f/fc/2a84599dab724f8c2a62d9fc3986ac9fb2e2012c.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001043570',
//         year: 2014
//     },
//     {
//         x: 96515,
//         y: 34400,
//         r: 4,
//         id: 1001042837,
//         picture: 'https://galeria.autotrader.pl/mid/1/44/bc/cc188dde5a5d444bb9b14fbc42353f7ae1cda40a.jpg',
//         url: '/oferta/volkswagen-golf-grzedy-1001042837',
//         year: 2015
//     },
//     {
//         x: 163000,
//         y: 22800,
//         r: 4,
//         id: 1001042373,
//         picture: 'https://galeria.autotrader.pl/mid/b/ea/ee/67bac0db9e68ea2159b588ee4039e73a5ab88e74.jpg',
//         url: '/oferta/volkswagen-golf-opole-1001042373',
//         year: 2009
//     },
//     {
//         x: 143976,
//         y: 26300,
//         r: 4,
//         id: 1001042122,
//         picture: 'https://galeria.autotrader.pl/mid/5/c8/c4/a35052d4c8a5c83a7b34ccc4940f4408fca2c280.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001042122',
//         year: 2008
//     },
//     {
//         x: 9,
//         y: 67000,
//         r: 4,
//         id: 1001042101,
//         picture: 'https://galeria.autotrader.pl/mid/9/64/7f/da93b4969f8864d48cfee77fa92ef8e279af4d2e.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001042101',
//         year: 2017
//     },
//     {
//         x: 150000,
//         y: 11900,
//         r: 4,
//         id: 1001041987,
//         picture: 'https://galeria.autotrader.pl/mid/1/13/5b/2c1d6f5391e813958493ef5b97f10c04d6017c52.jpg',
//         url: '/oferta/volkswagen-golf-goczalkowice-zdroj-1001041987',
//         year: 1989
//     },
//     {
//         x: 240000,
//         y: 16500,
//         r: 4,
//         id: 1001040951,
//         picture: 'https://galeria.autotrader.pl/mid/0/3b/a8/5d002ff3fd573be2aaa97da83af61dd1f9a95438.jpg',
//         url: '/oferta/volkswagen-golf-pyzdry-1001040951',
//         year: 2008
//     },
//     {
//         x: 79000,
//         y: 39900,
//         r: 4,
//         id: 1001039197,
//         picture: 'https://galeria.autotrader.pl/mid/8/d5/f1/3e813475d950d583962263f1b503a96779995520.jpg',
//         url: '/oferta/volkswagen-golf-poznan-1001039197',
//         year: 2010
//     },
//     {
//         x: 1400,
//         y: 21500,
//         r: 4,
//         id: 1001038113,
//         picture: 'https://galeria.autotrader.pl/mid/8/75/88/9d84909cabda75db8c04508885f2d1ea3b01561b.jpg',
//         url: '/oferta/volkswagen-golf-koscierzyna-1001038113',
//         year: 2008
//     },
//     {
//         x: 0,
//         y: 14500,
//         r: 4,
//         id: 1001035357,
//         picture: 'https://galeria.autotrader.pl/mid/d/59/c8/aed3bccce2305988fd99adc892897222b9c435a4.jpg',
//         url: '/oferta/volkswagen-golf-slupsk-1001035357',
//         year: 2004
//     },
//     {
//         x: 118000,
//         y: 49500,
//         r: 4,
//         id: 1001034240,
//         picture: 'https://galeria.autotrader.pl/mid/0/bc/61/bf0fa59497a5bcd12c854f61c2343a51187a7baf.jpg',
//         url: '/oferta/volkswagen-golf-warszawa-1001034240',
//         year: 2015
//     },
//     {
//         x: 144616,
//         y: 42000,
//         r: 4,
//         id: 1001034039,
//         picture: 'https://galeria.autotrader.pl/mid/5/03/56/8b5b04e14856039b88e2f9561e0c1f58363e11bf.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001034039',
//         year: 2014
//     },
//     {
//         x: 203440,
//         y: 11900,
//         r: 4,
//         id: 1001033462,
//         picture: 'https://galeria.autotrader.pl/mid/a/99/82/52a44fbf54da99dc9acdfc82e25453c9207be952.jpg',
//         url: '/oferta/volkswagen-golf-krakow-1001033462',
//         year: 2003
//     },
//     {
//         x: 119000,
//         y: 20900,
//         r: 4,
//         id: 1001033168,
//         picture: 'https://galeria.autotrader.pl/mid/d/bf/3e/2dd632fc1298bf087af54c3e16d88b4a06a57ef8.jpg',
//         url: '/oferta/volkswagen-golf-zlotniki-kujawskie-1001033168',
//         year: 2010
//     },
//     {
//         x: 189000,
//         y: 22600,
//         r: 4,
//         id: 1001033038,
//         picture: 'https://galeria.autotrader.pl/mid/f/28/82/f1ffe73bf96528757880a082c8d0ae73de0543b6.jpg',
//         url: '/oferta/volkswagen-golf-zdunska-wola-1001033038',
//         year: 2008
//     },
//     {
//         x: 132314,
//         y: 39000,
//         r: 4,
//         id: 1001032449,
//         picture: 'https://galeria.autotrader.pl/mid/6/d3/e1/486d68d58937d3c8f99d0de1e5fc90e0ea9930fe.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001032449',
//         year: 2015
//     },
//     {
//         x: 131384,
//         y: 39500,
//         r: 4,
//         id: 1001031711,
//         picture: 'https://galeria.autotrader.pl/mid/a/d6/0b/60a19b645d45d6032dfdc40b8a0f73df1650cde1.jpg',
//         url: '/oferta/volkswagen-golf-laziska-gorne-1001031711',
//         year: 2013
//     },
//     {
//         x: 145360,
//         y: 38500,
//         r: 4,
//         id: 1001031231,
//         picture: 'https://galeria.autotrader.pl/mid/7/48/de/967c9fde217548b829db35de8d9997ebacb3f7a5.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001031231',
//         year: 2015
//     },
//     {
//         x: 181000,
//         y: 6800,
//         r: 4,
//         id: 1001030579,
//         picture: 'https://galeria.autotrader.pl/mid/d/6f/60/ebdf0c791d576f10e1ce5e6033d1e6add105b44d.jpg',
//         url: '/oferta/volkswagen-golf-opole-1001030579',
//         year: 1998
//     },
//     {
//         x: 163000,
//         y: 27900,
//         r: 4,
//         id: 1001030576,
//         picture: 'https://galeria.autotrader.pl/mid/1/b6/06/fb138af18415b603163af6067e6ee13046e31344.jpg',
//         url: '/oferta/volkswagen-golf-dabrowka-1001030576',
//         year: 2009
//     },
//     {
//         x: 137303,
//         y: 24400,
//         r: 4,
//         id: 1001030324,
//         picture: 'https://galeria.autotrader.pl/mid/c/18/1a/6cc77e4e932b18ff5643ce1ae65b17c644de77fc.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001030324',
//         year: 2008
//     },
//     {
//         x: 86000,
//         y: 56500,
//         r: 4,
//         id: 1001029652,
//         picture: 'https://galeria.autotrader.pl/mid/0/c1/a6/8204f86d7152c1b60b1b98a6792eb670b101c10c.jpg',
//         url: '/oferta/volkswagen-golf-warszawa-1001029652',
//         year: 2015
//     },
//     {
//         x: 58811,
//         y: 59699,
//         r: 4,
//         id: 1001029585,
//         picture: 'https://galeria.autotrader.pl/mid/4/3e/70/12435160c0953ec6b40174700373e2695c31ee38.jpg',
//         url: '/oferta/volkswagen-golf-klaudyn-1001029585',
//         year: 2015
//     },
//     {
//         x: 131211,
//         y: 31700,
//         r: 4,
//         id: 1001028621,
//         picture: 'https://galeria.autotrader.pl/mid/1/b5/d5/b31dcb4fe4dcb5c8a7a34ad5fce7e1448fa7079d.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001028621',
//         year: 2010
//     },
//     {
//         x: 152000,
//         y: 32500,
//         r: 4,
//         id: 1001027227,
//         picture: 'https://galeria.autotrader.pl/mid/1/96/4f/e21b470299da96e05e2d4b4ff2795b46c34ef5fc.jpg',
//         url: '/oferta/volkswagen-golf-debica-1001027227',
//         year: 2014
//     },
//     {
//         x: 307000,
//         y: 7900,
//         r: 4,
//         id: 1001026672,
//         picture: 'https://galeria.autotrader.pl/mid/4/81/87/c149739b68ab816faee70c87024da151e2ce6e39.jpg',
//         url: '/oferta/volkswagen-golf-ostrow-mazowiecka-1001026672',
//         year: 1999
//     },
//     {
//         x: 214000,
//         y: 20900,
//         r: 4,
//         id: 1001026389,
//         picture: 'https://galeria.autotrader.pl/mid/a/97/c4/d1a7afeb69979750e0faa0c48f7b0ee1d1228876.jpg',
//         url: '/oferta/volkswagen-golf-zory-1001026389',
//         year: 2009
//     },
//     {
//         x: 228000,
//         y: 24900,
//         r: 4,
//         id: 1001025805,
//         picture: 'https://galeria.autotrader.pl/mid/7/b4/9d/9c7082652829b4c08fe44e9d9fce0c2be01489ce.jpg',
//         url: '/oferta/volkswagen-golf-warszawa-1001025805',
//         year: 2011
//     },
//     {
//         x: 114000,
//         y: 41500,
//         r: 4,
//         id: 1001025300,
//         picture: 'https://galeria.autotrader.pl/mid/e/cd/f8/7ce36c324ca7cdeeeb40ddf8ea6f048564c737e9.jpg',
//         url: '/oferta/volkswagen-golf-debica-1001025300',
//         year: 2014
//     },
//     {
//         x: 43714,
//         y: 81990,
//         r: 4,
//         id: 1001024718,
//         picture: 'https://galeria.autotrader.pl/mid/0/98/98/0b0c3699565698e703291e98d9e0adceda39a93b.jpg',
//         url: '/oferta/volkswagen-golf-falenty-janki-1001024718',
//         year: 2017
//     },
//     {
//         x: 147000,
//         y: 23700,
//         r: 4,
//         id: 1001023327,
//         picture: 'https://galeria.autotrader.pl/mid/5/98/c4/095fd2e838b198259e233cc4c23fd53aab820e93.jpg',
//         url: '/oferta/volkswagen-golf-swiebodzin-1001023327',
//         year: 2009
//     },
//     {
//         x: 179000,
//         y: 25900,
//         r: 4,
//         id: 1001022635,
//         picture: 'https://galeria.autotrader.pl/mid/2/e6/c6/582c930646b0e640b87c1ac61ed2ecc13ca649ad.jpg',
//         url: '/oferta/volkswagen-golf-warszawa-1001022635',
//         year: 2010
//     },
//     {
//         x: 176165,
//         y: 37000,
//         r: 4,
//         id: 1001022006,
//         picture: 'https://galeria.autotrader.pl/mid/2/f0/e3/252d6e910204f005dd3724e3aed21410d6b0d7cf.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001022006',
//         year: 2014
//     },
//     {
//         x: 183339,
//         y: 33000,
//         r: 4,
//         id: 1001022003,
//         picture: 'https://galeria.autotrader.pl/mid/8/36/46/97858ebde60436a815b4a2466a13cdf3638d9295.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001022003',
//         year: 2014
//     },
//     {
//         x: 118048,
//         y: 43900,
//         r: 4,
//         id: 1001020495,
//         picture: 'https://galeria.autotrader.pl/mid/b/6b/bf/1bbf4568f2aa6b70196ea3bf0a7c00b0752d1c2b.jpg',
//         url: '/oferta/volkswagen-golf-krakow-1001020495',
//         year: 2015
//     },
//     {
//         x: 234193,
//         y: 24900,
//         r: 4,
//         id: 1001020394,
//         picture: 'https://galeria.autotrader.pl/mid/a/7f/40/3aa1f57730637f4157373040bbc8bf192aaa0c83.jpg',
//         url: '/oferta/volkswagen-golf-olsztyn-1001020394',
//         year: 2010
//     },
//     {
//         x: 204000,
//         y: 43500,
//         r: 4,
//         id: 1001019068,
//         picture: 'https://galeria.autotrader.pl/mid/c/8e/27/e6c2b1664cb08ea7abebfb27b3667911f0215e99.jpg',
//         url: '/oferta/volkswagen-golf-1001019068',
//         year: 2010
//     },
//     {
//         x: 65000,
//         y: 54900,
//         r: 4,
//         id: 1001018066,
//         picture: 'https://galeria.autotrader.pl/mid/9/44/98/db968d9732cc445214a85b987e048f4dea314550.jpg',
//         url: '/oferta/volkswagen-golf-konstantynow-lodzki-1001018066',
//         year: 2014
//     },
//     {
//         x: 246000,
//         y: 22900,
//         r: 4,
//         id: 1001017727,
//         picture: 'https://galeria.autotrader.pl/mid/1/15/0f/2a16e213d98e153132bf800f95331316c0c31481.jpg',
//         url: '/oferta/volkswagen-golf-zdunska-wola-1001017727',
//         year: 2008
//     },
//     {
//         x: 208985,
//         y: 17900,
//         r: 4,
//         id: 1001017685,
//         picture: 'https://galeria.autotrader.pl/mid/0/d9/6a/ce0bffc0669ed9c3c5704f6ad36e81c1ed9e3049.jpg',
//         url: '/oferta/volkswagen-golf-szamotuly-1001017685',
//         year: 2006
//     },
//     {
//         x: 132858,
//         y: 43900,
//         r: 4,
//         id: 1001016823,
//         picture: 'https://galeria.autotrader.pl/mid/2/95/72/162e5de7c5ff954b5228f4721d441ab66de17667.jpg',
//         url: '/oferta/volkswagen-golf-chorzow-1001016823',
//         year: 2015
//     },
//     {
//         x: 105354,
//         y: 41300,
//         r: 4,
//         id: 1001016655,
//         picture: 'https://galeria.autotrader.pl/mid/1/bc/48/b110b7dd6f26bc3aa56ffa48d6efee214a32bf71.jpg',
//         url: '/oferta/volkswagen-golf-ozarow-mazowiecka-1001016655',
//         year: 2015
//     },
//     {
//         x: 149000,
//         y: 4700,
//         r: 4,
//         id: 1001015911,
//         picture: 'https://galeria.autotrader.pl/mid/6/c2/cc/0e6da6e3adc7c26b4c0dd4ccd501c2d80ed46a64.jpg',
//         url: '/oferta/volkswagen-golf-pyzdry-1001015911',
//         year: 1998
//     },
//     {
//         x: 75313,
//         y: 42000,
//         r: 4,
//         id: 1001014721,
//         picture: 'https://galeria.autotrader.pl/mid/3/ae/60/343c9200a160aee854b17d609553b1613c6b1933.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001014721',
//         year: 2014
//     },
//     {
//         x: 232000,
//         y: 19900,
//         r: 4,
//         id: 1001013687,
//         picture: 'https://galeria.autotrader.pl/mid/b/03/a8/a3b8061d819203fa6d4b57a84660698a1417f821.jpg',
//         url: '/oferta/volkswagen-golf-ostrow-mazowiecka-1001013687',
//         year: 2008
//     },
//     {
//         x: 18700,
//         y: 69000,
//         r: 4,
//         id: 1001013349,
//         picture: 'https://galeria.autotrader.pl/mid/8/b8/7e/0980f0aa43dab876d60cf97e257681a0f542464e.jpg',
//         url: '/oferta/volkswagen-golf-warszawa-1001013349',
//         year: 2016
//     },
//     {
//         x: 99890,
//         y: 58900,
//         r: 4,
//         id: 1001011574,
//         picture: 'https://galeria.autotrader.pl/mid/4/59/b8/3f4b72482ec359b70b149eb835c5b979fa5291a9.jpg',
//         url: '/oferta/volkswagen-golf-srem-1001011574',
//         year: 2016
//     },
//     {
//         x: 37000,
//         y: 46800,
//         r: 4,
//         id: 1001011201,
//         picture: 'https://galeria.autotrader.pl/mid/0/81/b6/b30a745adce6811cf96e0fb61c071b6ee7c92588.jpg',
//         url: '/oferta/volkswagen-golf-opole-1001011201',
//         year: 2013
//     },
//     {
//         x: 145914,
//         y: 38000,
//         r: 4,
//         id: 1001010151,
//         picture: 'https://galeria.autotrader.pl/mid/8/03/9f/6b83d881b7eb03b45dfa059f80cc0eff33487f62.jpg',
//         url: '/oferta/volkswagen-golf-piaseczno-1001010151',
//         year: 2014
//     },
// ];
//

function setChart(xhttp) {
  var resp = JSON.parse(xhttp.response);
  console.log(resp);

  const min = resp['data']['sold_price__min'];
  const max = resp['data']['sold_price__max'];
  const avg = resp['data']['sold_price__avg'];
  document.getElementById('cheapest-price').innerText ='$' + min.toString();
  document.getElementById('average-price').innerText ='$' +  (Math.round( avg )).toString();
  document.getElementById('highest-price').innerText ='$' +  max.toString();

  window.points = [];
  window.point = [];

  var lots = resp.lots;


  lots.forEach( a => {
    var image = (a['info']['images']).split('|');
    window.points.push({
        x: a.info.odometer_orr,
        y: a.sold_price,
        r: 4,
        id: a.info.vin,
        year: a.info.year,
        picture: 'https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + image[0],
        url: '/lot/' + a.info.lot
      });
    // window.points.push({
    //     x: a.info.odometer_orr,
    //     y: a.sold_price,
    //     r: 4,
    //     id: a.info.vin,
    //     year: a.info.year,
    //     picture: a['info']['avatar'],
    //     url:'https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + image[0]
    //   });
    if (vin == a.info.vin) {
      window.point.push({
        x: a.info.odometer_orr,
        y: a.sold_price,
        r: 7,
        id: a.info.vin,
        picture: 'https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + image[0],
        year: a.info.year,
        url: '/lot/' + a.info.lot
      })
    }
  });
  var start = {
    x: window.points[0].x,
    y: window.points[0].y
  };
  var end = {
    x: window.points[0].x,
    y: window.points[0].y
  };
  window.points.forEach(point => {
    if (point.x < start.x) {
      start.x = point.x;
      start.y = point.y;
    }
    if (point.x > end.x) {
      end.x = point.x;
      end.y = point.y;
    }
  });
  window.line = [
    {
      x: start.x,
      y: start.y
    },{
      x: end.x,
      y: end.y
    }
  ];

  window.plot = new Plot({
    points: window.points,
    point: window.point,
    line: window.line,
    chartTitle: window.chartTitle
  });

  plot.init();
  console.log(window.points);
}

var numberWithCommas = function (x)
{
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

// window.line = [{
//         x: 0,
//         y: 37649
//     },
//     {
//         x: 313000,
//         y: 27696
//     },
// ];
//
// window.plot = new Plot({
//     point: window.point,
//     points: window.points,
//     line: window.line,
//     chartTitle: window.chartTitle
// });
//
// plot.init();
