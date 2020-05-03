function check_input() {

    let input_credito = document.getElementById('input_credito');
    let input_debito = document.getElementById('input_debito');
    let input_credito_cvv = document.getElementById('input_credito_cvv');
    let input_credito_titular = document.getElementById('input_credito_titular');

    if (input_credito.value || input_credito_cvv.value || input_credito_titular.value) {
        document.getElementById('debito-tab').classList.add('disabled');
        // input_debito.setAttribute('required', true);
        // input_credito.setAttribute('required', true);
        // input_credito_cvv.setAttribute('required', true);
        // input_credito_titular.setAttribute('required', true);
    } else {
        document.getElementById('debito-tab').classList.remove('disabled');
        input_debito.removeAttribute('required');
        input_credito.removeAttribute('required');
        input_credito_cvv.removeAttribute('required');
        input_credito_titular.removeAttribute('required');
    }
    
    if (input_debito.value) {
        document.getElementById('credito-tab').classList.add('disabled');
        // input_debito.setAttribute('required', true);
    } else {
        document.getElementById('credito-tab').classList.remove('disabled');
        input_debito.removeAttribute('required');
    }



};
