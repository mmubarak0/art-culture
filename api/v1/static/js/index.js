const articles_container = document.querySelector("#articles");
const url = "http://172.21.137.143:5005";

const create_article = (
  id,
  title,
  text,
  likes = 0,
  comments = "",
  media = "",
  views = 0
) => {
  let article = `
    <div class="row mb-2 mt-2 ps-4 pe-4 artwork" id=${id}>
		<div class="col p-5 bg-dark bg-gradient">
			<h1 class="text-white-50 border-bottom border-4 w-50 pb-2">
				${title}
			</h1>
      <div class="row">
            ${media}
      </div>
			<p class="text-white">
                ${text}
			</p>
			<p class="btn btn-info btn-rounded">${likes} like</p>
			<p class="btn btn-info btn-rounded">comments</p>
			<p class="btn btn-info btn-rounded">${views} views</p>
		</div>
    <div class="row m-3" style="display: none;">
      <h1>comments</h1>
      <ul>
        ${comments}
      </ul>
    </div>
	</div>
    `;
  return article;
};

const concat = (...args) => {
  return args.join("/");
};

// get artworks from the api
async function get_artworks() {
  const api = "api/v1/artworks";
  try {
    let res = await fetch(concat(url, api));
    return await res.json();
  } catch (error) {
    console.log(error);
  }
}

async function get_artwork(artwork_id) {
  const api = `api/v1/artworks/${artwork_id}`;
  try {
    let res = await fetch(concat(url, api));
    return await res.json();
  } catch (error) {
    console.log(error);
  }
}

const create_comments = (c) => {
  let comments = ``;
  c.comments.forEach((comment) => {
    comments += `<li><a href="/api/v1/artists/${comment.by}">${comment.user_name}</a><p>${comment.content}</p></li>`;
  });
  if (comments.length < 1) {
    comments += `<li><h3>There is no comments here yet!</h3></li>`;
  }
  return comments;
};
const create_media = (m) => {
  let medias = ``;
  m.media.forEach((media) => {
    if (media.type == "image") {
      medias += `<div class="col col-4 border border-1"><img src="${media.url}" alt="${media.name}" width="250" height="250"></div>`;
    }
    // else if another type like videos, sounds, etc....
  });
  return medias;
};
async function render_artworks() {
  let s = await get_artworks();
  if ("error" in s) {
    console.log(s["error"]);
  } else {
    for (const key in s) {
      let comments = create_comments(s[key]);
      let media = create_media(s[key]);
      articles_container.innerHTML += create_article(
        s[key].id,
        s[key].title,
        s[key].description,
        s[key].likes,
        comments,
        media,
        s[key].views
      );
    }
  }
}
async function toggle_comments() {
  let artworks = document.querySelectorAll(".artwork");
  for (let i = 0; i < artworks.length; i++) {
    const element_src = artworks[i].firstElementChild.children[4];
    element_src.addEventListener("click", (e) => {
      const comment_section = artworks[i].children[1];
      if (comment_section.style.display == "none") {
        comment_section.style.display = "block";
      } else {
        comment_section.style.display = "none";
      }
    });
  }
}
async function toggle_likes() {
  let artworks = document.querySelectorAll(".artwork");
  for (let i = 0; i < artworks.length; i++) {
    const element_id = artworks[i].id;
    const api = concat(url, "api/v1/artworks", element_id, "like");
    const element_src = artworks[i].firstElementChild.children[3];
    element_src.addEventListener("click", async (e) => {
      let res = await fetch(api).then((result) => result.json());
      if (!("error" in res)) {
        element_src.innerText = `${res.likes} likes`;
      }
    });
  }
}
async function output() {
  await render_artworks();
  await toggle_comments();
  await toggle_likes();
}
output();
