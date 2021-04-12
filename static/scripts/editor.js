// Card search
$("#searchForm").on("submit", event => {
	event.preventDefault();

	// Clear out previous search results
	const searchResultsElem = document.getElementById("searchResults");
	searchResultsElem.innerHTML = "";

	const searchString = document.getElementById("searchQuery").value.trim();
	if (searchString) {
		// Fetch new results
		fetch(`/cards/search?q=${searchString}`).then(response => {
			if (response.ok) {
				response.json().then(data => {
					for (const card of data) {
						searchResultsElem.innerHTML += `<li id="search-${card.cardId}" class="cardAdd"><a target="_blank" href="/cards/${card.cardId}">${card.name}</a> <button class="btn btn-primary btn-sm card-add font-weight-bold">+</button></li>`;
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

// Add card to the deck list
$("#searchResults").on("click", ".card-add", function(event) {
	fetch(`?cardId=${event.target.parentElement.id.substring(7)}&op=add`, {method: "PATCH"}).then(response => {
		if (response.ok) {
			response.json().then(data => {
				const cardElem = $("#deck-"+data.card.id);
				if (cardElem.length) {
					cardElem.children("span").text(`x ${data.card.count}`);
				} else {
					$("#currentDeck").append(`<li id="deck-${data.card.id}"><a target="_blank" href="/cards/${data.card.id}">${data.card.name}</a> <span>x 1</span> <button class="btn btn-danger btn-sm card-remove font-weight-bold">-</button></li>`);
				}
			});
		}
	});
});

// Remove card from the deck list
$("#currentDeck").on("click", ".card-remove", function(event) {
	fetch(`?cardId=${event.target.parentElement.id.substring(5)}&op=rem`, {method: "PATCH"}).then(response => {
		if (response.ok) {
			response.json().then(data => {
				const cardElem = $("#deck-"+data.card.id);
				if (data.card.count === 0) {
					cardElem.remove();
				} else {
					cardElem.children("span").text(`x ${data.card.count}`);
				}
			});
		}
	});
});