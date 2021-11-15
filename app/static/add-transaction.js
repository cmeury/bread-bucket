function setupOperatorToggle() {
    var plusButton = document.querySelectorAll('.plus-button')[0];
    var minusButton = document.querySelectorAll('.minus-button')[0];

    plusButton.addEventListener('click', function() {
        minusButton.classList.remove('is-selected');
        minusButton.classList.remove('is-danger');

        plusButton.classList.add('is-selected');
        plusButton.classList.add('is-success');
    });

    minusButton.addEventListener('click', function() {
        plusButton.classList.remove('is-selected');
        plusButton.classList.remove('is-success');

        minusButton.classList.add('is-selected');
        minusButton.classList.add('is-danger');
    });
}


var OPERATOR = {
    MINUS: 'MINUS',
    PLUS: 'PLUS'
};

function getOperator() {
    var plusButton = document.querySelectorAll('.plus-button')[0];
    return plusButton.classList.contains('is-selected') ? OPERATOR.PLUS : OPERATOR.MINUS;
}

function onSubmit() {
    var selectedOperator = getOperator();
    var amountValue = document.transactionform.amount.value;

    if(isNaN(parseFloat(amountValue))) {
        return;
    }

    //Modify amount value
    document.transactionform.amount.value = selectedOperator === OPERATOR.PLUS ?
        Math.abs(parseFloat(amountValue)) :
        -Math.abs(parseFloat(amountValue));

    document.getElementById('transactionform').submit();
}

document.addEventListener('DOMContentLoaded', function() {
    setupOperatorToggle();
});
