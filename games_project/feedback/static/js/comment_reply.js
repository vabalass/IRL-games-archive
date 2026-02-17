document.getElementById("comment-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const comments_container = document.getElementById("comments-container")

    const text = formData.get("comment-text");
    const game_pk = comments_container.dataset.gamePk;

    console.log("Comment text:", text);
    console.log("Game pk:", game_pk);


    const csrftoken = formData.get("csrfmiddlewaretoken");
    console.log("CSRF Token:", csrftoken);

    if (!csrftoken) {
        console.error("CSRF token not found!");
    }

    fetch(`/games/${game_pk}/reply`, {
        method: "POST",
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            text: text
        })
    })
    .then(response => {
        console.log("Response status:", response.status);
        return response.text();
    })
    .then(text => {
        console.log("Response body:", text);
        const data = JSON.parse(text);
        console.log("Parsed:", data);
    })
    .catch(error => {
        console.log("failed!", error)
    });

});
