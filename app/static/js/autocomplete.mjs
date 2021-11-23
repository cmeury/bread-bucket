import debounce from './third-party/p-debounce.mjs';

/* Copied from https://www.w3schools.com/howto/howto_js_autocomplete.asp
  * and modified to suite our needs. Thanks w3schools!
  */

const UP_KEY_CODE = 38;
const DOWN_KEY_CODE = 40;
const ENTER_KEY_CODE = 13;
const TAB_KEY_CODE = 9;
const ITERATOR = 1;

/* The autocomplete function takes two arguments,
  the text field element and a function that returns an array of possible autocompleted values:*/
export default function autocomplete(inp, fetchArr) {
  let currentFocus;
  /*execute a function when someone writes in the text field:*/
  //Debounce so we don't blast the api endpoint every keystroke
  inp.addEventListener('keyup', debounce(async function(e) {
    if(e.keyCode === UP_KEY_CODE ||
      e.keyCode === DOWN_KEY_CODE ||
      e.keyCode === ENTER_KEY_CODE ||
      e.keyCode === TAB_KEY_CODE) { return; }

    const val = this.value;
    /*close any already open lists of autocompleted values*/
    closeAllLists();

    if (!val) { return false; }
    const arr = (await fetchArr(val)).memos;
    currentFocus = -ITERATOR;

    /*create a DIV element that will contain the items (values):*/
    const a = document.createElement('DIV');
    a.setAttribute('id', this.id + 'autocomplete-list');
    a.setAttribute('class', 'autocomplete-items');

    /*append the DIV element as a child of the autocomplete container:*/
    this.parentNode.appendChild(a);

    for (let i = 0; i < arr.length; i++) {
      /*check if the item contains the text field value:*/
      const uppercaseArrStr = arr[i].toUpperCase();
      if (uppercaseArrStr.includes(val.toUpperCase())) {
        /*create a DIV element for each matching element:*/
        const b = document.createElement('DIV');
        /*make the matching letters bold:*/
        const indexOfValString = uppercaseArrStr.indexOf(val.toUpperCase());
        if (indexOfValString === 0) {
          b.innerHTML = '<strong>' + arr[i].substr(0, val.length) + '</strong>';
          b.innerHTML += arr[i].substr(val.length);
        } else {
          b.innerHTML = arr[i].substr(0, indexOfValString);
          b.innerHTML += '<strong>' + arr[i].substr(indexOfValString, val.length) + '</strong>';
          b.innerHTML += arr[i].substr(indexOfValString + val.length);
        }
        /*insert a input field that will hold the current array item's value:*/
        b.innerHTML += '<input type="hidden" value="' + arr[i] + '">';
        /*execute a function when someone clicks on the item value (DIV element):*/
        b.addEventListener('click', function() {
          /*insert the value for the autocomplete text field:*/
          inp.value = this.getElementsByTagName('input')[0].value;
          /*close the list of autocompleted values,
            (or any other open lists of autocompleted values:*/
          closeAllLists();
        });
        a.appendChild(b);
      }
    }
  }, 300));

  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener('keydown', function(e) {
    let x = document.getElementById(this.id + 'autocomplete-list');
    if (x) {
      x = x.getElementsByTagName('div');
    }
    if (e.keyCode === DOWN_KEY_CODE) {
      /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
      /*and and make the current item more visible:*/
        addActive(x);
    } else if (e.keyCode === UP_KEY_CODE) { //up
      /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
      /*and and make the current item more visible:*/
        addActive(x);
    } else if (e.keyCode === ENTER_KEY_CODE) {
      /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
      if (currentFocus > -ITERATOR) {
        /*and simulate a click on the "active" item:*/
          if (x) {
            x[currentFocus].click();
            inp.blur();
          }
      } else {
        closeAllLists();
        inp.blur();
      }
    } else if(e.keyCode === TAB_KEY_CODE) {
        closeAllLists();
    }
  });

  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) { return false; }
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length){
      currentFocus = 0;
    }
    if (currentFocus < 0) {
      currentFocus = (x.length - 1);
    }
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add('autocomplete-active');
  }

  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove('autocomplete-active');
    }
  }

  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }

  /*execute a function when someone clicks in the document:*/
  document.addEventListener('click', function (e) {
    closeAllLists(e.target);
  });
}
