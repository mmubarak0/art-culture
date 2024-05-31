// Author: ki2kid [Github](https://github.com/mmubarak0) (Twitter)[https://x.com/ki2kid]

// This script is responsible for controlling the feed page.
// It is responsible for loading the feed.
// It also handles the like and comment functionality.

// TODO:
// 1- Implement pagination for the feed.
// 2- Implement category classification for the posts.
// 3- Implement the ability to filter the feed by category.
// 4- Show the details of a post artist creator when the avatar on name is clicked.
// 5- Implement the menu that appears when a three dots is clicked.
// 6- Add the ability to follow an artist.
// 7- Add the ability to delete a post.
// 8- Add the ability to edit a post.
// 9- Add the ability to delete a comment.
// 10- Add the ability to edit a comment.
// 11- Add the ability to report a post.
// 12- Send the post in private message.

// FIX: Line 132 > Using the e to access the like button cause a bug.
// Description:
//      when someone clicks on the action (ex. like) button and moves fast to an empty area.
//      This make the wrong next element to be updated inplace of the desired one.
// Recomendation:
//      reduce mouse movement when clicking on the action button.

// Set the default AJAX headers.
$.ajaxSetup({
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
    },
});

// static data dictionary
Icons = {
    likes: "like-svgrepo-com.svg",
    comments: "comment-1-svgrepo-com.svg",
    share: "share-2-svgrepo-com.svg",
    more: "more-svgrepo-com.svg",
};

// Load the feed when the page is loaded.
$(document).ready(function () {
    loadFeed();
});

// Load the feed.
function loadFeed() {
    var feedContainer = $("#main-content");

    $.ajax({
        url: `${window.location.origin.slice(0, -5)}:5004/api/v1/artworks`,
        method: "GET",
        success: async function (data) {
            data = data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            for (i = 0; i < data.length; i++) {
                let artistData = await getArtistData(data[i].artist_id);
                let article = await createArticle(data[i], artistData);
                feedContainer.append(article);
            }
        },
        error: function () {
            feedContainer.html(
                '<div class="alert alert-info">An error occurred while loading the feed.</div>'
            );
        },
    });
}

// Get artist data.
async function getArtistData(artistId) {
    return new Promise(function (resolve, reject) {
        $.get(
            `${window.location.origin.slice(0, -5)}:5004/api/v1/artists/${artistId}`,
            function (artistData) {
                resolve(artistData);
            }
        );
    });
}

// Create an article element for each post.
async function createArticle(post, artistData) {
    let article = $("<article></article>").attr("id", post.id);
    let header = await createPostHeader(artistData);
    let content = await createPostContent(post.id);
    let actions = await createPostActions(post);
    article.append(header);
    article.append(content);
    article.append(actions);
    article.append(
        $("<div></div>").addClass("more").addClass("hidden").attr("id", `options-${post.id}`)
    );
    article.append($("<div></div>").addClass("hidden").attr("id", `comment-${post.id}`));
    return article;
}

// Create post content section
async function createPostContent(postId) {
    let post = await updatePost(postId);
    let content = $("<div></div>").addClass("content");
    let postText = $("<p></p>").text(post.description);
    let images = await createPostImages(post);
    content.append(postText);
    content.append(images);
    return content;
}

// Create post images.
async function createPostImages(post) {
    // let imageExtenstions = ["jpg", "jpeg", "png", "gif", "svg"];
    let imagesContainer = $("<div></div>");
    let images = await getImages(post);
    images.forEach(function (image) {
        let imageElement = $("<img>").attr("src", image.url).attr("alt", "Post Image");
        imageElement.click(function () {
            if (document.fullscreenElement) {
                document.exitFullscreen();
            } else {
                this.requestFullscreen({ navigationUI: "show" });
            }
        });
        switch (images.length) {
            case 1:
                imageElement.addClass("i1");
                imagesContainer.append(imageElement);
                break;
            case 2:
                imageElement.addClass("i2");
                imagesContainer.append(imageElement);
                break;
            case 3:
                imageElement.addClass("i3");
                imagesContainer.append(imageElement);
                break;
            case 4:
                imageElement.addClass("i4");
                imagesContainer.append(imageElement);
                break;
            default:
                break;
        }
    });
    return imagesContainer;
}

