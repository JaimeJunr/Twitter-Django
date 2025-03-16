
// Função para atualizar o contador de retweets na interface
function updateRetweetUI(tweetId, retweetCount) {
  const retweetCountElement = document.querySelector(`#retweet-count-${tweetId}`);
  if (retweetCountElement) {
    retweetCountElement.textContent = retweetCount;
  }
}


async function retweet(tweetId, csrfToken) {
    const retweetContent = document.getElementById("retweetContent").value.trim();

    try {

        const formData = new URLSearchParams();
        formData.append("content", retweetContent);

        const response = await fetch(`/tweet/${tweetId}/retweet/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: formData.toString(),
        });

        if (!response.ok) {
            console.error("Erro na resposta:", response.status, response.statusText);
            alert("Ocorreu um erro ao tentar retweetar. Por favor, tente novamente.");
            return;
        }

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            console.error("Resposta não é JSON:", await response.text());
            alert("Ocorreu um erro ao tentar retweetar. Resposta inválida do servidor.");
            return;
        }

        const data = await response.json();

        if (data.error) {
            console.error("Erro do servidor:", data.error);
            alert("Ocorreu um erro ao tentar retweetar. Por favor, tente novamente.");
            return;
        }

        // Atualiza a UI com o novo número de retweets
        updateRetweetUI(tweetId, data.retweetCount);

        // Fecha a modal após o retweet e limpa o campo de comentário

             // Recarrega a página para atualizar os tweets
        window.location.reload();

        document.getElementById("retweetContent").value = "";

   

    } catch (error) {
        console.error("Erro ao retweetar:", error.message);
        alert("Ocorreu um erro ao tentar retweetar. Por favor, tente novamente.");
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
