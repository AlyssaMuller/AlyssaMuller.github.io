var selectLoginButton = document.querySelector("#selectLoginButton");
var selectRegisterButton = document.querySelector("#selectRegisterButton");
var loginButton = document.querySelector("#loginButton");
var registerButton = document.querySelector("#registerButton");
var addButton = document.querySelector("#add-button");
var chocolateUI = document.querySelector("#chocolateUI");
var loginUI = document.querySelector("#loginUI");
var registerUI = document.querySelector("#registerUI");
var unauthUI = document.querySelector("#unauthUI");
var adding = true;
var chocolateID = null;

//each fetch request needs credentials:'include'

//Button options if not logged in
selectLoginButton.onclick = function () {
    loginUI.style.display = "block";
    registerUI.style.display = "none";
    unauthUI.style.display = "none";
};

selectRegisterButton.onclick = function () {
    registerUI.style.display = "block"; //show register UI
    loginUI.style.display = "none";
    unauthUI.style.display = "none";
};

//after selected
loginButton.onclick = function () {
    var loginData = getLoginData();
    createSession(loginData);
    //login
};

registerButton.onclick = function () {
    var registerData = getRegisterData();
    createUser(registerData);
    //register
};


//if logged in 


addButton.onclick = function () {
    var chocolateData = getAndFormatData();

    if (adding == true)
        createChocolate(chocolateData);
    else {
        updateChocolate(chocolateData);
        addButton.innerHTML = "Add Chocolate";
    }
};

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
};


function getRegisterData() {
    //Step1: Query 
    var firstNameInput = document.querySelector("#firstName");
    var lastNameInput = document.querySelector("#lastName");
    var emailInput = document.querySelector("#email");
    var passwordInput = document.querySelector("#password");

    //step 2: capture text
    var firstName = firstNameInput.value;
    var lastName = lastNameInput.value;
    var email = emailInput.value;
    var password = passwordInput.value;

    //return formatted data
    var data = "first_name=" + encodeURIComponent(firstName);
    data += '&last_name=' + encodeURIComponent(lastName);
    data += '&email=' + encodeURIComponent(email);
    data += '&password=' + encodeURIComponent(password);

    return data;
};

//create a new chocolate on a server API
function createUser(registerData) {
    console.log('Sent data for registration: ', registerData);

    fetch("https://chocolates-app.herokuapp.com/users", { //dictionary
        method: 'POST',
        credentials: 'include',
        body: registerData,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        if (response.status == 201) {

            console.log("User created! Try Logging In");
            //here, the server has responded(async AJAX)
            //so, reload updated chocolates list
            selectLoginButton.onclick();
            userCreatedLogin.style.display = "block";
        }
        else if (response.status == 422) {
            console.log("User already exists. Try Logging In")
            errorRegistration.style.display = "block";
        }

    });
};


function getLoginData() {
    //Step1: Query 
    var emailInput = document.querySelector("#loginEmail");
    var passwordInput = document.querySelector("#loginPassword");
    //step 2: capture text
    var email = emailInput.value;
    var password = passwordInput.value;
    //return formatted data
    var data = 'email=' + encodeURIComponent(email);
    data += '&password=' + encodeURIComponent(password);

    return data;
};


//create a new chocolate on a server API
function createSession(loginData) {
    console.log('Sent data for login: ', loginData);


    fetch("https://chocolates-app.herokuapp.com/sessions", { //dictionary
        method: 'POST',
        credentials: 'include',
        body: loginData,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {

        userCreatedLogin.style.display = "none";
        if (response.status == 200 || response.status == 201) {
            //here, the server has responded(async AJAX)
            //so, reload updated chocolates list
            console.log("User login successful")
            loadChocolates();
        }
        else {
            unauthUI.style.display = "none";   //show login/register UI
            chocolatesUI.style.display = "none"; //hide List
            registerUI.style.display = "none"; //hide register
            loginUI.style.display = "block"; //hide login
            console.log("Unable to login. Try again")
            errorDiv.style.display = "block";

            //Hide restaurant UI
            //Show login or register UI
            return;
        };

    });
};


//create a new chocolate on a server API
function createChocolate(chocolateData) {
    console.log('Sent data for update: ', chocolateData);

    fetch("https://chocolates-app.herokuapp.com/chocolates", { //dictionary
        method: 'POST',
        credentials: 'include',
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

    fetch("https://chocolates-app.herokuapp.com/chocolates/" + chocolateID, {
        method: 'PUT',
        credentials: 'include',
        body: chocolateData,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(function (response) {
        loadChocolates();
    });
};

function deleteChocolateFromServer(chocolateID) {
    fetch("https://chocolates-app.herokuapp.com/chocolates/" + chocolateID, { method: "DELETE", credentials: 'include' }).then(function (response) {
        if (response.status == 401) {
            unauthUI.style.display = "block";   //show login/register UI
            chocolatesUI.style.display = "none"; //hide List
            registerUI.style.display = "none"; //hide register
            loginUI.style.display = "none"; //hide login

            //Hide restaurant UI
            //Show login or register UI
            return;
        };
        console.log("js delete response function started yay");
        if (response.status == 200) {
            console.log("chocolate successfully deleted");
            loadChocolates();
        };
    });
};

// load faveChocolates from the server as JSON data
function loadChocolates() {
    fetch("https://chocolates-app.herokuapp.com/chocolates", { credentials: 'include' }).then(function (response) {
        if (response.status == 401) {
            console.log("Unable to access site content: Error 401",);

            unauthUI.style.display = "block";   //show login/register UI
            chocolatesUI.style.display = "none"; //hide List
            registerUI.style.display = "none"; //hide register
            loginUI.style.display = "none"; //hide login
            return;
        }
        else if (response.status == 200) {
            unauthUI.style.display = "none";   //show login/register UI
            chocolatesUI.style.display = "grid"; //hide List
            registerUI.style.display = "none"; //hide register
            loginUI.style.display = "none"; //hide login
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
        }
    });
}

function displayEditForm(chocolateID, chocolateData) {
    console.log("edit button clicked", chocolateID, chocolateData, ratingDiv);
}

//immediately load chocolates
loadChocolates();