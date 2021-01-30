function checkProgress() {
    if ($("input:radio[name*='paymentMethod']:checked").length !== 0) {
        $('.continue').prop('disabled', false);
    } else {
        $('.continue').prop('disabled', true);
    }
}

$(function () {
    checkProgress();
    $("input:radio[name*='paymentMethod']").change(checkProgress, checkForCard);
});

function checkForCard() {
    if ($("input:radio[id*='card']:checked").length !== 0){
        $('.hide').css("display", "block")
    }else {
        $('.hide').css("display", "none")
    }
}