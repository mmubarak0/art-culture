import loadFeed from './base.js';

// Load the feed when the page is loaded.
$(document).ready(function () {
    const artworks_url = `${window.location.origin.slice(0, -5)}:5004/api/v1/artists/${ARTIST_ID}/artworks/`;
    loadFeed(artworks_url);
    $('#scrollUp').click(() => {
        // reload the feed
        loadFeed(artworks_url, true);
    })
});