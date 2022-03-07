var favChocolates = [];

var addButton = document.querySelector("#add-button");
console.log("button query: ", addButton);
addButton.onclick = function () {
    //call function to create new chocolate on server API
    //TODO: capture text from input field

    //Step 1:query the input field
    var chocolateNameInput = document.querySelector("#chocolateName");
    //step 2: capture the text
    var chocolateName = chocolateNameInput.value;

    var chocolateFlavorInput = document.querySelector("#chocolateFlavor");
    var chocolateFlavor = chocolateFlavorInput.value;

    var chocolatePriceInput = document.querySelector("#chocolatePrice");
    var chocolatePrice = chocolatePriceInput.value;

    var chocolateSizeInput = document.querySelector("#chocolateSize");
    var chocolateSize = chocolateSizeInput.value;

    var chocolateDescriptionInput = document.querySelector("#chocolateDescription");
    var chocolateDescription = chocolateDescriptionInput.value;

    var chocolateRatingInput = document.querySelector("#chocolateRating");
    var chocolateRating = chocolateRatingInput.value;

    //step 3: call the create chocolate function, pass in text
    createChocolate(chocolateName, chocolateFlavor, chocolatePrice, chocolateSize, chocolateDescription, chocolateRating);
};

//create a new chocolate on a server API
function createChocolate(chocolateName, chocolateFlavor, chocolatePrice, chocolateSize, chocolateDescription, chocolateRating) {
    var data = "name=" + encodeURIComponent(chocolateName);
    data += '&flavor=' + encodeURIComponent(chocolateFlavor);
    data += '&price=' + encodeURIComponent(chocolatePrice);
    data += '&size=' + encodeURIComponent(chocolateSize);
    data += '&description=' + encodeURIComponent(chocolateDescription);
    data += '&rating=' + encodeURIComponent(chocolateRating);

    console.log('The is the data is going to send to the server: ', data);

    fetch("http://localhost:8080/chocolates", {    //dictionary
        method: 'POST',
        body: data,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        //here, the server has responded(due to AJAX being asynchronous-waiting for the response)
        //so, reload chocolates from their server
        loadChocolates();
        //slight bug: list of chocolates is duplicated
    });
    //here server has not responded
};

function deleteChocolateFromServer(chocolateID) {
    fetch("http://localhost:8080/chocolates/" + chocolateId, { method: "DELETE" }).then(function (response) {
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
            favChocolates = data //this is the list
            console.log("Chocolates from the server:", favChocolates);

            //step 1:query the PARENT element
            var chocolateList = document.querySelector("#chocolate-list");
            console.log("chocolate list query: ", chocolateList);

            //empty the list of chocolates
            chocolateList.innerHTML = "";

            //loop over data immediately
            //for chocolates in faveChocolates, append each to the DOM list
            favChocolates.forEach(function (chocolate) {

                //see DOM insert/append code steps

                //step 2: create the child element

                var newListItem = document.createElement("li");

                var nameDiv = document.createElement("div");
                nameDiv.innerhtml = chocolate.name;
                nameDiv.classList.add("chocolate-name");
                newListItem.appendChild(nameDiv);

                var flavorDiv = document.createElement("div");
                flavorDiv.innerhtml = chocolate.flavor;
                flavorDiv.classList.add("chocolate-flavor");
                newListItem.appendChild(flavorDiv);

                var priceDiv = document.createElement("div");
                priceDiv.innerhtml = chocolate.price;
                priceDiv.classList.add("chocolate-price");
                newListItem.appendChild(priceDiv);

                var sizeDiv = document.createElement("div");
                sizeDiv.innerhtml = chocolate.size;
                sizeDiv.classList.add("chocolate-size");
                newListItem.appendChild(sizeDiv);

                var descriptionDiv = document.createElement("div");
                descriptionDiv.innerhtml = chocolate.description;
                descriptionDiv.classList.add("chocolate-description");
                newListItem.appendChild(descriptionDiv);

                var ratingDiv = document.createElement("div");
                ratingDiv.innerhtml = chocolate.rating;
                ratingDiv.classList.add("chocolate-rating");
                newListItem.appendChild(ratingDiv);

                var deleteButton = document.createElement("button");
                deleteButton.innerhtml = "Delete";
                deleteButton.onclick = function () {
                    console.log("delete button clicked", chocolate.id);
                    if (confirm("Are you sure?")) {
                        deleteChocolateFromServer(chocolate.id);
                    }
                };
                newListItem.appendChild(deleteButton);


                var editButton = document.createElement("button");
                editButton.innerhtml = "Edit";
                editButton.onclick = function () {
                    console.log("edit button clicked", chocolate.id);
                    if (confirm("Are you sure?")) {
                        //displayEditForm(chocolate.id, chocolate.name ...addButton.);
                    }

                };
                newListItem.appendChild(editButton);

                //step 3: append child to parent
                chocolateList.appendChild(newListItem);
            });
        });
    });
}

//immediately load chocolates
loadChocolates();