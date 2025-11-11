function containsDigitsLettersSpecialCharacters(s) {
    let resultD = 0, resultL = 0, resultS = 0;

    // Digit test
    '0123456789'.split('').forEach((x) => {
	if (s.includes(x))
	    resultD = 1;
    });

    // Letter test
    resultL =  /[a-z]/i.test(s);

    // Special charater test
    '+-*/,.:;/\[]<>$%&()!?^~'.split('').forEach((x) => {
	if (s.includes(x))
	    resultS = 1;
    });

    return resultD + resultL + resultS == 3;
}
