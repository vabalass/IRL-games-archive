/* Project specific Javascript goes here. */

document.addEventListener("DOMContentLoaded", function() {
    const comments_container = document.getElementById("comments-container");
    const template = document.getElementById("comment-template");

    if (comments_container) {
        const url = comments_container.getAttribute("data-url");
        fetch(url)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.length != 0) {
                comments_container.innerHTML = "";
                data.forEach(comment => {
                    const clone = template.content.cloneNode(true);

                    clone.querySelector('.comment-author').textContent = comment.author_name;
                    clone.querySelector('.comment-text').textContent = comment.text;
                    clone.querySelector('.comment-rating').textContent = comment.rating || "-";
                    clone.querySelector('.comment-upvotes').textContent = comment.upvotes;
                    clone.querySelector('.comment-downvotes').textContent = comment.downvotes;
                    clone.querySelector('.comment-date').textContent = comment.date;
                    comments_container.appendChild(clone);
                });
            }
        })
        .catch(error => {
            console.error("Error loading comments: ", error);
            comments_container.innerHTML = "<p>Failed to load comments (.js).</p>";
        });
    }
});
