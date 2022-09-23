const forms = document.querySelectorAll(".form-delete");

const escope = () => {
    for(const form of forms){
        form.addEventListener('submit', (e) =>{
            e.preventDefault();

            const confirmDeletion = confirm("Você tem certeza que quer excluir esta receita ?");

            if(confirmDeletion){
                form.submit();
            }
        });
    }
}

escope();