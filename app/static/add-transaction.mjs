import getMemosBySubtext from './api.mjs';
import autocomplete from './autocomplete.mjs';

function setupOperatorToggle() {
    const plusButton = document.querySelectorAll('.plus-button')[0];
    const minusButton = document.querySelectorAll('.minus-button')[0];

    plusButton.addEventListener('click', () => {
        minusButton.classList.remove('is-selected');
        minusButton.classList.remove('is-danger');

        plusButton.classList.add('is-selected');
        plusButton.classList.add('is-success');
    });

    minusButton.addEventListener('click', () => {
        plusButton.classList.remove('is-selected');
        plusButton.classList.remove('is-success');

        minusButton.classList.add('is-selected');
        minusButton.classList.add('is-danger');
    });
}

const OPERATOR = {
    MINUS: 'MINUS',
    PLUS: 'PLUS'
};

function getOperator() {
    const plusButton = document.querySelectorAll('.plus-button')[0];
    return plusButton.classList.contains('is-selected') ? OPERATOR.PLUS : OPERATOR.MINUS;
}

function onSubmit() {
    const selectedOperator = getOperator();
    const amountValue = document.transactionform.amount.value;

    if(isNaN(parseFloat(amountValue))) {
        return;
    }

    //Modify amount value
    document.transactionform.amount.value = selectedOperator === OPERATOR.PLUS ?
        Math.abs(parseFloat(amountValue)) :
        -Math.abs(parseFloat(amountValue));

    document.getElementById('transactionform').submit();
}

document.addEventListener('DOMContentLoaded', async function() {
    setupOperatorToggle();
    autocomplete(document.getElementById("memo-input"), getMemosBySubtext);
    document.getElementById('save-transaction').onclick = onSubmit;
});
