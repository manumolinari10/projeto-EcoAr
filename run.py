from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)   #debug=True faz o servidor reiniciar sozinho quando você salva um arquivo, e mostra erros detalhados no navegador — ótimo pra desenvolvimento (nunca deixar isso ligado em produção).