function getFromUrl(url, method, formdata, callback) {
	//var data = new FormData(form);
	var xhr = new XMLHttpRequest();
	xhr.open(method, url, true);
	xhr.onload = function () {
		callback(xhr.responseText);
	}
	if (formdata) {
		xhr.send(formdata);
	}
	else {
		xhr.send();
	}
}

function isEmailTaken(email, callback) {
	getFromUrl("/acc/isEmailTaken/?email=" + encodeURIComponent(email), "get", null, function (r) {
		if (r == "AVAILABLE") {
			callback(false);
		}
		else {
			callback(r);
		}
	})
}

function checkMessages(firstTime) {
	getFromUrl("/msg/pUnreadMessages/", "get", null, function (data) {
		//console.log("Checked unread messages: Originally " + unread + ", Now " + data);
		if (data != unread) {
			unread = Number(data);
			if (unread > 0) {
				document.getElementById("unreadMessages").innerHTML = unread;
			}
			if (window.location.pathname.indexOf("/msg/") != -1 && !firstTime) {
				window.location = window.location.href;
			}
		}
	});
}

var unread = -1;
var delay = window.location.pathname.indexOf("/msg/") != -1 ? 1000 : 5000;
var messageChecker = window.setInterval(function () {
	checkMessages(false);
}, delay);

checkMessages(true);
if (window.location.pathname.indexOf("/msg/") != -1) {
	if (window.location.pathname.length > 5) {
		document.getElementsByClassName("msgsBody")[0].scrollTop = document.getElementsByClassName("msgsBody")[0].scrollHeight;
		document.getElementById("formsendmsg").onsubmit = function (e) {
			e.stopPropagation();
			e.preventDefault();
			getFromUrl("/msg/pSendMessage/", "post", new FormData(document.getElementById("formsendmsg")), function (r) {
				window.location = window.location.href;
				//console.log(r);
			});
			return 0;
		}
		document.getElementById("msgin").focus();
	}
	document.getElementById("msgCtrlBtn").onclick = function () {
		document.getElementById("msgCtrl").className = "list-group-item";
		isEmailTaken(document.getElementById("msgCtrlEmail").value, function (taken) {
			if (taken) {
				window.location = "/msg/" + taken;
			}
			else {
				document.getElementById("msgCtrl").className = "list-group-item has-error";
			}
		});
	}
}

if (window.location.pathname == "/acc/") {
	document.getElementById("registerForm").onsubmit = function (e) {
		e.stopPropagation();
		e.preventDefault();
		document.getElementById("remail").parentNode.className = "col-sm-10";
		isEmailTaken(document.getElementById("remail").value, function (taken) {
			if (!taken) {
				document.getElementById("registerAlert").innerHTML = "";
				getFromUrl("/acc/pRegister/", "post", new FormData(document.getElementById("registerForm")), function (r) {
					if (r.indexOf("Error") != -1) {
						document.getElementById("registerAlert").className = "alert alert-danger";
						document.getElementById("registerAlert").innerHTML = "<strong>Error!</strong> " + r.substring(7);
					}
					else {
						window.location = "/acc/settings/";
						//console.log("r success");
					}
				});
			}
			else {
				document.getElementById("remail").parentNode.className = "col-sm-10 has-error";
			}
		});
		return 0;
	}
	document.getElementById("signinForm").onsubmit = function (e) {
		e.stopPropagation();
		e.preventDefault();
		document.getElementById("signinAlert").innerHTML = "";
		getFromUrl("/acc/pSignin/", "post", new FormData(document.getElementById("signinForm")), function (r) {
			if (r.indexOf("Error") != -1) {
				document.getElementById("signinAlert").className = "alert alert-danger";
				document.getElementById("signinAlert").innerHTML = "<strong>Error!</strong> " + r.substring(7);
			}
			else {
				window.location = "/acc/";
				//console.log("s success");
			}
		});
		return 0;
	}
}

function refreshHashNav() {
	switch (window.location.hash) {
		case "#addressform":
			document.getElementById("settingsnav").children[0].className = "";
			document.getElementById("settingsnav").children[1].className = "active";
			document.getElementById("settingsnav").children[2].className = "";
			break;
		case "#ccinfo":
			document.getElementById("settingsnav").children[0].className = "";
			document.getElementById("settingsnav").children[1].className = "";
			document.getElementById("settingsnav").children[2].className = "active";
			break;
		default:
			document.getElementById("settingsnav").children[0].className = "active";
			document.getElementById("settingsnav").children[1].className = "";
			document.getElementById("settingsnav").children[2].className = "";
			break;
	}
}

