class WorkshopSearch extends Search {

    satisfyText(row, value) {    
        let workshopSelector = row.querySelector(".workshop")
        let workshopName = workshopSelector.textContent.toLowerCase()
    	return workshopName.includes(value)
    }
}