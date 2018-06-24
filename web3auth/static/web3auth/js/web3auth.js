web3auth = {

    init: function (loginToken) {
        $(() => {
            if (typeof web3 !== 'undefined') {
                web3 = new Web3(web3.currentProvider);
                web3.eth.getAccounts((err, accounts) => { // Check for wallet being locked
                    if (err) {
                        throw err;
                    }
                    if (accounts.length == 0) {
                        $('[data-web3auth-display]').hide();
                        $('[data-web3auth-display="wallet-locked"]').show();
                    } else {
                        $('[data-web3auth-display]').hide();
                        $('[data-web3auth-display="wallet-available"]').show();
                    }

                });
            } else {
                $('[data-web3auth-display]').hide();
                $('[data-web3auth-display="wallet-unavailable"]').show();
            }

        });
        let loginBtn = $('[data-web3auth="login-button"]');
        $(loginBtn).click(() => {
            web3auth.login(loginToken, $('[data-web3auth="login-form"]'));
            return false;
        });

    },

    login: function (loginToken, form) {
        if (typeof web3 == 'undefined') {
            throw 'web3 missing';
        }
        msg = web3.toHex(loginToken);
        from = web3.eth.accounts[0];
        web3.personal.sign(msg, from, (err, result) => {
            if (err) {
                console.log(err, result);
            } else {
                $(form).find('input[name=signature]').val(result);
                $(form).submit();
            }
        });

    }
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function loginWithSignature(address, signature) {
    var request = new XMLHttpRequest();
    request.open('POST', '/login_api/', true);
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            var resp = request.responseText;
            console.log(JSON.parse(resp));
        } else {
            // We reached our target server, but it returned an error
            console.log("Autologin failed - request status " + request.status)
        }
    };

    request.onerror = function () {
        console.log("Autologin failed - there was an error")

        // There was a connection error of some sort
    };
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    var formData = 'address='+address+'&signature='+signature;
    request.send(formData);
}

function checkWeb3(callback) {
    web3.eth.getAccounts((err, accounts) => { // Check for wallet being locked
        if (err) {
            throw err;
        }
        callback(accounts.length !== 0);
    });
}

function autoLogin() {
    // 1. Retrieve arbitrary login token from server
    // 2. Sign it using web3
    // 3. Send signed message & your eth address to server
    // 4. If server validates that you signature is valid
    // 4.1 The user with an according eth adress is found - you are logged in
    // 4.2 The user with an according eth adress is NOT found - you are redirected to signup page


    var request = new XMLHttpRequest();
    request.open('GET', '/login_api/', true);

    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            var resp = JSON.parse(request.responseText);
            var token = resp.data;
            console.log("Token: " + token);
            var msg = web3.toHex(token);
            var from = web3.eth.accounts[0];
            web3.personal.sign(msg, from, (err, result) => {
                if (err) {
                    console.log("Failed signing message \n" + msg + "\n - " + err);
                } else {
                    console.log("Signed message: " + result);
                    loginWithSignature(from, result);
                }
            });

        } else {
            // We reached our target server, but it returned an error
            console.log("Autologin failed - request status " + request.status)
        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
        console.log("Autologin failed - there was an error")
    };
    request.send();

}

function ready(fn) {
    if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading") {
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

ready(function () {
    if (typeof web3 !== 'undefined') {
        checkWeb3(function (loggedIn) {
            if (!loggedIn) {
                console.log("Please unlock your web3 provider (probably, Metamask)")
            } else {
                autoLogin();
            }
        });

    } else {
        console.log('web3 missing');
    }
});
