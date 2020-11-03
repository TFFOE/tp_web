function login() {
    var userblock = document.getElementById("userblock");
    userblock.classList.add('logged-user');
}

function logout() {
    var userblock = document.getElementById("userblock");
    userblock.classList.remove("logged-user");
}