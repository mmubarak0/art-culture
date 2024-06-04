import loadFeed, { likePost } from './base.js';

// Load the feed when the page is loaded.
$(document).ready(function () {
    const artworks_url = `${window.location.origin.slice(0, -5)}:5004/api/v1/artworks`;
    loadFeed(artworks_url);
    $('#scrollUp').click(() => {
        // reload the feed
        loadFeed(artworks_url, true);
    })
});