 // Function to perform user search
 function searchUsers() {
    const searchInput = document.getElementById("user-search").value;
    const searchResults = document.querySelector(".search-results");

    if (searchInput.trim() === "") {
        // If the search input is empty, hide the search results
        searchResults.style.display = "none";
        return; // Exit the function
    }

    // Make an AJAX request to the search_users view
    fetch(`search_users/?q=${searchInput}`)
        .then(response => response.json())
        .then(data => {
            searchResults.style.display = "block"; // Show the search results container
            searchResults.innerHTML = ""; // Clear previous search results

            // Display the search results
            data.users.forEach(user => {
                const userElement = document.createElement("div");
                userElement.classList.add("user-result");
                userElement.innerHTML = `<strong>${user.username}</strong> - ${user.email}`;
                userElement.addEventListener("click", () => {
                    // Handle adding the user as a friend here
                    addUserAsFriend(user.id);
                });
                searchResults.appendChild(userElement);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Add event listeners for search input and button
const searchInput = document.getElementById("user-search");
searchInput.addEventListener("input", searchUsers);

// Hide the search results initially
document.addEventListener("DOMContentLoaded", () => {
    const searchResults = document.querySelector(".search-results");
    searchResults.style.display = "none";
});




function addUserAsFriend(profileId) {
    // Make an AJAX request to the add_friend view
    fetch(`add_friend/${profileId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Optionally, you can update the UI to indicate that the user has been added as a friend
                console.log(`User with profile ID ${profileId} added as a friend.`);
                location.reload();
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


