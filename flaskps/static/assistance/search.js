class AssistanceSearch extends Search {
	satisfyText(row, value) {    	
    	return this.workshopName(row).includes(value)
    }

    workshopName(row) {
    	let selector = row.querySelector(".workshop-name")
    	let value = selector.textContent.toLowerCase()
    	return value
    }
}