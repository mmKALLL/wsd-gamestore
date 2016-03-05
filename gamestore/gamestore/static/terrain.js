
var canvas = document.getElementById("canvas");
var g = canvas.getContext("2d");
var terrain = [];
var load = 0;
var idleTimer;
var phase = 0;
var turn = 0;
var selection = { active: false, x: 0, y: 0 };
var gameOn = false;
var gameStateClear = false;
var gameStateFailure = false;

// Kaksi apufunktiota RGB-arvojen muuttamiseen värikoodeiksi.

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

/* Peli toimii yksinomaan hiirellä. Tämä funktio lisää pelille kuuntelijan, joka kutsuu ohjelman muita
 * funktioita käyttäjän klikkauksien perusteella. Kaikki toiminnot paitsi lepoanimaatio alkavat täältä.
 */

function events () {
	canvas.addEventListener("click", function (event) {
		if (gameOn) {
			x = event.offsetX;
        	y = event.offsetY;
			if (x > 1 && x < 602 && y > 1 && y < 602) {
				x = Math.floor((x - 2) / 24);
				y = Math.floor((y - 2) / 24);
				if (selection.active) {
					if (x == selection.x && y == selection.y) {
						selection.active = false;
					} else {
						selection.x = x;
						selection.y = y;
					}
				} else {
					selection.active = true;
					selection.x = x;
					selection.y = y;
				}
				requestAnimationFrame(draw);
			} else if (x > 653 && x < 729 && y > 374 && y < 450 && !gameStateClear && !gameStateFailure) {
				activeTile = terrain[selection.x][selection.y];
				if (selection.active && activeTile.type == "plains" && activeTile.elevation < 12) {
					activeTile.elevation += 1;
					activeTile.color = rgbToHex(100, 255 - (activeTile.elevation * 5), 150);
					tick();
					if (!gameStateClear && !gameStateFailure) {
						up.play();
					} else if (gameStateFailure) {
						splash.play();
					} else {
						victory.play();
					}
				}
			} else if (x > 778 && x < 854 && y > 374 && y < 450 && !gameStateClear && !gameStateFailure) {
				activeTile = terrain[selection.x][selection.y];
				if (selection.active && activeTile.type == "plains" && activeTile.elevation > 1) {
					activeTile.elevation -= 1;
					activeTile.color = rgbToHex(100, 255 - (activeTile.elevation * 5), 150);
					tick();
					if (!gameStateClear && !gameStateFailure) {
						down.play();
					} else if (gameStateFailure) {
						splash.play();
					} else {
						victory.play();
					}
				}
			} else if (x > 653 && x < 858 && y > 526 && y < 581) {
				reset();
			}
		} else {
			gameOn = true;
			requestAnimationFrame(draw);
		}
	});
}

/* Pelin alustusfunktio. Kutsutaan kerran aina kun uusi peli alkaa. Funktio satunnaisgeneroi kartan ja piirtää
 * ne asiat kankaalle, jotka eivät koskaan muutu. (Esim. reunat) Funktio myös käynnistää lepoanimaation.
 */

function initialize () {
	var villages = 0;
	for (var x = 0; x < 25; x++) {
		terrain[x] = []
		for (var y = 0; y < 25; y++) {
			var height = Math.floor(Math.random() * 13) + 1;
			terrain[x][y] = {
				type: "plains",
				elevation: height,
				color: rgbToHex(100, 255 - (height * 5), 150),
				positionX: x,
				positionY: y
			}
			if (height == 13) {
				terrain[x][y].type = "mountain";
			} else if (Math.random() < 0.08) {
				terrain[x][y].type = "forest";
			} else if (Math.random() < 0.02 && (x < 8 || x > 16) && (y < 8 || y > 16)) {
				terrain[x][y].type = "village";
				villages += 1;
			}
		}
	}
	if (villages == 0) {
		var placement = Math.floor(Math.random() * 25);
		if (placement > 7 && placement < 17) {
			if (Math.random() < 0.5) {
				terrain[placement][Math.floor(Math.random() * 8)].type = "village";
			} else {
				terrain[placement][Math.floor(Math.random() * 8) + 17].type = "village";
			}
		} else {
			terrain[placement][Math.floor(Math.random() * 25)].type = "village";
		}
	}
	terrain[12][12].type = "spring";
	terrain[12][12].elevation = 0;
	g.fillStyle = "#EFDFAF";
	g.fillRect(604, 2, 300, 500);
	g.fillStyle = "#AF8F6F";
	g.fillRect(604, 504, 300, 98);
	g.fillStyle = "#2D2D2D";
	g.fillRect(0, 0, 906, 2);
	g.fillRect(0, 602, 906, 2);
	g.fillRect(0, 2, 2, 600);
	g.fillRect(602, 2, 2, 600);
	g.fillRect(904, 2, 2, 600);
	g.fillRect(604, 502, 300, 2);
	g.fillRect(654, 527, 204, 54);
	g.font = "32px Yantramanav";
	var gradient = g.createLinearGradient(654, 0, 854, 0);
	gradient.addColorStop("0", "#FFFFFF");
	gradient.addColorStop("0.25", "#22FF00");
	gradient.addColorStop("0.5", "#00FFFF");
	gradient.addColorStop("0.75", "#0050FF");
	g.fillStyle = gradient;
	g.fillText("New Game", 686, 564);
	g.font = "20px Yantramanav";
	requestAnimationFrame(draw);
	idleTimer = setInterval(function () { requestAnimationFrame(idleAnimation); }, 1000);
}

