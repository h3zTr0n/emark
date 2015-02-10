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

if (window.location.pathname == "/acc/") {
	document.getElementById("registerForm").onsubmit = function (e) {
		e.stopPropagation();
		e.preventDefault();
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

if (window.location.pathname == "/acc/settings/") {
	refreshHashNav();
	document.getElementById("settingsnav").onclick = function () {
		window.setTimeout(function () {
			refreshHashNav();
		}, 1);
	}
	document.getElementById("generalform").onsubmit = function (e) {
		if (document.getElementById("password").value != document.getElementById("passwordagain").value) {
			document.getElementById("password").parentElement.className += " has-error";
			document.getElementById("passwordagain").parentElement.className += " has-error";
			e.stopPropagation();
			e.preventDefault();
			return 0;
		}
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