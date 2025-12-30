function App() {
  const [games, setGames] = React.useState([]);
  const [amount, setAmount] = React.useState(100);
  const [loading, setLoading] = React.useState(false);

const generateGames = async () => {
  setLoading(true);
  setGames([]); // Limpa jogos antigos antes de começar
  
  try {
    // Forçamos a conversão para número inteiro aqui
    const quantity = parseInt(amount, 10);
    
    const res = await axios.post("/api/generate", {
      games: quantity,
    });
    
    console.log("Dados recebidos:", res.data);
    setGames(res.data.games);
  } catch (e) {
    console.error("Erro detalhado:", e.response?.data);
    alert("Erro na API. Verifique o console do navegador.");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="container">
      <h1>🎯 Mega IA</h1>

      <div className="controls">
        <input
          type="number"
          min="1"
          max="500"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <button onClick={generateGames} disabled={loading}>
          {loading ? "Gerando..." : "Gerar Jogos"}
        </button>
      </div>

      <div className="games">
        {games.length > 0 ? (
          games.map((game, i) => (
            <div key={i} className="game" style={{ flexDirection: 'column', alignItems: 'center' }}>
              {/* NUMERAÇÃO DO JOGO */}
              <small style={{ marginBottom: '8px', color: '#94a3b8', fontWeight: 'bold', fontSize: '0.75rem', textTransform: 'uppercase' }}>
                Jogo {String(i + 1).padStart(2, '0')}
              </small>
              
              {/* CONTAINER DAS BOLINHAS */}
              <div style={{ display: 'flex', gap: '8px' }}>
                {game.map((n, idx) => (
                  <span key={idx} className="number-ball">
                    {String(n).padStart(2, '0')}
                  </span>
                ))}
              </div>
            </div>
          ))
        ) : (
          !loading && <p style={{ textAlign: 'center', gridColumn: '1/-1' }}>Nenhum jogo gerado ainda.</p>
        )}
      </div>
    </div>
  );
}

const rootElement = document.getElementById("root");
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<App />);
}

