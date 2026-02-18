document.addEventListener("DOMContentLoaded", function() {
    loadComments()
});

function loadComments() {
    const commentsContainer = document.getElementById("comments-container");
    const commentTemplate = document.getElementById("comment-template");

    const url = commentsContainer.getAttribute("data-url");

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error (.js): ${response.status}`);
            return response.json();
        })
        .then(data => {
            commentsContainer.innerHTML = "";

            // Render each top-level comment with its replies
            data.forEach(comment => {
                const commentElement = createCommentElement(comment, false);
                commentsContainer.appendChild(commentElement);

                if (comment.replies.length > 0) {
                    // Find the comment we just added in the DOM
                    const commentCard = commentsContainer.querySelector(`[data-comment-id="${comment.id}"]`);

                    if (commentCard) {
                        const repliesContainer = commentCard.querySelector('.replies');

                        if (repliesContainer) {
                            comment.replies.forEach(reply => {
                                const replyElement = createCommentElement(reply, true);
                                repliesContainer.appendChild(replyElement);
                            });
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error("Error loading comments:", error);
            commentsContainer.innerHTML = '<div class="alert alert-danger">Failed to load comments.</div>';
        });

    function createCommentElement(comment, isReply) {
        const clone = commentTemplate.content.cloneNode(true);

        const card = clone.querySelector('.card');
        if (card) card.dataset.commentId = comment.id;

        clone.querySelector('.comment-author').textContent = comment.author_name;
        clone.querySelector('.comment-text').textContent = comment.text;
        clone.querySelector('.comment-upvotes').textContent = comment.upvotes;
        clone.querySelector('.comment-downvotes').textContent = comment.downvotes;
        clone.querySelector('.comment-date').textContent = comment.time_ago;
        clone.querySelector('.comment-rating').textContent = comment.rating


        const replyBtn = clone.querySelector('.reply-btn');
        const ratingContainer = clone.querySelector('.comment-rating').closest('small');
        if (replyBtn) {
            replyBtn.dataset.commentId = comment.id;
            replyBtn.dataset.commentAuthor = comment.author_name;

            if (isReply) {
                replyBtn.classList.add('d-none');
                ratingContainer.classList.add('d-none');
            }
        }

        // Remove replies container from reply comments
        if (isReply) {
            const repliesContainer = clone.querySelector('.replies');
            if (repliesContainer) {
                repliesContainer.remove();
            }
        }

        return clone;
    }
}
