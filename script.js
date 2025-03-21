let board = Array(9).fill(null);
let currentPlayer = "X";
let xScore = 0;
let oScore = 0;

const buttons = document.querySelectorAll(".game-button");
const scoreX = document.getElementById("score-x");
const scoreO = document.getElementById("score-o");
const turnLabel = document.getElementById("turn");

function playMove(index) {
    if (board[index] || checkWin()) return;
    
    board[index] = currentPlayer;
    buttons[index].textContent = currentPlayer;
    buttons[index].style.color = currentPlayer === "X" ? "blue" : "red";

    if (checkWin()) {
        updateScore();
        alert(`${currentPlayer} a gagné!`);
        resetGame();
    } else if (board.every(cell => cell !== null)) {
        alert("Match nul!");
        resetGame();
    } else {
        currentPlayer = currentPlayer === "X" ? "O" : "X";
        turnLabel.textContent = `C'est au tour de ${currentPlayer}`;
    }
}

function checkWin() {
    const winningCombinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  // lignes
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  // colonnes
        [0, 4, 8], [2, 4, 6]              // diagonales
    ];

    return winningCombinations.some(combination => {
        const [a, b, c] = combination;
        return board[a] && board[a] === board[b] && board[a] === board[c];
    });
}

function updateScore() {
    if (currentPlayer === "X") {
        xScore++;
        scoreX.textContent = `X: ${xScore}`;
    } else {
        oScore++;
        scoreO.textContent = `O: ${oScore}`;
    }
}

function resetGame() {
    board.fill(null);
    buttons.forEach(button => button.textContent = "");
    currentPlayer = "X";
    turnLabel.textContent = `C'est au tour de ${currentPlayer}`;
}