/* Pelimekaniikan pääfunktio. Kutsutaan aina kun käyttäjä on pelannut vuoron. Funktio nostaa veden tasoa
 * yhdellä ja yrittää levittää sitä. Funktio myös tarkastaa, voittiko tai hävisikö käyttäjä viime siirrolla.
 */

function tick () {
	turn += 1;
	var waterArea = [];
	var spreadArea = [];
	for (var x = 0; x < 25; x++) {
		for (var y = 0; y < 25; y++) {
			currentTile = terrain[x][y];
			if (currentTile.type == "water" || currentTile.type == "spring") {
				currentTile.elevation += 1;
				waterArea.push(currentTile);
			}
		}
	}
	while (waterArea.length > 0 || spreadArea.length > 0) {
		if (waterArea.length > 0) {
			spreadArea = spread(waterArea);
			waterArea = [];
		} else if (spreadArea.length > 0) {
			waterArea = spread(spreadArea);
			spreadArea = [];
		}
	}
	requestAnimationFrame(draw);
}

/* Apufunktio veden levittämiseen. tick-funktio kutsuu tätä niin kauan kunnes vesi ei voi levitä enempää.
 * Ottaa parametrina edellisessä vaiheessa veden valtaamat tiilet ja palauttaa niiden valtaamat tiilet.
 */

function spread (area) {
	var result = [];
	var length = area.length;
	for (var i = 0; i < length; i++) {
		currentX = area[i].positionX;
		currentY = area[i].positionY;
		if (currentX - 1 >= 0) {
			spreadTile = terrain[currentX - 1][currentY];
			if (spreadTile.type == "plains" || spreadTile.type == "forest" || spreadTile.type == "village") {
				if (spreadTile.elevation <= turn) {
					if (spreadTile.type == "village")
						gameStateFailure = true;
					if (currentX - 1 == 0 && !gameStateFailure)
						gameStateClear = true;
					spreadTile.type = "water";
					spreadTile.elevation = turn;
					result.push(spreadTile);
				}
			}
		}
		if (currentY - 1 >= 0) {
			spreadTile = terrain[currentX][currentY - 1];
			if (spreadTile.type == "plains" || spreadTile.type == "forest" || spreadTile.type == "village") {
				if (spreadTile.elevation <= turn) {
					if (spreadTile.type == "village")
						gameStateFailure = true;
					if (currentY - 1 == 0 && !gameStateFailure)
						gameStateClear = true;
					spreadTile.type = "water";
					spreadTile.elevation = turn;
					result.push(spreadTile);
				}
			}
		}
		if (currentX + 1 <= 24) {
			spreadTile = terrain[currentX + 1][currentY];
			if (spreadTile.type == "plains" || spreadTile.type == "forest" || spreadTile.type == "village") {
				if (spreadTile.elevation <= turn) {
					if (spreadTile.type == "village")
						gameStateFailure = true;
					if (currentX + 1 == 24 && !gameStateFailure)
						gameStateClear = true;
					spreadTile.type = "water";
					spreadTile.elevation = turn;
					result.push(spreadTile);
				}
			}
		}
		if (currentY + 1 <= 24) {
			spreadTile = terrain[currentX][currentY + 1];
			if (spreadTile.type == "plains" || spreadTile.type == "forest" || spreadTile.type == "village") {
				if (spreadTile.elevation <= turn) {
					if (spreadTile.type == "village")
						gameStateFailure = true;
					if (currentY + 1 == 24 && !gameStateFailure)
						gameStateClear = true;
					spreadTile.type = "water";
					spreadTile.elevation = turn;
					result.push(spreadTile);
				}
			}
		}
	}
	return result;
}

