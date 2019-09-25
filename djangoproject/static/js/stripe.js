
// https secure site when live

var paymentForm = $(".payment-form")
if (paymentForm.length > 1){
    alert("Only one payment form is allowed per page")
    paymentForm.css('display', 'none')
}
else if (paymentForm.length == 1) {

var pubKey = paymentForm.attr('data-token')
var nextUrl = paymentForm.attr('data-next-url')
    // Create a Stripe client
var stripe = Stripe(pubKey);

// Create an instance of Elements
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    lineHeight: '24px',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

var form = $('#payment-form');
form.on('submit', function(event) {
  event.preventDefault();
  var $this = $(this)
  var currentTimeout;
  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error
      var errorElement = $('#card-errors');
      errorElement.textContent = result.error.message;
      } else {
        // Send the token to your server
        stripeTokenHandler(nextUrl, result.token);
      }
  });
});

function redirectToNext(nextPath, timeoffset) {
    // body...
    if (nextPath){
    setTimeout(function(){
                window.location.href = nextPath
            }, timeoffset)
    }
}

function stripeTokenHandler(nextUrl, token){
    console.log(token.id)
    var paymentMethodEndpoint = '/billing/payment-method/create/'
    var data = {
        'token': token.id
    }
    console.log(data)
    $.ajax({
        data: data,
        url: paymentMethodEndpoint,
        method: "POST",
        success: function(data){
            var succesMsg = data.message || "Success! Your card was added."
            card.clear()
            if (nextUrl){
                succesMsg = succesMsg
            }
            if ($.alert){
                $.alert(succesMsg)
            } else {
                alert(data)
            }
            redirectToNext(nextUrl, 1500) 
        },
        error: function(error){
            // console.log(error)
            alert({title: "An error occured", content:"Please try adding your card again."})
        }
    })
}
}
