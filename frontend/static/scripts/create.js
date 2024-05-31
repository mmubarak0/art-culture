$(function () {
    // Set the default AJAX headers.
    $.ajaxSetup({
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
    });

    const Data = {};
    const ImageData = [];
    $("#title").on("change", function (e) {
        let title = e.target.value;
        Data["title"] = title;
    });
    $("#description").on("change", function (e) {
        let description = e.target.value;
        Data["description"] = description;
    });
    $("#media").on("change", function (e) {
        images = e.target.files;
        for (i = 0; i < images.length; i++) {
            prefix = "/static/images/upload/" + ARTIST_ID + "/";
            let url = prefix + images[i].name;
            let type = "image";
            let name = images[i].name;
            ImageData.push({
                url: url,
                type: type,
                name: name,
            });
        }
    });
    $("#submit").on("click", function () {
        // create The Artwork
        Data["artist_id"] = ARTIST_ID;
        $.ajax({
            type: "POST",
            url: `${window.location.origin.slice(0, -5)}:5004/api/v1/artworks`,
            data: JSON.stringify(Data),
            success: function (response) {
                // create The Image
                for (i = 0; i < ImageData.length; i++) {
                    $.ajax({
                        type: "POST",
                        url: `${window.location.origin.slice(0, -5)}:5004/api/v1/artworks/${
                            response.id
                        }/medias`,
                        data: JSON.stringify(ImageData[i]),
                        success: function (response) {
                            // window.location.href = "/feed";
                        },
                        error: function (error) {
                            alert("Error Creating Image");
                        },
                    });
                }
            },
            error: function (error) {
                alert("Error Creating Artwork");
            },
        });
    });
});