/* Massiivinen piirtofunktio. Tämä funktio kutsutaan kerran pelin alussa ja sen jälkeen aina kun käyttäjä on
 * pelannut vuoron. Kaikki pelaajalle näkyvä lepoanimaatiota lukuun ottamatta piirretään täällä. Funktio
 * uudelleenpiirtää joka vuoro kartan, valitsimen ja infolaatikon. Funktio välittää myös visuaalisen
 * voitto- tai tappioilmoituksen ja piirtää pelin alussa tutoriaalin käyttäjälle.
 */

function draw () {
	animation = phase % 3;
	for (var i = 0; i < 25; i++) {
		for (var j = 0; j < 25; j++) {
			tile = terrain[i][j];
			if (tile.type != "water" && tile.type != "spring") {
				g.fillStyle = tile.color;
				g.fillRect(i * 24 + 2, j * 24 + 2, 24, 24);
				if (tile.type != "plains") {
					if (tile.type == "mountain") {
						g.drawImage(mountain, i * 24 + 2, j * 24 + 2);
					} else if (tile.type == "forest") {
						g.drawImage(forest, i * 24 + 2, j * 24 + 2);
					} else if (tile.type == "village") {
						g.drawImage(village, i * 24 + 2, j * 24 + 2);
					}
				}
			} else if (tile.type == "water") {
				switch (animation) {
					case 0:
						g.drawImage(water1, i * 24 + 2, j * 24 + 2);
						break;
					case 1:
						g.drawImage(water2, i * 24 + 2, j * 24 + 2);
						break;
					case 2:
						g.drawImage(water3, i * 24 + 2, j * 24 + 2);
						break;
				}
			} else {
				switch (animation) {
					case 0:
						g.drawImage(spring1, 290, 290);
						break;
					case 1:
						g.drawImage(spring2, 290, 290);
						break;
					case 2:
						g.drawImage(spring3, 290, 290);
						break;
				}
			}
		}
	}

	g.fillStyle = "#EFDFAF";
	g.fillRect(604, 2, 300, 500);
	if (gameStateFailure) {
		g.font = "80px Yantramanav";
		g.fillStyle = "#FF0000";
		g.fillText("FAILURE", 613, 333);
		g.font = "20px Yantramanav";
	} else if (gameStateClear) {
		g.font = "bold 100px Yantramanav";
		var gradient = g.createLinearGradient(604, 0, 904, 0);
		gradient.addColorStop("0", "#22FF00");
		gradient.addColorStop("0.5", "#00FFFF");
		gradient.addColorStop("1", "#0022FF");
		g.fillStyle = gradient;
		g.fillText("CLEAR", 618, 343);
		g.font = "20px Yantramanav";
	}

	if (selection.active) {
		select();
		tile = terrain[selection.x][selection.y];
		switch (tile.type) {
			case "plains":
				g.fillStyle = tile.color;
				g.fillRect(704, 44, 24, 24);
				g.fillStyle = "black";
				g.fillText("Plains", 757, 63);
				g.fillText("Elevation: " + tile.elevation, 708, 126);
				if (!gameStateClear && !gameStateFailure) {
					g.font = "64px Yantramanav";
					if (tile.elevation < 12) {
						g.fillStyle = "#2D2D2D";
						g.fillRect(654, 375, 75, 75);
						g.fillStyle = "#64B996";
						g.fillText("⬆", 659, 437);
					}
					if (tile.elevation > 1) {
						g.fillStyle = "#2D2D2D";
						g.fillRect(779, 375, 75, 75);
						g.fillStyle = "#64FF96";
						g.fillText("⬇", 784, 437);
					}
					g.font = "20px Yantramanav";
				}
				break;
			case "spring":
				switch (animation) {
					case 0:
						g.drawImage(spring1, 704, 44);
						break;
					case 1:
						g.drawImage(spring2, 704, 44);
						break;
					case 2:
						g.drawImage(spring3, 704, 44);
						break;
				}
				g.fillStyle = "black";
				g.fillText("Spring", 756, 63);
				g.fillText("Level: " + tile.elevation, 728, 126);
				break;
			case "water":
				switch (animation) {
					case 0:
						g.drawImage(water1, 704, 44);
						break;
					case 1:
						g.drawImage(water2, 704, 44);
						break;
					case 2:
						g.drawImage(water3, 704, 44);
						break;
				}
				g.fillStyle = "black";
				g.fillText("Water", 757, 63);
				g.fillText("Level: " + tile.elevation, 728, 126);
				break;
			case "mountain":
				g.fillStyle = tile.color;
				g.fillRect(704, 44, 24, 24);
				g.drawImage(mountain, 704, 44);
				g.fillStyle = "black";
				g.fillText("Mountain", 745, 63);
				g.fillText("Impassable", 718, 126);
				break;
			case "forest":
				g.fillStyle = tile.color;
				g.fillRect(704, 44, 24, 24);
				g.drawImage(forest, 704, 44);
				g.fillStyle = "black";
				g.fillText("Forest", 756, 63);
				g.fillText("Elevation: " + tile.elevation, 708, 126);
				break;
			case "village":
				g.fillStyle = tile.color;
				g.fillRect(704, 44, 24, 24);
				g.drawImage(village, 704, 44);
				g.fillStyle = "black";
				g.fillText("Village", 754, 63);
				g.fillText("Elevation: " + tile.elevation, 708, 126);
				break;
		}
	}

	if (!gameOn) {
		g.fillStyle = "#2D2D2D";
		g.fillRect(104, 104, 400, 400);
		g.fillStyle = "#64DC96";
		g.fillRect(119, 316, 24, 24);
		g.fillStyle = "#FFFFFF";
		g.font = "32px Yantramanav";
		g.fillText("Terrain", 259, 145);
		g.font = "16px Yantramanav";
		g.fillText("In this game, your goal is to guide the rising water to the", 119, 176);
		g.fillText("edge of the map without letting it flood any villages. You", 119, 198);
		g.fillText("accomplish this by controlling the ground level.", 119, 220);
		g.fillText("Since every map is randomly generated, it is not always", 119, 262);
		g.fillText("possible to win. You can start a new game at any time.", 119, 284);
		g.drawImage(mountain, 119, 346);
		g.drawImage(forest, 119, 376);
		g.drawImage(village, 119, 406);
		g.drawImage(spring1, 119, 436);
		g.drawImage(water1, 119, 466);
		g.fillText("Plains  -  You can raise or lower a plain once per turn", 155, 333);
		g.fillText("Mountain  -  Water can never pass through them", 155, 363);
		g.fillText("Forest  -  These don't stop the water", 155, 393);
		g.fillText("Village  -  Don't let a single one sink or you lose!", 155, 423);
		g.fillText("Spring  -  The source of the water", 155, 453);
		g.fillText("Water  -  Water level rises by one every turn, beware!", 155, 483);
		g.font = "20px Yantramanav";
	}
}

