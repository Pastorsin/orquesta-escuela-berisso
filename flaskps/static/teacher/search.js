class TeacherSearch extends Search {

    satisfyText(row, value) {    	
    	return this.fullName(row).includes(value)
    }

    fullName(row) {
    	let firstNameSelector = row.querySelector(".first-name")
    	let lastNameSelector = row.querySelector(".last-name")

    	let firstName = firstNameSelector.textContent.toLowerCase()
    	let lastName = lastNameSelector.textContent.toLowerCase()

    	return firstName + " " + lastName
    }
}