async function getImages(post) {
    return new Promise(async function (resolve, reject) {
        let result = [];
        for (let i = 0; i < post.media.length; i++) {
            let image = await getPostImage(post.media[i]);
            result.push(image);
        }
        resolve(result);
    });
}

// Get post images.
async function getPostImage(mediaId) {
    return new Promise(function (resolve, reject) {
        $.get(
            `${window.location.origin.slice(0, -5)}:5004/api/v1/medias/${mediaId}`,
            function (image) {
                resolve(image);
            }
        );
    });
}

// Create the post header.
function createPostHeader(artistData) {
    let postHeader = $("<div></div>").addClass("post-header");
    postHeader.append(
        $("<img>")
            .addClass("post-profile-pic")
            // Later to be repalced with user actuall image.
            .attr("src", "static/images/post-profile.jpg")
            .attr("alt", "Post Profile Picture")
    );
    postHeader.append(
        $("<h3></h3>")
            .addClass("username")
            .text(artistData.first_name + " " + artistData.last_name)
    );
    return postHeader;
}

// Create the post actions.
function createPostActions(post) {
    let postActions = $("<div></div>").addClass("post-actions");
    postActions.append(createActionLink("likes", "Like", "likePost", post, true));
    postActions.append(createActionLink("comments", "Comment", "showComments", post, true));
    postActions.append(createActionLink("share", "Share"));
    postActions.append(createActionLink("more", "More", "moreOptions", post));
    return postActions;
}

// Create an action link.
function createActionLink(className, altText, clickHandler, data, counter) {
    let link = $("<a></a>").attr("href", "#").addClass(className);
    link.append(
        $("<img>").attr("src", `static/images/icons/${Icons[className]}`).attr("alt", altText)
    );
    if (counter) {
        link.append($("<span></span>").text(data[className].length));
    }
    if (clickHandler) {
        link.on("click", function (e) {
            e.preventDefault();
            window[clickHandler](data, e);
        });
    }
    return link;
}

// Like a post.
function likePost(post, e) {
    postId = post.id;
    $.post(
        `${window.location.origin.slice(0, -5)}:5004/api/v1/artworks/${postId}/like`,
        JSON.stringify({
            artist_id: ARTIST_ID,
        }),
        function (data) {
            updateCount(e, data.likes.length);
        }
    );
}

// Show comments for a post.
async function showComments(post, e, update = false) {
    post = await updatePost(post.id);
    let postComment = $(`#comment-${post.id}`).addClass(update ? "hidden" : "");
    let comments = post.comments;
    updateCount(e, comments.length);
    if (postComment.hasClass("hidden")) {
        hideAllComments();
        postComment.html("").append($("<h4></h4>").text("Comments"));
        postComment.removeClass("hidden");

        for (let i = 0; i < comments.length; i++) {
            let commentId = comments[i];
            let commentData = await getCommentData(commentId);
            let artistData = await getArtistData(commentData.artist_id);
            postComment.append(createComment(artistData, commentData, e));
        }

        let newCommentForm = createNewCommentForm(post.id, e);
        postComment.append(newCommentForm);
    } else {
        postComment.addClass("hidden");
    }
}

// Update post details.
async function updatePost(postId) {
    return new Promise(function (resolve, reject) {
        $.get(
            `${window.location.origin.slice(0, -5)}:5004/api/v1/artworks/${postId}`,
            function (data) {
                resolve(data);
            }
        );
    });
}

// Hide all comments.
function hideAllComments() {
    let allPosts = $("#main-content").children();
    allPosts.each(function (index, element) {
        let commentSection = element.children[element.children.length - 1];
        if (!commentSection.classList.contains("hidden")) {
            commentSection.classList.add("hidden");
        }
    });
}

// Get comment data.
async function getCommentData(commentId) {
    return new Promise(function (resolve, reject) {
        $.get(
            `${window.location.origin.slice(0, -5)}:5004/api/v1/comments/${commentId}`,
            function (commentData) {
                resolve(commentData);
            }
        );
    });
}

