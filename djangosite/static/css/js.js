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