async function retweet(tweetId, csrfToken) {
  const retweetContent = document.getElementById("retweetContent").value;

  // Se não houver conteúdo, use o conteúdo do tweet original
  const contentToSubmit =
    retweetContent.trim() === "" ? tweetContent : retweetContent;

  try {
    const response = await fetch(`/tweet/${tweetId}/retweet/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content: contentToSubmit }), // Enviando o conteúdo correto
    });

    if (!response.ok) {
      throw new Error("Falha ao realizar retweet");
    }

    const data = await response.json(); // Obtenha a resposta em JSON
    updateRetweetUI(tweetId, data.retweetCount);

    window.location.reload(); // Recarrega a página para atualizar a lista de tweets
  } catch (error) {
    console.error("Erro ao retweetar:", error.message);
    alert("Ocorreu um erro ao tentar retweetar. Por favor, tente novamente.");
  }
}

function updateRetweetUI(tweetId, retweetCount) {
  const retweetCountElement = document.querySelector(
    `#retweet-count-${tweetId}`
  );

  retweetCountElement.textContent = retweetCount;
}

async function openRetweetModal(tweetId, csrfToken, modal) {
  const tweetContentElement = document.querySelector(
    `#tweet-content-${tweetId}`
  );
  const tweetRetweetElement = document.querySelector(
    `#tweet-retweet-${tweetId}`
  );

  let tweetContent = "";

  // Verifique se o conteúdo do tweet original está disponível
  if (tweetContentElement) {
    tweetContent = tweetContentElement.innerText;
  } else if (tweetRetweetElement) {
    tweetContent = tweetRetweetElement.innerText;
  }

  document.getElementById("originalTweetContent").innerText = tweetContent;

  modal.show();

  // Definindo o evento para o botão de enviar retweet
  document.getElementById("submitRetweet").onclick = async () => {
    retweet(tweetId, csrfToken);
  };
}
