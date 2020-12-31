let button = document.getElementsByClassName('update-cart');

for (let i = 0; i < button.length; i++) {
    button[i].addEventListener('click', function () {
        let productId = this.dataset.product;
        let action = this.dataset.action;


        if (user === "AnonymousUser") {
            console.log("User Not Logged In")
        } else {
            updateUserOrder(productId, action);
        }
    })
}

function updateUserOrder(productId, action) {
    let url = '/updateItem/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productID': productId, 'action': action})
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('data:', data)
            location.reload()
        })

}