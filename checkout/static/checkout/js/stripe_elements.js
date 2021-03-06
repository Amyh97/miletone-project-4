/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
var clientSecret = $("#id_client_secret").text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
// style from stripe docs, updated colour to black and invalid colours to match bootstrap danger
var style = {
    base: {
        color: "#000",
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: "antialiased",
        fontSize: "16px",
        "::placeholder": {
            color: "#aab7c4",
        },
    },
    invalid: {
        color: "#dc3545",
        iconColor: "#dc3545",
    },
};
var card = elements.create("card", { style: style });
card.mount("#card-element");

// Handle realtime validation errors in card element

card.addEventListener("change", function (event) {
    var errorDiv = document.getElementById("card-errors");
    $(errorDiv).empty();
    if (event.error) {
        var html = `<span role="alert">
	                <p><i class="fas fa-times"></i> ${event.error.message}</p>
	            </span>`;

        $(errorDiv).html(html);
    } else {
        $(errorDiv).textContent = "";
    }
});
// from stripe docs, and personalised for Django and site html
// Handle form submit
var form = document.getElementById("payment-form");

form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    card.update({ disabled: true });
    $("#submit-button").attr("disabled", true);
    $("#payment-form").fadeToggle(100);
    $("#loading-overlay").fadeToggle(100);

    var saveInfo = Boolean($("#save-info").attr("checked"));
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        // value assigned above
        csrfmiddlewaretoken: csrfToken,
        client_secret: clientSecret,
        save_info: saveInfo,
    };
    var url = "/checkout/cache_checkout_data/";

    // post data to views via the url
    // use .done() to send it server returns 200 status
    $.post(url, postData)
        .done(function () {
            // confirmCardPayment is stripe function
            stripe
                .confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: card,
                        billing_details: {
                            // use trip to remove whitespace
                            // all fields in model
                            name: $.trim(form.full_name.value),
                            phone: $.trim(form.phone_number.value),
                            email: $.trim(form.email.value),
                            address: {
                                // postcode comes from card element
                                line1: $.trim(form.street_address1.value),
                                line2: $.trim(form.street_address2.value),
                                city: $.trim(form.town_or_city.value),
                                country: $.trim(form.country.value),
                            },
                        },
                    },
                    // for future scope of sending products to different address to billing
                    shipping: {
                        name: $.trim(form.full_name.value),
                        phone: $.trim(form.phone_number.value),
                        address: {
                            line1: $.trim(form.street_address1.value),
                            line2: $.trim(form.street_address2.value),
                            city: $.trim(form.town_or_city.value),
                            country: $.trim(form.country.value),
                            postal_code: $.trim(form.postcode.value),
                        },
                    },
                })
                .then(function (result) {
                    if (result.error) {
                        var errorDiv = document.getElementById("card-errors");
                        var html = `<span role="alert">
	                        <p><i class="fas fa-times"></i> ${result.error.message}</p>
	                    </span>`;

                        $(errorDiv).html(html);
                        $("#payment-form").fadeToggle(100);
                        $("#loading-overlay").fadeToggle(100);
                        card.update({ disabled: false });
                        $("#submit-button").attr("disabled", false);
                    } else {
                        if (result.paymentIntent.status === "succeeded") {
                            form.submit();
                        }
                    }
                });
            // use .fail if the view returns a 400 bad request response
        })
        .fail(function () {
            // just reload the page, the error will be in django messages
            location.reload();
        });
});
