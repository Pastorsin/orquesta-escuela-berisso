class StudentSearch extends Search {

    satisfy(row, value) {
        return this.includesName(row, value)
    }

    fullName(row) {
    	let firstNameSelector = row.querySelector(".first-name")
    	let lastNameSelector = row.querySelector(".last-name")

    	let firstName = firstNameSelector.textContent.toLowerCase()
    	let lastName = lastNameSelector.textContent.toLowerCase()

    	return firstName + " " + lastName
    }

    includesName(row, value) {    	
    	return this.fullName(row).includes(value)
    }

}