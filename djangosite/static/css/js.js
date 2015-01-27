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