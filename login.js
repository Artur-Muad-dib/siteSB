document.getElementById('login-button').addEventListener('click', async () => {
    const cpf = document.getElementById('cpf').value;
    const senha = document.getElementById('senha').value;

    const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cpf, senha })
    });

    const result = await response.json();

    if (response.status === 200) {
        // Redireciona para a página do mapa
        window.location.href = 'mapa.html';
    } else {
        alert(result.detail);
    }
});