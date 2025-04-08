const signup = document.getElementById("sign-up");
signin = document.getElementById("sign-in");
loginin = document.getElementById("login-in");
loginup = document.getElementById("login-up");

signup.addEventListener("click", () => {
    loginin.classList.remove("block");
    loginup.classList.remove("none");

    loginin.classList.add("none");
    loginup.classList.add("block");
})

signin.addEventListener("click", () => {
    loginin.classList.remove("none");
    loginup.classList.remove("block");

    loginin.classList.add("block");
    loginup.classList.add("none");
})

document.getElementById('copyButton').addEventListener('click', function() {
    var addressText = document.querySelector('.Address__box').innerText.trim();
    copyToClipboard(addressText);
    displayAlert();
  });
  
  function copyToClipboard(text) {
    var textarea = document.createElement("textarea");
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
  }
  
  function displayAlert() {
    var alertElement = document.getElementById('alertMessage');
    alertElement.classList.remove('hidden');
    setTimeout(function() {
      alertElement.classList.add('hidden');
    }, 4000); // Hide the alert after 3 seconds
  }
  
  
  
  