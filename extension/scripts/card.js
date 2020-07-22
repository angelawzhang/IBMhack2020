import data from "./data.js";

const buildCard = (company) => {
    const a = document.createElement('a');
    a.setAttribute("href", company.domain)
    a.setAttribute("target", "_blank")

    const button = document.createElement('button');
    button.setAttribute("class", "card");

    const header = document.createElement('header');
    header.setAttribute("class", "company");

    const logo = document.createElement("img");
    logo.setAttribute("class", "logo")
    logo.setAttribute("src", company.logo);

    const tags = document.createElement('p')
    tags.setAttribute("class", "tags")

    const photo1 = document.createElement("img");
    photo1.setAttribute("class", "photo1")
    photo1.setAttribute("src", company.photos[0]);
    
    const photo2 = document.createElement("img");
    photo2.setAttribute("class", "photo2")
    photo2.setAttribute("src", company.photos[1]);

    const photo3 = document.createElement("img");
    photo3.setAttribute("class", "photo3")
    photo3.setAttribute("src", company.photos[2]);

    const body = document.querySelector("body");

    const body_div = body.querySelector("div");

    body_div.append(a);
    a.append(button);
    button.append(header);
    button.append(logo);
    button.append(tags);
    button.append(photo1);
    button.append(photo2);
    button.append(photo3);
    header.innerHTML = company.name;
    tags.innerHTML = company.tags;
};

data.forEach(function(company) {
    buildCard(company);
    console.log("wtf");
})
// data.forEach(company => buildCard(company));