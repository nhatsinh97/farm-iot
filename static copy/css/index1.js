document.getElementById("login-button").addEventListener("click", function() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (username === "tk" && password === "mk") {
        alert("Đăng nhập thành công!");
    } else {
        alert("Tên người dùng hoặc mật khẩu không chính xác.");
    }
});
