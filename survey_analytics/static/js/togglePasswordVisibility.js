function togglePasswordVisibility() {
    const passwordField = document.getElementById('password');
    const toggleIcon = document.getElementById('toggle-password');

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.src = eyeOpenIcon;
    } else {
        passwordField.type = 'password';
        toggleIcon.src = eyeClosedIcon;
    }
}