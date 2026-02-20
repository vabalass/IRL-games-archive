document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("comment-form");
    const parentInput = document.getElementById("parent-id");
    const formTitle = document.getElementById("form-title");
    const cancelBtn = document.getElementById("cancel-reply");
    const commentsContainer = document.getElementById("comments-container");
    const formErrors = document.getElementById("form-errors");

    document.addEventListener('click', function(e) {
        if (e.target.closest('.reply-btn')) {
            const btn = e.target.closest('.reply-btn');
            const commentId = btn.dataset.commentId;
            const commentAuthor = btn.dataset.commentAuthor;

            if (parentInput) parentInput.value = commentId;
            if (formTitle) formTitle.textContent = `Replying to @${commentAuthor}`;
            if (cancelBtn) cancelBtn.classList.remove('d-none');

            form.scrollIntoView({ behavior: 'smooth', block: 'center' });

            const textarea = document.getElementById('comment-text');
            if (textarea) textarea.focus();
        }
    });

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            resetForm();
        });
    }

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const formData = new FormData(event.target);
        const text = formData.get("text");
        const parentId = parentInput ? parentInput.value : null;
        const gamePk = commentsContainer ? commentsContainer.dataset.gamePk : null;
        const csrftoken = formData.get("csrfmiddlewaretoken");

        fetch(`/games/${gamePk}/reply/`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                text: text,
                parent: parentId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resetForm();
                loadComments();
            } else {
                displayErrors(data.errors);
            }
        })
        .catch(error => {
            alert("Failed to post comment: " + error.message);
        });
    });

    function resetForm() {
        form.reset();
        if (parentInput) parentInput.value = '';
        if (formTitle) formTitle.textContent = 'Add a Comment';
        if (cancelBtn) cancelBtn.classList.add('d-none');

        const formErrors = document.getElementById('form-errors');
        if (formErrors) formErrors.classList.add('d-none');
    }

    function displayErrors(errors) {
        if (!formErrors) {
            alert('Error: ' + JSON.stringify(errors));
            return;
        }

        let errorHtml = '';

        for (let field in errors) {
            const fieldErrors = errors[field];

            if (Array.isArray(fieldErrors)) {
                errorHtml += fieldErrors.join('<br>') + '<br>';
            } else {
                errorHtml += fieldErrors + '<br>';
            }
        }

        formErrors.innerHTML = errorHtml;
        formErrors.classList.remove('d-none');

        formErrors.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
