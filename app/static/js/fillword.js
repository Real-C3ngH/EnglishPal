let isRead = localStorage.getItem('readChecked') !== 'false';  // default to true
let isChoose = localStorage.getItem('chooseChecked') !== 'false';

function getWord() {
    return window.getSelection ? window.getSelection() : document.selection.createRange().text;
}

function fillInWord() {
    let word = getWord();
    if (isRead) Reader.read(word, inputSlider.value);
    if (!isChoose) {
        if(isHighlight){
             const element = document.getElementById("selected-words3");
             element.value = element.value + " " + word;
        }
        return;
    }
    const element = document.getElementById("selected-words");
    localStorage.setItem('nowWords', element.value);
    element.value = element.value + " " + word;
    localStorage.setItem('selectedWords', element.value);
}

if (document.getElementById("text-content")) {
    document.getElementById("text-content").addEventListener("click", fillInWord, false);
}

const sliderValue = document.getElementById("rangeValue");
const inputSlider = document.getElementById("rangeComponent");

if (inputSlider) {
    inputSlider.oninput = () => {
	let value = inputSlider.value;
	sliderValue.textContent = value + '×';
    };
}

function onReadClick() {
    isRead = !isRead;
    localStorage.setItem('readChecked', isRead);
}

function onChooseClick() {
    isChoose = !isChoose;
    localStorage.setItem('chooseChecked', isChoose);
}

// 如果网页刷新，停止播放声音
if (performance.getEntriesByType("navigation")[0].type == "reload") {
    Reader.stopRead();
}

