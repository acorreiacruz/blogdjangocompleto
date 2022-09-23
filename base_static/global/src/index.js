const escope = () => {
    const form = document.querySelector(".form-delete");
    form.addEventListener('submit', (e) =>{
        e.preventDefault();

        const confirmDeletion = confirm("Você tem certeza que quer excluir esta receita ?");
        
        if(confirmDeletion){
            form.submit();
        }
    });
}

escope();