function generateList(gamelist) {
	var list = document.querySelector('#userlist')
	list.innerHTML = ''

	for (var i = 0; i <= gamelist.length - 1; i++) {
		
		var item = document.createElement('div')
		item.id="item"
		item.className = "row"
		var game = document.createElement('div')
		var cost = document.createElement('div')
		game.className ="col-sm-10"
		cost.className ="col-sm-2"
		game.innerHTML = "<b>"+gamelist[i][1].charAt(0).toUpperCase() + gamelist[i][1].slice(1)+"<b>"
		cost.innerHTML = "<b>" +gamelist[i][2]+"</b> points"
		item.appendChild(game)
		item.appendChild(cost)
		list.appendChild(item)
	}
}