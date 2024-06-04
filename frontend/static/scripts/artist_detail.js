import loadFeed from "./base.js";

// Load the feed when the page is loaded.
$(document).ready(function () {
    const artworks_url = `http://${window.location.hostname}:5004/api/v1/artists/${DETAIL_ID}/artworks/`;
    loadFeed(artworks_url);
    $("#scrollUp").click(() => {
        // reload the feed
        loadFeed(artworks_url, true);
    });
    $.ajaxSetup({
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
    });
    // Follow the artist
    $("#follow").click(() => {
        // follow the artist
        $.post(
            `http://${window.location.hostname}:5004/api/v1/artists/${DETAIL_ID}/follow`,
            JSON.stringify({
                artist_id: ARTIST_ID,
            }),
            (response) => {
                // if (response["status"] === "success") {
                    if ($("#follow").text() == "Follow") {
                        $("#follow").text("Unfollow");
                        $("#followers").text(parseInt($("#followers").text()) + 1);
                    } else {
                        $("#follow").text("Follow");
                        $("#followers").text(parseInt($("#followers").text()) - 1);
                    }
                // }
            }
        );
    });
});
