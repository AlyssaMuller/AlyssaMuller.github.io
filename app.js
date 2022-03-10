var addButton = document.querySelector("#add-button");
var adding = true;
var chocolateID = null;
var sanitation = false;

function getAndFormatData() {
    //Step1: Query las ladies
    var chocolateNameInput = document.querySelector("#chocolateName");
    var chocolateFlavorInput = document.querySelector("#chocolateFlavor");
    var chocolatePriceInput = document.querySelector("#chocolatePrice");
    var chocolateSizeInput = document.querySelector("#chocolateSize");
    var chocolateDescriptionInput = document.querySelector("#chocolateDescription");
    var chocolateRatingInput = document.querySelector("#chocolateRating");

    //step 2: capture text
    var chocolateName = chocolateNameInput.value;
    var chocolateFlavor = chocolateFlavorInput.value;
    var chocolatePrice = chocolatePriceInput.value;
    var chocolateSize = chocolateSizeInput.value;
    var chocolateDescription = chocolateDescriptionInput.value;
    var chocolateRating = chocolateRatingInput.value;
    
    //return formatted data
    var data = "name=" + encodeURIComponent(chocolateName);
    data += '&flavor=' + encodeURIComponent(chocolateFlavor);
    data += '&price=' + encodeURIComponent(chocolatePrice);
    data += '&size=' + encodeURIComponent(chocolateSize);
    data += '&description=' + encodeURIComponent(chocolateDescription);
    data += '&rating=' + encodeURIComponent(chocolateRating);

    return data;
}

addButton.onclick = function () {
    var chocolateData = getAndFormatData();

    if (adding == true)
        createChocolate(chocolateData);
    else {
        updateChocolate(chocolateData);
        addButton.innerHTML = "Add Chocolate";
    }
};

//create a new chocolate on a server API
function createChocolate(chocolateData) {
    console.log('Sent data for update: ', chocolateData);

    fetch("http://localhost:8080/chocolates", { //dictionary
        method: 'POST',
        body: chocolateData,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        //here, the server has responded(async AJAX)
        //so, reload updated chocolates list
        loadChocolates();
    });
};

//create a new chocolate on a server API
function updateChocolate(chocolateData) {
    console.log('This is the data being sent to the server (for PUT): ', chocolateData);

    adding = true;

    fetch("http://localhost:8080/chocolates/" + chocolateID, {
        method: 'PUT',
        body: chocolateData,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        loadChocolates();
    });
};

function deleteChocolateFromServer(chocolateID) {
    fetch("http://localhost:8080/chocolates/" + chocolateID, { method: "DELETE" }).then(function (response) {
        console.log("js delete response function started yay");
        if (response.status == 200) {
            console.log("chocolate successfully deleted");
            loadChocolates();
        }
    });
}

// load faveChocolates from the server as JSON data
function loadChocolates() {
    fetch("http://localhost:8080/chocolates").then(function (response) {
        // The server has responded.
        response.json().then(function (data) {
            serverChocolates = data //this is the list
            console.log("Chocolates from the server:", serverChocolates);

            //step 1:query the PARENT element
            var chocolateList = document.querySelector("#chocolate-list");
            console.log("chocolate list query: ", chocolateList);

            //empty the list of chocolates
            chocolateList.innerHTML = "";

            //loop over data immediately
            //for chocolates in faveChocolates, append each to the DOM list
            serverChocolates.forEach(function (chocolate) {
                //see DOM insert/append code steps
                //step 2: create the child element

                var newListItem = document.createElement("div");
                newListItem.classList.add("outputDivs");

                var nameDiv = document.createElement("div");
                // Combining the name and flavor into one
                nameDiv.innerHTML = chocolate.name + " " + chocolate.flavor;
                nameDiv.classList.add("chocolate-name");
                newListItem.appendChild(nameDiv);

                /* var flavorDiv = document.createElement("div"); flavorDiv.innerHTML = chocolate.flavor; flavorDiv.classList.add("chocolate-flavor"); newListItem.appendChild(flavorDiv); */

                var priceDiv = document.createElement("div");
                priceDiv.innerHTML = "ONLY " + chocolate.price + "!";
                priceDiv.classList.add("chocolate-price");
                newListItem.appendChild(priceDiv);

                var sizeDiv = document.createElement("div");
                sizeDiv.innerHTML = "Size: " + chocolate.size;
                sizeDiv.classList.add("chocolate-size");
                newListItem.appendChild(sizeDiv);

                var descriptionDiv = document.createElement("div");
                descriptionDiv.innerHTML = chocolate.description;
                descriptionDiv.classList.add("chocolate-description");
                newListItem.appendChild(descriptionDiv);

                var ratingDiv = document.createElement("div");
                ratingDiv.innerHTML = "";

                if (chocolate.rating == 5)
                    ratingDiv.innerHTML += "⭐⭐⭐⭐⭐";
                else {
                    for (var i = 0; i < chocolate.rating; i++)
                        ratingDiv.innerHTML += "⭐";

                    for (var j = chocolate.rating; j < 5; j++)
                        ratingDiv.innerHTML += "★";
                }

                ratingDiv.classList.add("chocolate-rating");
                newListItem.appendChild(ratingDiv);

                var editButton = document.createElement("button");
                editButton.innerHTML = "Edit";
                editButton.classList.add("editButton");
                editButton.onclick = function () {
                    var chocolateNameInput = document.querySelector("#chocolateName");
                    var chocolateFlavorInput = document.querySelector("#chocolateFlavor");
                    var chocolatePriceInput = document.querySelector("#chocolatePrice");
                    var chocolateSizeInput = document.querySelector("#chocolateSize");
                    var chocolateDescriptionInput = document.querySelector("#chocolateDescription");
                    var chocolateRatingInput = document.querySelector("#chocolateRating");

                    chocolateNameInput.value = chocolate.name;
                    chocolateFlavorInput.value = chocolate.flavor;
                    chocolatePriceInput.value = chocolate.price;
                    chocolateSizeInput.value = chocolate.size;
                    chocolateDescriptionInput.value = chocolate.description;
                    chocolateRatingInput.value = chocolate.rating;

                    adding = false;
                    chocolateID = chocolate.id;
                    addButton.innerHTML = "Save Chocolate";
                };

                newListItem.appendChild(editButton);

                var deleteButton = document.createElement("button");
                deleteButton.innerHTML = "Delete";
                deleteButton.classList.add("deleteButton");
                deleteButton.onclick = function () {
                    console.log("delete button clicked, id: ", chocolate.id);
                    if (confirm("Are you sure?")) {
                        deleteChocolateFromServer(chocolate.id);
                    }
                };
                newListItem.appendChild(deleteButton);

                // step 3: append child to parent
                chocolateList.appendChild(newListItem);
            });
        });
    });
}

function displayEditForm(chocolateID, chocolateData) {
    console.log("edit button clicked", chocolateID, chocolateData, ratingDiv);
}

//immediately load chocolates
loadChocolates();