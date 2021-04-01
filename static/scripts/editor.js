document.getElementById("searchForm").addEventListener("submit", event => {
	event.preventDefault();

	// Clear out previous search results
	const searchResultsElem = document.getElementById("searchResults");
	searchResultsElem.innerHTML = "";

	const searchString = document.getElementById("searchQuery").value.trim();
	if (searchString) {
		// Fetch new results
		fetch(`/api/cards/search?q=${searchString}`).then(response => {
			if (response.ok) {
				response.json().then(data => {
					console.log(data);
					for (const card of data) {
						searchResultsElem.innerHTML += `<li><a target="_blank" href="/cards/${card.cardId}">${card.name}</a> <button class="card-add">+</button></li>`;
					}
				});
			} else {
				searchResultsElem.innerHTML = '<li class="text-danger">An error occured. Please try again later.</li>';
			}
		});
	} else {
		searchResultsElem.innerHTML ='<li class="text-danger">No input specified.</li>';
	}
});