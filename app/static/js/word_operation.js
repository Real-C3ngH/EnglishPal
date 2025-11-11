function familiar(theWord) {
    let username = $("#username").text();
    let word = document.getElementById(`word_${theWord}`).innerText;
    let freq = document.getElementById(`freq_${theWord}`).innerText;
    console.log(theWord);
    console.log(word);
    $.ajax({
        type:"GET",
        url:"/" + username + "/" + word + "/familiar",
        success:function(response) {
            let new_freq = freq - 1;
            const allow_move = document.getElementById("move_dynamiclly").checked;
            if (allow_move) {
                if (new_freq <= 0) {
                    removeWord(theWord);
                } else {
                    renderWord({word: theWord, freq: new_freq});
                }
            } else {
                if(new_freq <1) {
                    $("#p_" + theWord).remove();
                } else {
                    $("#freq_" + theWord).text(new_freq);
                }
            }
        }
    });
}

function unfamiliar(theWord) {
    let username = $("#username").text();
    let word = document.getElementById(`word_${theWord}`).innerText;
    let freq = document.getElementById(`freq_${theWord}`).innerText;
    console.log(theWord);
    console.log(word);
    $.ajax({
        type:"GET",
        url:"/" + username + "/" + word + "/unfamiliar",
        success:function(response) {
            let new_freq = parseInt(freq) + 1;
            const allow_move = document.getElementById("move_dynamiclly").checked;
            if (allow_move) {
                renderWord({word: theWord, freq: new_freq});
            } else {
                $("#freq_" + theWord).text(new_freq);
            }
        }
    });
}

function delete_word(theWord) {
    let username = $("#username").text();
    let word = theWord.replace('&amp;', '&');
    $.ajax({
        type:"GET",
        url:"/" + username + "/" + word + "/del",
        success:function(response) {
            const allow_move = document.getElementById("move_dynamiclly").checked;
            if (allow_move) {
                removeWord(theWord);
            } else {
                $("#p_" + theWord).remove();
            }
	    // remove highlighting for the word
	    let highlightedWords = document.querySelectorAll('.highlighted');
	    for (let x of highlightedWords) {
		if (x.innerHTML == word)
		    x.replaceWith(x.innerHTML);
	    }
        }
    });
}

function read_word(theWord) {
    let to_speak = $("#word_" + theWord).text();
    original_position = 0;
    current_position = 0;
    Reader.read(to_speak, inputSlider.value);
}


/* 
 * interface Word {
 *   word: string,
 *   freq: number
 * }
* */

/**
 * 传入一个词频HTML元素，将其解析为Word类型的对象
 */
function parseWord(element) {
    const word = element
        .querySelector("a.btn.btn-light[role=button]")  // 获取当前词频元素的词汇元素
        .innerText  // 获取词汇值;
    let freqId = `freq_${word}`;
    freqId = CSS.escape(freqId); // for fixing bug 580, escape the apostrophe in the word
    const freq = Number.parseInt(element.querySelector("#"+freqId).innerText);   // 获取词汇的数量
    return {
        word,
        freq
    };
}

/**
 * 使用模板将传入的单词转换为相应的HTML字符串
*/
function wordTemplate(word) {
    // 这个模板应当与 templates/userpage_get.html 中的 <p id='p_${word.word}' class="new-word" > ... </p> 保持一致
    return `<p id="p_${word.word}" class="new-word" >
        <a id="word_${word.word}"  class="btn btn-light" href='http://youdao.com/w/eng/${word.word}/#keyfrom=dict2.index'
           role="button">${word.word}</a>
        ( <a id="freq_${word.word}" title="${word.word}">${word.freq}</a> )
        <a class="btn btn-success" onclick=familiar("${word.word}") role="button">熟悉</a>
        <a class="btn btn-warning" onclick=unfamiliar("${word.word}") role="button">不熟悉</a>
        <a class="btn btn-danger" onclick=delete_word("${word.word}") role="button">删除</a>
        <a class="btn btn-info" onclick=read_word("${word.word}") role="button">朗读</a>
        <a class="btn btn-primary" onclick="addNote('{{ word }}'); saveNote('{{ word }}')" role="button">笔记</a> <!-- Modify to call addNote and then saveNote -->
        <input type="text" id="note_{{ word }}" class="note-input" placeholder="输入笔记内容" style="display:none;" oninput="saveNote('{{ word }}')"> <!-- Added oninput event -->
    </p>`;
}


/**
 * 删除某一词频元素
 * 此处word为词频元素对应的单词
 */
function removeWord(word) {
    // 根据词频信息删除元素
    word = word.replace('&amp;', '&');
    const element_to_remove = document.getElementById(`p_${word}`);
    if (element_to_remove !== null) {
        element_to_remove.remove();
    }
}

function renderWord(word) {
    const container = document.querySelector(".word-container");
    // 删除原有元素
    removeWord(word.word);
    // 插入新元素
    let inserted = false;
    const new_element = elementFromString(wordTemplate(word));
    for (const current of container.children) {
        const cur_word = parseWord(current);
        // 找到第一个词频比它小的元素，插入到这个元素前面
        if (compareWord(cur_word, word) === -1) {
            container.insertBefore(new_element, current);
            inserted = true;
            break;
        }
    }
    // 当word就是词频最小的词时，把他补回去
    if (!inserted) {
        container.appendChild(new_element);
    }
    // 让发生变化的元素抖动
    new_element.classList.add("shaking");
    // 移动到该元素
    new_element.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
    // 抖动完毕后删除抖动类
    setTimeout(() => {
        new_element.classList.remove("shaking");
    }, 1600);
}

/**
 * 从string中创建一个HTML元素并返回
 */
function elementFromString(string) {
    const d = document.createElement('div');
    d.innerHTML = string;
    return d.children.item(0);
}

/**
 * 对比两个单词：
 *  当first小于second时返回-1
 *  当first等于second时返回0
 *  当first大于second时返回1
 */
function compareWord(first, second) {
    if (first.freq !== second.freq) {
        return first.freq < second.freq ? -1 : 1;
    }
    if (first.word !== second.word) {
        return first.word < second.word ? -1 : 1;
    }
    return 0;
}

/* 生词csv导出 */
function exportToCSV() {
    let csvContent = "data:text/csv;charset=utf-8,Word,Frequency\n";
    let rows = document.querySelectorAll(".new-word");

    rows.forEach(row => {
        let word = row.querySelector("a.btn-light").innerText;
        let freq = row.querySelector("a[title]").innerText;
        csvContent += word + "," + freq + "\n";
    });

    let encodedUri = encodeURI(csvContent);
    let link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "word_list.csv");
    document.body.appendChild(link);

    link.click();
    document.body.removeChild(link);
}

/**
 *
 * 随机选取 10 个单词学习
 */
function random_select_word(word) {

    // 获取所有带有 "word-container" 类的 <p> 标签
    const container = document.querySelector('.word-container');

    console.log("container",container)

    // 获取所有带有"new-word"类的<p>标签
    let wordContainers = container.querySelectorAll('.new-word');

    // 检查是否存在带有"new-word"类的<p>标签
    if (wordContainers.length > 0) {
      // 将NodeList转换为数组
      let wordContainersArray = [...wordContainers];

      // 随机打乱数组，乱序
      for (let i = wordContainersArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [wordContainersArray[i], wordContainersArray[j]] = [wordContainersArray[j], wordContainersArray[i]];
      }

        wordContainersArray.forEach((p, index) => {
          if (index < 10) {
            p.style.display = 'block';
          } else {
            p.style.display = 'none';
          }
        });
    }
}
