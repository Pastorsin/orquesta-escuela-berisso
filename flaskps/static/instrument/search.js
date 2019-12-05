class InstrumentSearch extends Search {

    satisfyText(row, value) {    	
    	return this.name(row).includes(value)
    }

    name(row) {
    	let nameSelector = row.querySelector(".name")
    	let nameValue = nameSelector.textContent.toLowerCase()
    	return nameValue
    }
}