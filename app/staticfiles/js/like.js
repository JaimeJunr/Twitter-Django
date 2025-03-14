async function handleLikeButtonClick(
  button,
  tweetId,
  csrfToken,
  textElement,
  likeCountElement,
  iconElement
) {
  const liked = button.dataset.liked === "true"; // Verifica se o tweet já foi curtido

  let likeCount = parseInt(likeCountElement.innerText) || 0;

  // Atualiza o estado visual imediatamente (mesmo antes da requisição)
  if (!liked) {
    // Simular curtir imediatamente
    iconElement.classList.remove("far"); // Ícone contornado (não curtido)
    iconElement.classList.add("fas"); // Ícone preenchido (curtido)
    textElement.innerText = "Descurtir"; // Atualiza o texto
    likeCount += 1;
  } else {
    // Simular descurtir imediatamente
    iconElement.classList.remove("fas"); // Ícone preenchido (curtido)
    iconElement.classList.add("far"); // Ícone contornado (não curtido)
    textElement.innerText = "Curtir"; // Atualiza o texto
    likeCount -= 1;
  }

  // Atualiza imediatamente o contador de curtidas
  likeCountElement.innerHTML = `${likeCount}`;
  try {
    // Enviar requisição para curtir/descurtir
    const response = await fetch(`/tweet/${tweetId}/like/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({}),
    });

    if (!response.ok) {
      throw new Error(`Erro: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    // Atualiza o estado do botão e ícone com base no estado curtido
    button.dataset.liked = data.liked; // Atualiza o estado do botão

    if (!data.liked && liked) {
      // Reverter a mudança de curtida se a API falhar ou se a curtida não for confirmada
      iconElement.classList.remove("fas");
      iconElement.classList.add("far");
      textElement.innerText = "Curtir";
      likeCount -= 1;
    } else if (data.liked && !liked) {
      // Confirmação de que o tweet foi curtido
      iconElement.classList.remove("far");
      iconElement.classList.add("fas");
      textElement.innerText = "Descurtir";
      likeCount += 1;
    }

    // Atualiza a contagem de curtidas na interface
  } catch (error) {
    console.error("Erro ao curtir/descurtir:", error);
    alert("Ocorreu um erro. Tente novamente mais tarde.");
    // Reverter a mudança local em caso de erro
    if (!liked) {
      // Reverte o estado de curtir
      iconElement.classList.remove("fas");
      iconElement.classList.add("far");
      textElement.innerText = "Curtir";
      likeCount -= 1;
    } else {
      // Reverte o estado de descurtir
      iconElement.classList.remove("far");
      iconElement.classList.add("fas");
      textElement.innerText = "Descurtir";
      likeCount += 1;
    }

    // Reverter a contagem de curtidas
    likeCountElement.innerHTML = `${likeCount}`;
  } finally {
    button.disabled = false; // Reabilitar o botão após o processamento
  }
}