// Apufunktio valitsimen piirtämiseen. Piirtofunktio ja lepoanimaatiofunktio kutsuvat tätä.

function select () {
	x = selection.x;
	y = selection.y;
	g.fillStyle = "#FF0000";
	g.fillRect((x * 24) + 2, (y * 24) + 2, 24, 2);
	g.fillRect((x * 24) + 2, ((y + 1) * 24), 24, 2);
	g.fillRect((x * 24) + 2, (y * 24) + 4, 2, 20);
	g.fillRect(((x + 1) * 24), (y * 24) + 4, 2, 20);
}

/* Funktio uuden pelin aloittamiseen. Nollaa kaikki pelimekaniikan kannalta olennaiset muuttujat ja alustaa
 * pelin uudelleen. Kutsutaan aina kun pelaaja painaa New Game -nappulaa.
 */

function reset () {
	clearInterval(idleTimer);
	turn = 0;
	selection.active = false;
	gameStateClear = false;
	gameStateFailure = false;
	initialize();
}

var w = window;
requestAnimationFrame = w.requestAnimationFrame || w.webkitRequestAnimationFrame || w.msRequestAnimationFrame || w.mozRequestAnimationFrame;

/* Lepoanimaatiofunktio. Vesi on ainoa asia, mitä pelissä piirretään kankaalle jatkuvasti ilman käyttäjän
 * painalluksia. Tätä funktiota kutsutaan setInterval-ajastimella kerran sekunnissa.
 */