function refreshHashNavPurchaseHistory() {
	switch (window.location.hash) {
		case "#received":
			document.getElementById("settingsnav").children[0].className = "";
			document.getElementById("settingsnav").children[1].className = "active";
			document.getElementById("settingsnav").children[2].className = "";
			break;
		case "#finishedorders":
			document.getElementById("settingsnav").children[0].className = "";
			document.getElementById("settingsnav").children[1].className = "";
			document.getElementById("settingsnav").children[2].className = "active";
			break;
		default:
			document.getElementById("settingsnav").children[0].className = "active";
			document.getElementById("settingsnav").children[1].className = "";
			document.getElementById("settingsnav").children[2].className = "";
			break;
	}
}

if (window.location.pathname == "/acc/settings/") {
	refreshHashNav();
	document.getElementById("settingsnav").onclick = function () {
		window.setTimeout(function () {
			refreshHashNav();
		}, 1);
	}
	document.getElementById("passwordform").onsubmit = function (e) {
		if (document.getElementById("password").value != document.getElementById("passwordagain").value) {
			document.getElementById("password").parentElement.className += " has-error";
			document.getElementById("passwordagain").parentElement.className += " has-error";
			e.stopPropagation();
			e.preventDefault();
			return 0;
		}
	}
}

if (window.location.pathname == "/acc/purchaseHistory/") {
	refreshHashNavPurchaseHistory();
	document.getElementById("settingsnav").onclick = function () {
		window.setTimeout(function () {
			refreshHashNavPurchaseHistory();
		}, 1);
	}
}

if (document.getElementsByClassName("jumbotron").length > 0) {
	//parallax
}

if (document.getElementById("rating")) {
	var stars = document.getElementsByClassName("star");
	for (var i = 0; i < stars.length; i++) {
		stars[i].onclick = function (e) {
			var cur = e.target.attributes["value"].value;
			for (var j = 0; j < stars.length; j++) {
				stars[j].className = j < cur ? "star n" : "star a";
			}
			document.getElementById("rating").value = cur;
		}
		stars[i].onmouseover = function (e) {
			var cur = e.target.attributes["value"].value;
			for (var j = 0; j < stars.length; j++) {
				stars[j].className = j < cur ? "star n" : "star a";
			}
		}
		stars[i].onmouseout = function (e) {
			var cur = document.getElementById("rating").value;
			for (var j = 0; j < stars.length; j++) {
				stars[j].className = j < cur ? "star n" : "star a";
			}
		}
	}
}

var tags = {};
function recalc() {
	document.getElementById("tags").value = "";
	for (var tag in tags) {
		if (tags.hasOwnProperty(tag) && tags[tag]) {
			if (document.getElementById("tags").value.length != 0)  {
				document.getElementById("tags").value += ",";
			}
			document.getElementById("tags").value += tag;
		}
	}
}
function createTagElem(name) {
	var elem = document.createElement("div");
	elem.className = "tag";
	elem.innerHTML = name + " <button class='close'>&times;</button></div>";
	document.getElementById("tagHolder").appendChild(elem);
	elem.children[0].onclick = function (e) {
		e.target.parentElement.remove();
		var tname = e.target.parentElement.innerText.substring(0, e.target.parentElement.innerText.length-2);
		tags[tname] = null;
		recalc();
	}
	return elem;
}
if (document.getElementById("tags")) {
	console.log("inside method");
	if (document.getElementById("tags").value.length > 0) {
		console.log("making defaults");
		var tagsl = document.getElementById("tags").value.split(",");
		for (var i = 0; i < tagsl.length; i++) {
			tags[tagsl[i]] = createTagElem(tagsl[i]);
			console.log("added " + tagsl[i]);
		}
	}
	document.getElementById("tagBtn").onclick = function() {
		console.log("clicked button");
		var tag = document.getElementById("tagTxt").value.replace(",","").replace("'","").replace("\"","").replace("\\","").replace("  "," ").trim();
		document.getElementById("tagTxt").value = "";
		if (tags[tag]) {
			return 0;
		}
		tags[tag] = createTagElem(tag);
		console.log("added " + tag);
		recalc();
	}
	document.getElementById("tagTxt").onkeypress = function (e) {
		if (e.keyCode == 32 || e.keyCode == 44) {
			console.log("pushed space or comma");
			var tagsl = document.getElementById("tagTxt").value.replace("'","").replace("\"","").replace("\\","").replace("  "," ").trim().split(",");
			document.getElementById("tagTxt").value = "";
			for (var i = 0; i < tagsl.length; i++) {
				if (tagsl[i] && !tags[tagsl[i]]) {
					tags[tagsl[i]] = createTagElem(tagsl[i]);
					console.log("added " + tagsl[i]);
				}
			}
			recalc();
			e.preventDefault();
			e.stopPropagation();
			return 0;
		}
	}
}