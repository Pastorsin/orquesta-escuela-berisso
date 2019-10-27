class Search {

    constructor() {
        this.initSelectors()
        this.initEvents()
    }

    initSelectors() {
        this.searchInput = document.querySelector("#search")
        this.rowsSelector = document.querySelectorAll(".user-row")
        this.searchButton = document.querySelector("#search-button")
        this.activeCheckbox = document.querySelector("#active-checkbox")
    }

    initEvents() {
    	this.searchInput.addEventListener("keyup", this.start.bind(this))
    	this.searchButton.addEventListener("clickup", this.start.bind(this))
    	this.activeCheckbox.addEventListener("change", this.start.bind(this))
    }

    start() {
        this.hideRows()
        let result = this.search()
        this.showRows(result)
    }

    hideRows() {
        this.rowsSelector.forEach((row) => row.style.display = 'none')
    }

	search() {
        let value = this.searchInput.value.trim()		
		let rows = Array.from(this.rowsSelector) 
        return rows.filter((row) => this.satisfy(row, value))
    }

    satisfy(row, value) {
        return this.includesUsername(row, value) && this.isActive(row, value)
    }

    includesUsername(row, value) {
    	let selector = row.querySelector(".username")
    	let username = selector.textContent
        return username.includes(value)
    }

    isActive(row, value) {
    	let checked = $("#active-checkbox").is(":checked")
    	if (!checked) {
    		return true
    	} else {
    		let selector = row.querySelector(".user-active")
    		let userActive = selector.getAttribute("active")
    		return Boolean(Number(userActive))
    	}    	
    }

    showRows(rows) {
        rows.forEach((row) => row.style.display = '');
    }
}


$(document).ready(() => {
	const search = new Search()
});