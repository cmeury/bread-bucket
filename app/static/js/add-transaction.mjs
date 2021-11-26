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

function formatAmountInputValue (e) {
    let value = e.target.value || '0';
    value = parseInt(value.replace('.',''), 10);
    value = isNaN(value) ? 0 : value;
    if(value <= 999) {
        value = ("000"+value).slice(-3);
    }
    value = value.toString();
    value = value.substr(0, value.length - 2) + '.' + value.substr(value.length - 2);
    e.target.value = value;
}

function amountKeydown(e) {
    e.preventDefault();
    //Prevent non-number inputs
    const NUM_KEY_CODES = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57],
        BACKSPACE_KEY_CODE = 8,
        DELETE_KEY_CODE = 46;
    const ALLOWED_KEY_CODES = [].concat(
        NUM_KEY_CODES,
        BACKSPACE_KEY_CODE,
        DELETE_KEY_CODE);
    if(ALLOWED_KEY_CODES.indexOf(e.keyCode) === -1) {
        return;
    }
    if(NUM_KEY_CODES.indexOf(e.keyCode) !== -1) {
        e.target.value += e.key;
        formatAmountInputValue(e);
    }
    if(e.keyCode === BACKSPACE_KEY_CODE ||
        e.keyCode === DELETE_KEY_CODE) {
        const currentValue = e.target.value;
        if(currentValue.length > 0) {
            e.target.value = currentValue.substr(0, currentValue.length - 1);
            formatAmountInputValue(e);
        }
    }
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
    document.getElementById('save-transaction')
        .onclick = onSubmit;
    document.getElementById('amount-input')
        .addEventListener('keydown', amountKeydown);
    document.getElementById('amount-input')
        .oninput = formatAmountInputValue;
});