// Create a comment element.
function createComment(artistData, commentData, cbutton) {
    let comment = $("<div></div>").addClass("comment");
    comment.append(
        $("<img>")
            .addClass("comment-profile-pic")
            // Later to be repalced with user actuall image.
            .attr("src", "/static/images/post-profile.jpg")
            .attr("alt", "Comment Profile Picture")
    );
    comment.append(
        $("<h3></h3>")
            .addClass("comment-username")
            .text(artistData.first_name + " " + artistData.last_name)
    );
    comment.append($("<p></p>").text(commentData.content));
    if (artistData.id === ARTIST_ID) {
        comment.append(
            $("<button></button>")
                .text("Del")
                .addClass("button button-danger")
                .attr("id", commentData.id)
                .on("click", (e) => {
                    deleteComment(e, cbutton);
                })
        );
    }
    return comment;
}

// Create a form for adding a new comment.
function createNewCommentForm(postId, cbutton) {
    let form = $("<form></form>");
    form.append(
        $("<input>")
            .attr("type", "text")
            .attr("name", "new_comment")
            .attr("placeholder", "New comment...")
    );
    form.append(
        $("<input>")
            .attr("type", "text")
            .attr("name", "artist_id")
            .attr("value", ARTIST_ID)
            .addClass("hidden")
    );
    form.append(
        $("<input>")
            .attr("type", "submit")
            .attr("name", "submit")
            .attr("value", "Send")
            .on("click", function (e) {
                e.preventDefault();
                sendNewComment(postId, e, cbutton);
            })
    );
    return $("<div></div>").addClass("create-comment").append(form);
}

// Send a new comment.
async function sendNewComment(postId, e, cbutton) {
    let url = `${window.location.origin.slice(0, -5)}:5004/api/v1/artworks/${postId}/comments/`;
    let data = {
        artist_id: ARTIST_ID,
        content: e.target.parentElement[0].value,
    };
    await $.post(url, JSON.stringify(data));
    let postUrl = `${window.location.origin.slice(0, -5)}:5004/api/v1/artworks/${postId}`;
    await $.get(postUrl, function (post) {
        showComments(post, cbutton, true);
        updateCount(cbutton, post.comments.length);
    });
}

// Update the like or comment count.
function updateCount(e, count) {
    let counter = $(e.target).next();
    counter.text(count);
}

// Delete a comment.
function deleteComment(e, cbutton) {
    comment_body = e.target.parentElement;
    $.ajax({
        url: `${window.location.origin.slice(0, -5)}:5004/api/v1/comments/${e.target.id}`,
        method: "DELETE",
        success: function () {
            comment_body.remove();
            let y = $(cbutton.target).next();
            let x = +y.text() - 1;
            updateCount(cbutton, x < 0 ? 0 : x);
        },
        error: function (e) {
            console.log("error", e);
        },
    });
}

// Show more options for a post.
function moreOptions(post, e) {
    // <div class="dropdown-profile">
    //     <img class="dropbtn-profile" src="static/images/profile.jpg" alt="Profile Picture">
    //     <div class="dropdown-content-profile">
    //         <a href="/logout">Logout</a>
    //         <a href="profile_settings">Profile Settings</a>
    //         <a href="profile">Profile Details</a>
    //     </div>
    // </div>
    let optionsContainer = $(`#options-${post.id}`);
    optionsContainer.html("");
    if (optionsContainer.hasClass("hidden")) {
        let options = $("<div></div>").addClass("more-content");
        let deleteOption = $("<a></a>")
            .attr("href", "#")
            .text("Delete")
            .on("click", function (e) {
                e.preventDefault();
                deletePost(post, e);
            });
        let editOption = $("<a></a>")
            .attr("href", "#")
            .text("Edit")
            .on("click", function (e) {
                e.preventDefault();
                // editPost(post, e);
            });
        options.append(deleteOption);
        options.append(editOption);
        optionsContainer.append(options);
        optionsContainer.removeClass("hidden");
    } else {
        optionsContainer.addClass("hidden");
    }
}

function deletePost(post, e) {
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: `${window.location.origin.slice(0, -5)}:5004/api/v1/artworks/${post.id}`,
                method: "DELETE",
                success: function () {
                    targetArtwork = document.getElementById(post.id);
                    targetArtwork.remove();
                },
                error: function (e) {
                    console.log("error", e);
                },
            });
            Swal.fire({
                title: "Deleted!",
                text: "Your artwork has been deleted.",
                icon: "success",
            });
        }
    });
}
