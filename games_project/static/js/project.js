/* Project specific Javascript goes here. */

document.addEventListener("DOMContentLoaded", function() {
    const comments_container = document.getElementById("comments-container");

    if (comments_container) {
        const url = comments_container.getAttribute("data-url");

        fetch(url, {
            method: "GET",
            header: {
                // tells django this is an AJAX request
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => {
            if (!response.ok) throw new Error("Response is not ok");
            return response.text();
        })
        .then(html => {
            comments_container.innerHTML = html
        })
        .catch(error => {
            console.error("Error loading comments: ", error);
            comments_container.innerHTML = "<p>Failed to load comments.</p>";
        });
    }
});
