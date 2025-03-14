// Função para retweetar
async function retweet(tweetId, csrfToken) {
  const retweetContent = document.getElementById("retweetContent").value.trim();

  try {
    console.log("Id:",tweetId)
    console.log("Conteudo:", retweetContent)

    const formData = new URLSearchParams();
    formData.append("content", retweetContent);

    const response = await fetch(`/tweet/${tweetId}/retweet/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(), // Envia os dados como um formulário normal
    });

    if (!response.ok) {
      console.log(response.message);
    }

    const data = await response.json(); // Obtenha a resposta em JSON

    // Atualiza a UI com o novo número de retweets
    updateRetweetUI(tweetId, data.retweetCount);

    // Fecha a modal após o retweet e limpa o campo de comentário
    const modal = bootstrap.Modal.getInstance(document.getElementById('retweetModal'));
    modal.hide();
    document.getElementById("retweetContent").value = ""; // Limpar campo

  } catch (error) {
    console.error("Erro ao retweetar:", error.message);
    alert("Ocorreu um erro ao tentar retweetar. Por favor, tente novamente.");
  }
}

// Função para atualizar o contador de retweets na interface
function updateRetweetUI(tweetId, retweetCount) {
  const retweetCountElement = document.querySelector(`#retweet-count-${tweetId}`);
  if (retweetCountElement) {
    retweetCountElement.textContent = retweetCount;
  }
}

// Função para abrir a modal e preencher o conteúdo original
async function openRetweetModal(tweetId, csrfToken, modal) {
  const tweetContentElement = document.querySelector(`#tweet-content-${tweetId}`);
  const tweetRetweetElement = document.querySelector(`#tweet-retweet-${tweetId}`);

  let tweetContent = "";

  // Verifique se o conteúdo do tweet original está disponível
  if (tweetContentElement) {
    tweetContent = tweetContentElement.innerText;
  } else if (tweetRetweetElement) {
    tweetContent = tweetRetweetElement.innerText;
  }

  // Defina o conteúdo do tweet original na modal
  document.getElementById("originalTweetContent").innerText = tweetContent;

  // Exibe o modal
  modal.show();

  // Definindo o evento para o botão de enviar retweet
  document.getElementById("submitRetweet").onclick = () => {
    retweet(tweetId, csrfToken); // Chama a função de retweet
  };
}
