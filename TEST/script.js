document.getElementById('predictBtn').addEventListener('click', function() {
    // ユーザーが入力した得点を取得
    const team1Score = document.getElementById('team1').value;
    const team2Score = document.getElementById('team2').value;

    // 結果表示用の要素
    const resultElement = document.getElementById('result');

    // 両方の得点が入力されているかチェック
    if (team1Score === "" || team2Score === "") {
        resultElement.textContent = "両方のチームの得点を入力してください。";
        resultElement.style.color = "red";
    } else {
        // 得点を予測結果として表示
        resultElement.textContent = `予想スコア: チーム1 ${team1Score} - ${team2Score} チーム2`;
        resultElement.style.color = "#28a745";
    }
});