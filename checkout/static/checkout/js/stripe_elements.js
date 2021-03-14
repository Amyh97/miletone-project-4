/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// values from form.py passed through json script. Camel case to match stripe docs and match js syntax
// use 1 and -1 to remove quote marks
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

var card = elements.create("card");
card.mount("#card-element", { style: style });