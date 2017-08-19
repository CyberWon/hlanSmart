hlan = {};
hlan.debug=true
hlan.res = {}
hlan.menu = {}
hlan.log=function(s){
	hlan.debug && console.log(s)
}

hlan.send = function(retfun, method, params) {
	p = {};
	if(typeof(method) != "undefined" && method != '') {
		p.method = method;
	} else {
		hlan.log('method error');
		return;
	}
	if(typeof(params) == 'undefined') {
		params = {}
	}
	p.retfun = retfun;
	p.params = JSON.stringify(params);
	p.id = new Date().getTime();
	try {
		$.post(hlan.api_url, p, function(data, status) {
			msg = JSON.parse(data)
			hlan.res[msg.id] = msg.retdata
			eval(msg.retfun + '("' + msg.id + '")')
		});
	} catch(err) {
		hlan.log('-----ws_send websokect发送报错');
		hlan.log(err);
	}
	return ''

}
hlan.app_send = function(retfun,app, method, params) {
	p = {};
	if(typeof(method) != "undefined" && method != '') {
		p.method = method;
	} else {
		hlan.log('method error');
		return;
	}
	if(typeof(params) == 'undefined') {
		params = {}
	}
	p.retfun = retfun;
	p.params = JSON.stringify(params);
	p.id = new Date().getTime();

	try {
		$.post('/app/'+app, p, function(data, status) {
			msg = JSON.parse(data)
			hlan.res[msg.id] = msg.retdata
			eval(msg.retfun + '("' + msg.id + '")')
		});
	} catch(err) {
		hlan.log('-----ws_send websokect发送报错');
		hlan.log(err);
	}
	return ''
}

function getmenu() {
	$.get('/api/menu/menu1', function(res) {
		hlan.menu = JSON.parse(res);
		writemenu()
	})
}

function navmenuClick(o) {
	hlan.send('writemenu', 'menu.getmenu', {
		'navid': o
	})
}

function getnav(d) {
	var s = '';
	first = 0;
	for(i in hlan.res[d]) {
		if(first == 0) {
			first = 1
			hlan.send('writemenu', 'menu.getmenu', {
				'navid': hlan.res[d][i][0]
			})
		}
		if (hlan.res[d][i][3]!="#"){
		s = s + "<li><a class=\"J_menuItem\" href=\"" + hlan.res[d][i][3] + "\"><i class=\"fa " + hlan.res[d][i][2] + "\"></i>" + hlan.res[d][i][1] + " </a></li>";
		}else{
			s = s + "<li><a  href=\"javascript:navmenuClick('" + hlan.res[d][i][0] + "')\"><i class=\"fa " + hlan.res[d][i][2] + "\"></i>" + hlan.res[d][i][1] + " </a></li>";
		}
	}
	$('#nav_bar').html(s)
	hlan.initmenu()
	delete hlan.res[d]
}
var ws;
hlan.websocket = function() {
	ws = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws');

	ws.onopen = function() {
		// Web Socket 已连接上，使用 send() 方法发送数据
		hlan.debug && console.log('ws success connect');

	};

	ws.onmessage = function(evt) {
		try {
			var msg = JSON.parse(evt.data);
		} catch(err) {
			console.log('接受的数据格式不正确')
		}
		try {
			eval(msg.retfun + '("' + msg.retdata + '")')
		} catch(err) {
			console.log(err)
			console.log('执行' + msg.retfun + '失败')
		}

	};

	ws.onclose = function() {
		// 关闭 websocket
        hlan.debug && console.log('websocket断开链接了')

	};
}
hlan.ws_send = function(retfun, method, params) {
    /*
        exp: hlan.ws_send('print','test.mod1','')
     */
	p = {};
	if(typeof(method) != "undefined" && method != '') {
		p.method = method;
	} else {
		console.log('method error');
		return;
	}
	if(typeof(params) == 'undefined') {
		params = {}
	}
	p.retfun = retfun;
	// p.params = JSON.stringify(params);
    p.params = params;
	p.id = new Date().getTime();
	try {
		ws.send(JSON.stringify(p))
	} catch(err) {
		console.log('-----ws_send websokect发送报错');
		console.log(err);
	}

}
//IP转成整型
function _ip2int(ip) {
	var num = 0;
	ip = ip.split(".");
	num = Number(ip[0]) * 256 * 256 * 256 + Number(ip[1]) * 256 * 256 + Number(ip[2]) * 256 + Number(ip[3]);
	num = num >>> 0;
	return num;
};
//整型解析为IP地址
function _int2ip(num) {
	var str;
	var tt = new Array();
	tt[0] = (num >>> 24) >>> 0;
	tt[1] = ((num << 8) >>> 24) >>> 0;
	tt[2] = (num << 16) >>> 24;
	tt[3] = (num << 24) >>> 24;
	str = String(tt[0]) + "." + String(tt[1]) + "." + String(tt[2]) + "." + String(tt[3]);
	return str;
};
function bytesToSize(bytes) {
	if(bytes === 0) return '0 B';
	var k = 1024, // or 1024
		sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
		i = Math.floor(Math.log(bytes) / Math.log(k));

	return(bytes / Math.pow(k, i)).toPrecision(3) + ' ' + sizes[i];
}

function isEmptyObject(obj) {
	for(var key in obj) {
		//	console.log(key);
		return false;
	}
	return true;
}
hlan.login=function () {
    window.location.href=hlan.login_url+'?url='+window.location.pathname;
}