function idleAnimation () {
	phase += 1;
	animation = phase % 3;
	if (gameOn) {
		for (var i = 0; i < 25; i++) {
			for (var j = 0; j < 25; j++) {
				tile = terrain[i][j];
				if (tile.type == "water") {
					switch (animation) {
						case 0:
							g.drawImage(water1, i * 24 + 2, j * 24 + 2);
							break;
						case 1:
							g.drawImage(water2, i * 24 + 2, j * 24 + 2);
							break;
						case 2:
							g.drawImage(water3, i * 24 + 2, j * 24 + 2);
							break;
					}
				}
			}
		}
		switch (animation) {
			case 0:
				g.drawImage(spring1, 290, 290);
				break;
			case 1:
				g.drawImage(spring2, 290, 290);
				break;
			case 2:
				g.drawImage(spring3, 290, 290);
				break;
		}
		if (selection.active) {
			select();
			selectedTile = terrain[selection.x][selection.y];
			if (selectedTile.type == "water") {
				switch (animation) {
					case 0:
						g.drawImage(water1, 704, 44);
						break;
					case 1:
						g.drawImage(water2, 704, 44);
						break;
					case 2:
						g.drawImage(water3, 704, 44);
						break;
				}
			} else if (selectedTile.type == "spring") {
				switch (animation) {
					case 0:
						g.drawImage(spring1, 704, 44);
						break;
					case 1:
						g.drawImage(spring2, 704, 44);
						break;
					case 2:
						g.drawImage(spring3, 704, 44);
						break;
				}
			}
		}
	} else {
		switch (animation) {
			case 0:
				g.drawImage(spring1, 119, 436);
				g.drawImage(water1, 119, 466);
				break;
			case 1:
				g.drawImage(spring2, 119, 436);
				g.drawImage(water2, 119, 466);
				break;
			case 2:
				g.drawImage(spring3, 119, 436);
				g.drawImage(water3, 119, 466);
				break;
		}
	}
}

// Tämä pikkufunktio käynnistää pelin sitten kun kaikki kuvat on ladattu.

var loading = function () {
	load += 1;
	if (load == 9) {
		events();
		initialize();
	}
}

var spring1 = new Image();
var spring2 = new Image();
var spring3 = new Image();
var water1 = new Image();
var water2 = new Image();
var water3 = new Image();
var mountain = new Image();
var forest = new Image();
var village = new Image();
spring1.onload = function () { loading(); }
spring2.onload = function () { loading(); }
spring3.onload = function () { loading(); }
water1.onload = function () { loading(); }
water2.onload = function () { loading(); }
water3.onload = function () { loading(); }
mountain.onload = function () { loading(); }
forest.onload = function () { loading(); }
village.onload = function () { loading(); }
spring1.src = "http://dime.tml.hut.fi/~hirvonj5/Assets/lake-1.png";
spring2.src = "http://dime.tml.hut.fi/~hirvonj5/Assets/lake-2.png";
spring3.src = "http://dime.tml.hut.fi/~hirvonj5/Assets/lake-3.png";
water1.src = "http://dime.tml.hut.fi/~hirvonj5/Assets/sea-1.png";
water2.src = "http://dime.tml.hut.fi/~hirvonj5/Assets/sea-2.png";
water3.src = "http://dime.tml.hut.fi/~hirvonj5/Assets/sea-3.png";
mountain.src = "http://dime.tml.hut.fi/~hirvonj5/Assets/mountain.png";
forest.src = "http://dime.tml.hut.fi/~hirvonj5/Assets/forest.png";
village.src = "http://dime.tml.hut.fi/~hirvonj5/Assets/house-2.png";
var splash = new Audio("http://dime.tml.hut.fi/~hirvonj5/Assets/SPLASH.WAV");
var up = new Audio("http://dime.tml.hut.fi/~hirvonj5/Assets/lift2.wav");
var down = new Audio("http://dime.tml.hut.fi/~hirvonj5/Assets/gusts2.wav");
var victory = new Audio("http://dime.tml.hut.fi/~hirvonj5/Assets/fanfare.wav");
