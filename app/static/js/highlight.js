let isHighlight = localStorage.getItem('highlightChecked') !== 'false'; // default to true

function cancelBtnHandler() {
    cancelHighlighting();
    document.getElementById("text-content").removeEventListener("click", fillInWord, false);
    document.getElementById("text-content").removeEventListener("touchstart", fillInWord, false);
    document.getElementById("text-content").addEventListener("click", fillInWord2, false);
    document.getElementById("text-content").addEventListener("touchstart", fillInWord2, false);
}

function showBtnHandler() {
    if (document.getElementById("text-content")) {
	document.getElementById("text-content").removeEventListener("click", fillInWord2, false);
	document.getElementById("text-content").removeEventListener("touchstart", fillInWord2, false);
	document.getElementById("text-content").addEventListener("click", fillInWord, false);
	document.getElementById("text-content").addEventListener("touchstart", fillInWord, false);
	highLight();
    }
}
function replaceWords(str, word) {
  let count = 0;

  const regex = new RegExp(`(^|\\s)${word}(?=\\s|$)`, 'g');

  let result = str.replace(regex, (match, p1) => {
    count++;
    // p1 保留前导空格（如果有），仅第一个匹配保留，后续匹配替换为空字符串
    return count === 1 ? match : p1;
  });

  return result;
}

function countWords(str, word) {
  // 使用正则表达式匹配目标单词的整个单词边界情况，包括前后空格、行首和行尾
  const regex = new RegExp(`(^|\\s)${word}(?=\\s|$)`, 'g');
  let match;
  let count = 0;

  // 迭代匹配所有符合条件的单词
  while ((match = regex.exec(str)) !== null) {
    count++;
  }

  return count;
}
//用于替换单词
function replaceAllWords(str, word, replacement) {
  const regex = new RegExp(`(^|\\s)${word}(?=\\s|$)`, 'gi');
  let result = str.replace(regex, (match, p1) => {
    return p1 + replacement;
  });

  return result;
}

function getWord() {
    return window.getSelection ? window.getSelection().toString() : document.selection.createRange().text;
}

function highLight() {
    if (!isHighlight) return;
    let word = (getWord() + "").trim().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "");
    let articleContent = document.getElementById("article").innerHTML; // innerHTML保留HTML标签来保持部分格式，且适配不同的浏览器
    let pickedWords = document.getElementById("selected-words");  // words picked to the text area
    let dictionaryWords = document.getElementById("selected-words2"); // words appearing in the user's new words list
    let allWords = dictionaryWords === null ? pickedWords.value + " " : pickedWords.value + " " + dictionaryWords.value;
    let highlightWords = document.getElementById("selected-words3");
    allWords = highlightWords == null ? allWords : allWords + " " + highlightWords.value;
    const list = allWords.split(" "); // 将所有的生词放入一个list中
    if(word !== null && word !== "" && word !== " "){
        if(localStorage.getItem("nowWords").indexOf(word) !== -1 || localStorage.getItem("nowWords").indexOf(word.toLowerCase()) !== -1){
            articleContent = articleContent.replace(new RegExp('<span class="highlighted">' + word + '</span>', "g"), word);

    let count=countWords(pickedWords.value,word)
    let currentWords=localStorage.getItem("nowWords")+" "+word
    localStorage.setItem("nowWords",currentWords)
//
    if(count>0){
        if(count==1){
            localStorage.setItem("nowWords",replaceWords(currentWords,word))
        }else{
            localStorage.setItem("nowWords",replaceAllWords(currentWords,word,""))
        }
    }


    pickedWords.value = localStorage.getItem("nowWords")
            document.getElementById("article").innerHTML = articleContent;
            return;
        }
    }
    let totalSet = new Set();
    for (let i = 0; i < list.length; ++i) {
        list[i] = list[i].replace(/(^\W*)|(\W*$)/g, ""); // 消除单词两边的非单词字符
        list[i] = list[i].replace('|', "");
        list[i] = list[i].replace('?', "");
        if (list[i] != "" && !totalSet.has(list[i])) {
            // 返回所有匹配单词的集合, 正则表达式RegExp()中, "\b"匹配一个单词的边界, g 表示全局匹配, i 表示对大小写不敏感。
            let matches = new Set(articleContent.match(new RegExp("\\b" + list[i] + "\\b", "gi")));
            totalSet = new Set([...totalSet, ...matches]);
        }
    }
    // 删除所有的"<span class='highlighted'>"标签,防止标签发生嵌套
    articleContent = articleContent.replace(new RegExp('<span class="highlighted">',"gi"), "")
    articleContent = articleContent.replace(new RegExp("</span>","gi"), "");
    // 将文章中所有出现该单词word的地方改为："<span class='highlighted'>" + word + "</span>"。
    for (let word of totalSet) {
        articleContent = articleContent.replace(new RegExp("\\b" + word + "\\b", "g"), "<span class='highlighted'>" + word + "</span>");
    }
    document.getElementById("article").innerHTML = articleContent;
    addClickEventToHighlightedWords();
}

function cancelHighlighting() {
    let articleContent = document.getElementById("article").innerHTML;
    articleContent = articleContent.replace(new RegExp('<span class="highlighted">',"gi"), "")
    articleContent = articleContent.replace(new RegExp("</span>","gi"), "");
    document.getElementById("article").innerHTML = articleContent;
}

function fillInWord() {
    highLight();
}

function fillInWord2() {
    cancelHighlighting();
}

function toggleHighlighting() {
    if (isHighlight) {
        isHighlight = false;
        cancelHighlighting();
    } else {
        isHighlight = true;
        highLight();
    }
    localStorage.setItem('highlightChecked', isHighlight);
}

function showWordMeaning(event) {
    const word = event.target.innerText.trim().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").toLowerCase();
    const apiUrl = '/translate';
    const rect = event.target.getBoundingClientRect();
    const tooltipX = rect.left + window.scrollX;
    const tooltipY = rect.top + window.scrollY + rect.height;
    // 发送POST请求
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ word: word }), // 发送的JSON数据
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // 解析JSON响应
        })
        .then(data => {
            // 假设data.translation是翻译结果
            const tooltip = document.getElementById('tooltip');
            if (!tooltip) {
                console.error('Tooltip element not found');
                return;
            }

            tooltip.textContent = data.translation || '没有找到该单词的中文意思';
            tooltip.style.left = `${tooltipX}px`;
            tooltip.style.top = `${tooltipY}px`;
            tooltip.style.display = 'block';
	    tooltip.style.position = 'absolute';
	    tooltip.style.background = 'yellow';

            // 可以在这里添加点击事件监听器来隐藏tooltip，但注意避免内存泄漏
            document.addEventListener('click', function handler(e) {
                if (!tooltip.contains(e.target)) {
                    tooltip.style.display = 'none';
                    document.removeEventListener('click', handler);
                }
            });
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
        });
}

function addClickEventToHighlightedWords() {
    const highlightedWords = document.querySelectorAll('.highlighted');
    highlightedWords.forEach(word => {
        word.addEventListener('click', showWordMeaning);
    });
}

showBtnHandler();
