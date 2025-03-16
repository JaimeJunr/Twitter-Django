async function deleteTweet(){
    document.querySelectorAll('.delete-tweet-link').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const tweetId = this.dataset.tweetId;
            const csrfToken = "{{ csrf_token }}";

            if (confirm('Tem certeza que deseja deletar este tweet?')) {
                fetch(`tweet/${tweetId}/delete`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            // Lógica para remover o tweet da página ou recarregar
                            document.getElementById(`tweet-${tweetId}`).remove();
                        } else {
                            alert('Erro ao deletar o tweet.');
                        }
                    })
                    .catch(error => console.error('Erro:', error));
            }
        });
    })
}